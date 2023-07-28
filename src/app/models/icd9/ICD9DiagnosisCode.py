from sqlalchemy import Column, String, Index
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.db.base import Base


class ICD9DiagnosisCode(Base):
    __tablename__ = "icd9_codes"

    code = Column("code", String, primary_key=True, index=True)
    long_description = Column("long_description", String)
    short_description = Column("short_description", String)
    fts_ts_vector = Column("fts_ts_vector", TSVECTOR)

    __table__args__ = (
        Index(
            "idx_icd9_fts_tsvector",
            fts_ts_vector,
            postgresql_using="gin",
        ),
    )
