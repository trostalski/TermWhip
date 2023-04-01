from pydantic import BaseModel


class ICD9CodeOut(BaseModel):
    code: str
    long_description: str
    short_description: str
    version: str = "ICD-9"

    class Config:
        orm_mode = True
