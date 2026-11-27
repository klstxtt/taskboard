from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

TaskStatus = Literal["todo", "in_progress", "done"]
Title = Annotated[str, Field(min_length=1, max_length=200)]
Description = Annotated[str, Field(max_length=2000)]


class _StrictModel(BaseModel):
    # Reject unknown fields (e.g. "id", "owner") and trim every string
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class TaskCreate(_StrictModel):
    title: Title
    description: Description | None = None
    status: TaskStatus = "todo"


class TaskUpdate(_StrictModel):
    title: Title | None = None
    description: Description | None = None
    status: TaskStatus | None = None

    @field_validator("title", "status")
    @classmethod
    def not_null(cls, value):
        # Fields may be omitted, but an explicit null is refused
        if value is None:
            raise ValueError("must not be null")
        return value


class Task(TaskCreate):
    id: int
