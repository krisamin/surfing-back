from typing import List

from pydantic import Field

from app.schemas.base_schema import BaseSchema

class SubmitRequest(BaseSchema):
    circle_id: int = Field(title="Circle ID", description="Circle ID")
    question1: str = Field(title="Question 1", description="Question 1", min_length=1, max_length=300)
    question2: str = Field(title="Question 2", description="Question 2", min_length=1, max_length=300)
    question3: str = Field(title="Question 3", description="Question 3", min_length=1, max_length=300)
    question4: str = Field(title="Question 4", description="Question 4")

class SubmitCountOverError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class OwnerCannotSubmitError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class CircleNotFoundError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class MultipleSubmitError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class NotSecondPassedError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class AlreadyFinalChoiceError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class SubmitResponse(BaseSchema):
    circle_id: int = Field(title="Circle ID", description="Circle ID")
    question1: str = Field(title="Question 1", description="Question 1")
    question2: str = Field(title="Question 2", description="Question 2")
    question3: str = Field(title="Question 3", description="Question 3")
    question4: str = Field(title="Question 4", description="Question 4")
    status: str = Field(title="Status", description="Status")
class SubmitListResponse(BaseSchema):
    submit_list: List[SubmitResponse] = Field(title="Submit List", description="Submit List")

class StudentNoNotSetError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")