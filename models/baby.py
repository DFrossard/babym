import re
from datetime import date
from pydantic import BaseModel, validator

class Baby(BaseModel):
    name: str
    dob: date
    weight: float
    height: float
    
    @validator('name')
    def name_must_contain_only_letters_and_space(cls, v):
        pattern = re.compile(r'^[a-zA-Z\s]+$')
        if not pattern.match(v):
            raise ValueError("Name should only contain letters and white spaces")
        return v.title()
