from sqlalchemy import Boolean, Column, Integer, String, ForeignKey

from app.db.base import Base


class ICD9ToICD10Map(Base):
    __tablename__ = "icd9_to_icd10_map"

    id = Column("id", Integer, primary_key=True, index=True)
    icd9_code = Column("code", String)
    icd10_code = Column("icd10_code", String)
    approximate = Column("approximate", Boolean)
    no_map = Column("no_map", Boolean)
    combination = Column("combination", Boolean)
    scenario = Column("scenario", Integer)
    choice = Column("choice", Integer)
