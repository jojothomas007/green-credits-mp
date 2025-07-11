from pydantic import BaseModel
from typing import List, Optional

class Author(BaseModel):
    displayName: str

class Comment(BaseModel):
    body: str
    created: str
    author: Author

class JiraCommentsResponse(BaseModel):
    comments: List[Comment]
    maxResults: int
    startAt: int
    total: int
