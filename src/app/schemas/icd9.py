from pydantic import BaseModel


class ICD9CodeOut(BaseModel):
    code: str
    long_description: str
    short_description: str

    class Config:
        orm_mode = True
