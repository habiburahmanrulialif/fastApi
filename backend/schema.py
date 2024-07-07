from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None

class FeedbackRatingCreate(BaseModel):
    item_id: int
    rating: int

class FeedbackRatingResponse(BaseModel):
    id: int
    user_id: int
    item_id: int
    rating: int

class ItemCreate(BaseModel):
    title: str

class ItemResponse(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
