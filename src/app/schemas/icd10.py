from pydantic import BaseModel
from typing import List


class ICD10CodeOut(BaseModel):
    code: str
    description: str
    chapter_code: str
    chapter_description: str
    group_code: str
    group_description: str
    parent: str
    children: List[str] = []

    class Config:
        orm_mode = True
