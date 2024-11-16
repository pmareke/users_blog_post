from pydantic import BaseModel


class CreatedUserResponse(BaseModel):
    id: str
