from pydantic import BaseModel


class UserInfoSchema(BaseModel):
    username: str