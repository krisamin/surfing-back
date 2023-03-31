# clast/app/models/base_model.py

import json

from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    def to_json_str(self) -> str:
        return json.loads(self.json())

class GeneralSuccessResponse(BaseSchema):
    message: str = Field(title="Message", description="Return Message")

class GeneralErrorResponse(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class JWTBearerError(BaseSchema):
    detail: str = Field(title="Detail", description="Error Detail")

class NotPeriodError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")