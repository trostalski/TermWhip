from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ICD10Code(Base):
    __tablename__ = "icd10_codes"

    code = Column("code", String, primary_key=True, index=True)
    description = Column("description", String)
    group = relationship("ICD10Group", back_populates="codes")
    group_id = Column("group_id", Integer, ForeignKey("icd10_groups.id"))
    chapter = relationship("ICD10Chapter", back_populates="codes")
    chapter_id = Column("chapter_id", Integer, ForeignKey("icd10_chapters.id"))
