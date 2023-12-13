import typing

import pydantic


def parse_response_to_model(
    response: dict, model: typing.Type[pydantic.BaseModel]
) -> pydantic.BaseModel:
    return model(**response)
