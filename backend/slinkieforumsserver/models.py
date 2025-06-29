import pydantic
import typing

class TokenHeader(pydantic.BaseModel):
    user_id: str
    emittedOn: str
    expiry: int
    

class Token(pydantic.BaseModel):    
    header: TokenHeader
    signature: str


class ContentShardModel(pydantic.BaseModel):
    id: int
    author: int
    date: float
    content_type: str


class CategoryModel(pydantic.BaseModel):
    id: int
    title:str
    description: int
    icon:str

class ThreadModel(pydantic.BaseModel):
    id: int
    title: str
    body: int
    date: float
    last_edited: typing.Optional[float]
    authors: list[str]


class Attachment(pydantic.BaseModel):
    mime_type: str
    data: str
    temporary_id: str
    

class CreateThreadRequest(pydantic.BaseModel):
    title: str
    category: int
    body_content: str
    body_mime_type: typing.Literal["text/plain", "text/markdown"]
    allow_replies: bool
    attachments: list[Attachment]


class replyModel(pydantic.BaseModel):
    id: int
    body: int
    author: int
    allow_edits: bool
    allow_replies: bool
    deletion_date: typing.Optional[int]
    children: list[int]