from pydantic import BaseModel, EmailStr, Field

class EmailSchema(BaseModel):
    email: EmailStr
    user_name: str = Field(..., min_length=2, max_length=50)
