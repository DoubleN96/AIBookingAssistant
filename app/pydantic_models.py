from pydantic import BaseModel, Field


class ResponseStatus(BaseModel):
    code: int
    text: str


class TextItem(BaseModel):
    text: str = Field(
        example='ani za nic'
    )
    history: list[dict] = Field(
        example=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
