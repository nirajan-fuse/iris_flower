from pydantic import BaseModel, Field


class IrisInput(BaseModel):
    sepal_length: float = Field(
        ..., ge=4.0, le=8.0, description="Sepal length must be between 4.0 and 8.0 cm."
    )
    sepal_width: float = Field(
        ..., ge=2.0, le=4.5, description="Sepal width must be between 2.0 and 4.5 cm."
    )
    petal_length: float = Field(
        ..., ge=1.0, le=7.0, description="Petal length must be between 1.0 and 7.0 cm."
    )
    petal_width: float = Field(
        ..., ge=0.1, le=2.5, description="Petal width must be between 0.1 and 2.5 cm."
    )
