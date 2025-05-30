from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role:str #"ops" or "client"

class UserInDB(UserCreate):
    is_verified: bool = False
    verification_token: Optional[str]

class FileInDB(BaseModel):
    filename: str
    owner: str  # client email
    content: bytes    
