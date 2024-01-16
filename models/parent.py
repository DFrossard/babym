import re
from typing import Optional
from datetime import date
from pydantic import BaseModel, validator

class Parent(BaseModel):
    name: str
    dob: Optional[date] = None
    email: Optional[str] = None

    @validator('name')
    def name_must_contain_only_letters_and_space(cls, v):
        pattern = re.compile(r'^[a-zA-Z\s]+$')
        if not pattern.match(v):
            raise ValueError("Name should only contain letters and white spaces")
        return v.title()
    
    @validator('email')
    def validate_email(cls, v):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email address')
        return v