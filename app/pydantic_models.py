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
            {"role": "system", "content": "You are a helpful friendly room booking assistant."},
            {"role": "user", "content": "Where do you recommend to go to holidays?"},
            {"role": "assistant", "content": "It depends on your requirements and personal interests."},
            {"role": "user", "content": "Personally I prefer ..."}
        ]
    )


class BookingItem(BaseModel):
    text: str = Field(
        example='I want to make a booking.'
    )
