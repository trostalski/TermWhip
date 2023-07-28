from pydantic import BaseModel
from typing import List, Optional


class SnomedConceptOut(BaseModel):
    id: str
    active: str
    fsn: str
    synonyms: Optional[List[str]] = []
    is_a: Optional[List[str]] = []

    class Config:
        orm_mode = True


class ECLQuery(BaseModel):
    ecl_expression: str


class SmomedCodedTerm(BaseModel):
    term: str
    code: int


class SnomedFtsOut(BaseModel):
    coded_terms: List[SmomedCodedTerm]
