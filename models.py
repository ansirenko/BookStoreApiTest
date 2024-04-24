from pydantic import BaseModel, EmailStr, field_validator


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BookSearch(BaseModel):
    query: str


class AddToCart(BaseModel):
    bookId: int


class Checkout(BaseModel):
    payment_method: str