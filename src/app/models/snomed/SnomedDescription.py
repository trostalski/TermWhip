from sqlalchemy import BigInteger, Column, ForeignKey, String, Index
from sqlalchemy.dialects.postgresql import TSVECTOR


from app.db.base import Base


class SnomedDescription(Base):
    __tablename__ = "snomed_descriptions"

    id = Column("id", BigInteger, primary_key=True, index=True)
    effectiveTime = Column("effective_time", String, nullable=False)
    active = Column("active", String, nullable=False)
    moduleId = Column("module_id", String, nullable=False)
    conceptId = Column(
        "concept_id", BigInteger, ForeignKey("snomed_concepts.id"), nullable=False
    )
    languageCode = Column("language_code", String, nullable=False)
    typeId = Column(
        "type_id", BigInteger, ForeignKey("snomed_concepts.id"), nullable=False
    )
    term = Column("term", String, nullable=False)
    caseSignificanceId = Column("case_significance_id", String, nullable=False)
    fts_ts_vector = Column("fts_ts_vector", TSVECTOR)

    __table__args__ = (
        Index(
            "idx_snomed_fts_tsvector",
            fts_ts_vector,
            postgresql_using="gin",
        ),
    )
