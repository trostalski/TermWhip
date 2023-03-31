from sqlalchemy import BigInteger, Column, ForeignKey, String

from app.db.base import Base


class SnomedRelationship(Base):
    __tablename__ = "snomed_relationships"

    id = Column("id", BigInteger, primary_key=True, index=True)
    effectiveTime = Column("effective_time", String, nullable=False)
    active = Column("active", String, nullable=False)
    moduleId = Column("module_id", String, nullable=False)
    sourceId = Column(
        "source_id",
        BigInteger,
        ForeignKey("snomed_concepts.id"),
        primary_key=True,
        nullable=False,
    )
    destinationId = Column(
        "destination_id",
        BigInteger,
        ForeignKey("snomed_concepts.id"),
        primary_key=True,
        nullable=False,
    )
    relationshipGroup = Column("relationship_group", String, nullable=False)
    typeId = Column(
        "type_id", BigInteger, ForeignKey("snomed_concepts.id"), nullable=False
    )
    characteristicTypeId = Column("characteristic_type_id", String, nullable=False)
    modifierId = Column("modifier_id", String, nullable=False)
