from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ICD9DiagnosisCode(Base):
    __tablename__ = "icd9_diagnosis_codes"

    code = Column("code", String, primary_key=True, index=True)
    long_description = Column("long_description", String)
    short_description = Column("short_description", String)
