from pydantic import BaseModel
from typing import List


class LoincCodeOut(BaseModel):
    code: str
    component: str

    class Config:
        orm_mode = True


class LoincCodedTerm(BaseModel):
    term: str
    code: str


class LoincFtsOut(BaseModel):
    coded_terms: List[LoincCodedTerm]
