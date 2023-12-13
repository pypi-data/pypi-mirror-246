import typing

import pydantic

import schemaless.bases
import schemaless.config
import schemaless.http_client
import schemaless.delta
import schemaless.rid


class PathHistoryItem(pydantic.BaseModel):
    created_at: int
    delta: schemaless.delta.DeltaModel


class PathHistoryResponse(pydantic.BaseModel):
    history: typing.List[PathHistoryItem]


class SubmitObjectBody(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID
    rid: schemaless.rid.RID
    object: dict[str, typing.Any]


class DeltaListResponse(pydantic.BaseModel):
    delta: typing.List[schemaless.delta.DeltaModel]


class VersionControl(schemaless.bases.Handler):
    def __init__(self, http_client: schemaless.bases.BaseHTTP):
        self.http_client = http_client

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "VersionControl":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
        )

    async def submit_object(
        self,
        domain_rid: schemaless.rid.RID,
        rid: schemaless.rid.RID,
        obj: dict[str, typing.Any],
    ) -> DeltaListResponse:
        response = await self.http_client.post(
            url="/api/v1/vc/object/submit",
            json=SubmitObjectBody(
                domain_rid=domain_rid,
                rid=rid,
                object=obj,
            ).model_dump(),
        )

        return response.parse_to_model(DeltaListResponse)

    async def get_snapshot(
        self,
        domain_rid: schemaless.rid.RID,
        rid: schemaless.rid.RID,
        model: typing.Optional[typing.Type[schemaless.bases.T]] = None,
    ) -> typing.Union[typing.Dict[str, typing.Any], typing.Type[schemaless.bases.T]]:
        response = await self.http_client.get(
            url="/api/v1/vc/object/snapshot",
            params={
                "domain_rid": domain_rid.to_string(),
                "rid": rid.to_string(),
            },
        )

        if model is None:
            return response.data()

        return response.parse_to_model(model)

    async def get_history_of_path(
        self,
        domain_rid: schemaless.rid.RID,
        rid: schemaless.rid.RID,
        path: str,
    ) -> PathHistoryResponse:
        response = await self.http_client.get(
            url="/api/v1/vc/history/path",
            params={
                "domain_rid": domain_rid.to_string(),
                "rid": rid.to_string(),
                "path": path,
            },
        )
        print(response.data())
        return response.parse_to_model(PathHistoryResponse)
