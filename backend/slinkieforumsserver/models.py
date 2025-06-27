import pydantic
import typing

class CategoryModel(pydantic.BaseModel):
    id: int
    title:str
    description: int
    icon:str

class ThreadModel(pydantic.BaseModel):
    id: int
    title: str
    date: int
    body: int

class ThreadMetricsModel(pydantic.BaseModel):
    replies: int
    last_reply: int

class TokenHeader(pydantic.BaseModel):
    user_id: str
    emittedOn: str
    expiry: int
    
class Token(pydantic.BaseModel):    
    header: TokenHeader
    signature: str