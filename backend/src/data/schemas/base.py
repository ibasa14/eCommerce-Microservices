import datetime
import typing

import pydantic

from src.utilities.formatters import (
    format_datetime_into_isoformat,
    format_dict_key_to_camel_case,
)


class BaseSchemaModel(pydantic.BaseModel):
    class Config(pydantic.Config):
        orm_mode: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
        json_encoders: dict = {
            datetime.datetime: format_datetime_into_isoformat
        }
        alias_generator: typing.Any = format_dict_key_to_camel_case
