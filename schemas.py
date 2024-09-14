from pydantic import BaseModel


class TransformRequest(BaseModel):
    value: str