from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.db.base import Base


class ICD10Code(Base):
    __tablename__ = "icd10_codes"

    code = Column("code", String, primary_key=True, index=True)
    description = Column("description", String)
    group = relationship("ICD10Group", back_populates="codes")
    group_id = Column("group_id", Integer, ForeignKey("icd10_groups.id"))
    chapter = relationship("ICD10Chapter", back_populates="codes")
    chapter_id = Column("chapter_id", Integer, ForeignKey("icd10_chapters.id"))
    fts_ts_vector = Column("fts_ts_vector", TSVECTOR)

    __table__args__ = (
        Index(
            "idx_icd10_fts_tsvector",
            fts_ts_vector,
            postgresql_using="gin",
        ),
    )
