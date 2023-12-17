import enum
import typing
import datetime

import cloudevents.pydantic.v2
import pydantic

import schemaless.rid
import schemaless.bases
import schemaless.config
import schemaless.http_client
import schemaless.delta


class WebhookRelations(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID


class WebhookModel(pydantic.BaseModel):
    rid: schemaless.rid.RID
    relations: WebhookRelations
    alias: typing.Union[str, None] = None
    name_prefix: typing.Union[str, None] = None
    pattern: str
    on_operations: typing.List[schemaless.delta.Operation]
    url: str
    created_at: int
    modified_at: int
    deleted_at: typing.Union[int, None] = None

    def get_created_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.created_at)

    def get_updated_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.modified_at)

    def get_deleted_at_datetime(self):
        return datetime.datetime.fromtimestamp(self.deleted_at)

    @classmethod
    def from_api_response(cls, response: dict) -> "WebhookModel":
        return cls(
            **response,
        )


class RegisterWebhookBody(pydantic.BaseModel):
    id: typing.Union[str, None] = None
    domain_rid: schemaless.rid.RID
    pattern: str
    on_operations: typing.List[schemaless.delta.Operation]
    url: str
    alias: typing.Union[str, None] = None
    name_prefix: typing.Union[str, None] = None

    model_config = pydantic.ConfigDict(use_enum_values=True)


class WebhookHistoryStatus(enum.Enum):
    Success = "Success"
    Error = "Error"
    Fail = "Fail"


class Relations(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID
    entity_rid: schemaless.rid.RID
    webhook_rid: schemaless.rid.RID


class History(pydantic.BaseModel):
    rid: schemaless.rid.RID
    relations: Relations
    event: cloudevents.pydantic.v2.CloudEvent
    created_at: int
    status: WebhookHistoryStatus
    message: typing.Union[str, None] = None


class HistoryResponse(pydantic.BaseModel):
    history: typing.List[History] = []


class EventHistoryFilters(pydantic.BaseModel):
    domain_rid: typing.Union[schemaless.rid.RID, None] = None
    rid: typing.Union[schemaless.rid.RID, None] = None
    entity_rid: typing.Union[schemaless.rid.RID, None] = None

    def to_request_params(self) -> dict:
        base = {}
        if self.domain_rid is not None:
            base["domain_rid"] = self.domain_rid.to_string()
        if self.rid is not None:
            base["rid"] = self.rid.to_string()
        if self.entity_rid is not None:
            base["entity_rid"] = self.entity_rid.to_string()
        return base


class WebhookHistory(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID


class Webhook(schemaless.bases.Handler):
    def __init__(self, http_client: schemaless.bases.BaseHTTP):
        self.http_client = http_client

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "Webhook":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
        )

    async def register(self, webhook: RegisterWebhookBody) -> WebhookModel:
        response = await self.http_client.post(
            url="/api/v1/webhook/register",
            json=webhook.model_dump(),
        )

        return response.parse_to_model(WebhookModel)

    async def history(self, filters: EventHistoryFilters) -> HistoryResponse:
        response = await self.http_client.get(
            url="/api/v1/webhook/history",
            params=filters.to_request_params(),
        )

        return response.parse_to_model(HistoryResponse)
