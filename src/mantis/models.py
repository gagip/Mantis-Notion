from pydantic import BaseModel
from typing import Optional

class Project(BaseModel):
    id: int
    name: str

class Issue(BaseModel):
    id: int
    summary: str
    description: str
    status: str