import typing
import datetime
import pydantic

import schemaless.rid
import schemaless.bases
import schemaless.config
import schemaless.http_client
import schemaless.delta


class Relations(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID
    entity_rid: schemaless.rid.RID


class CommitModel(pydantic.BaseModel):
    rid: schemaless.rid.RID
    relations: Relations
    deltas: typing.List[schemaless.delta.DeltaModel]
    branch: str
    parents: typing.Union[typing.List[schemaless.rid.RID], None] = None
    hash: str
    created_at: int
    modified_at: int
    deleted_at: typing.Union[int, None] = None

    model_config = pydantic.ConfigDict(use_enum_values=True)

    def get_created_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.created_at)

    def get_updated_at_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.modified_at)

    def get_deleted_at_datetime(self):
        return datetime.datetime.fromtimestamp(self.deleted_at)

    @classmethod
    def from_api_response(cls, response: dict) -> "CommitModel":
        return cls(
            **response,
        )


class Domain(schemaless.bases.Handler):
    def __init__(self, http_client: schemaless.bases.BaseHTTP):
        self.http_client = http_client

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "Domain":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
        )
