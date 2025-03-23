from pydantic import BaseModel


class PasswordCreate(BaseModel):
    password: str


class PasswordResponse(BaseModel):
    service_name: str
    password: str
