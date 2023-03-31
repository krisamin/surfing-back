from typing import List

from pydantic import Field

from app.schemas.base_schema import BaseSchema

class NoPermissionError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class AdminSubmitResponse(BaseSchema):
    submit_id: int = Field(title="Submit ID", description="Submit ID")
    submitter_grade: int = Field(title="Submitter Grade", description="Submitter Grade")
    submitter_class: int = Field(title="Submitter Class", description="Submitter Class")
    submitter_student_no: int = Field(title="Submitter Student No", description="Submitter Student No")
    submitter_realname: str = Field(title="Submitter Real Name", description="Submitter Real Name")
    submitter_email: str = Field(title="Submitter Email", description="Submitter Email")
    question1: str = Field(title="Question 1", description="Question 1")
    question2: str = Field(title="Question 2", description="Question 2")
    question3: str = Field(title="Question 3", description="Question 3")
    question4: str = Field(title="Question 4", description="Question 4")
    status: str = Field(title="Status", description="Status")

class AdminSubmitListResponse(BaseSchema):
    circle_id: int = Field(title="Circle ID", description="Circle ID")
    submit_list: List[AdminSubmitResponse] = Field(title="Submit List", description="Submit List")

class SubmitNotFoundError(BaseSchema):
    error: str = Field(title="Error", description="Error Message")

class FirstConfirmResponse(BaseSchema):
    submitter_email: str = Field(title="Submitter Email", description="Submitter Email")