from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ICD10Group(Base):
    __tablename__ = "icd10_groups"

    id = Column("id", Integer, primary_key=True, index=True)
    group_code = Column("group_code", String, index=True, nullable=False)
    description = Column("description", String)
    chapter_id = Column("chapter_id", Integer, ForeignKey("icd10_chapters.id"))
    codes = relationship("ICD10Code", back_populates="group")
    chapter = relationship("ICD10Chapter", back_populates="groups")
