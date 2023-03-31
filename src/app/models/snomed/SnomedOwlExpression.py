
from sqlalchemy import Column, String

from app.db.base import Base


class SnomedOwlExpression(Base):
    __tablename__ = "snomed_owl_expressions"

    id = Column("id", String, primary_key=True, index=True)
    effectiveTime = Column("effective_time", String, nullable=False)
    active = Column("active", String, nullable=False)
    moduleId = Column("module_id", String, nullable=False)
    refsetId = Column("refset_id", String, nullable=False)
    referencedComponentId = Column("referenced_component_id", String, nullable=False)
    owlExpression = Column("owl_expression", String, nullable=False)

