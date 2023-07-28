from sqlalchemy import BigInteger, Column, String
from app.db.base import Base


class SnomedConcept(Base):
    __tablename__ = "snomed_concepts"

    id = Column("id", BigInteger, primary_key=True, index=True)
    effectiveTime = Column("effective_time", String)
    active = Column("active", String)
    moduleId = Column("module_id", String)
    definitionStatusId = Column("definition_status_id", String)
