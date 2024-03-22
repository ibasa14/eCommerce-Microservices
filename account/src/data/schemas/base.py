import datetime
import pydantic

from src.utilities.formatters import (
    format_datetime_into_isoformat,
)


class BaseSchemaModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        from_attributes= True,
        validate_assignment= True,
        populate_by_name= True,
        json_encoders = {
            datetime.datetime: format_datetime_into_isoformat
        }
    )
