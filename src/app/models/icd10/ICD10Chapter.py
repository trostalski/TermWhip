from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class ICD10Chapter(Base):
    __tablename__ = "icd10_chapters"

    id = Column("id", Integer, primary_key=True, index=True)
    chapter_code = Column("chapter_code", String, index=True, nullable=False)
    description = Column("description", String)
    codes = relationship("ICD10Code", back_populates="chapter")
    groups = relationship("ICD10Group", back_populates="chapter")
