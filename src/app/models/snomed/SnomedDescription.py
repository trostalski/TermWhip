from sqlalchemy import BigInteger, Column, ForeignKey, String

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
