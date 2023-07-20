from sqlalchemy.orm import Session

from app.models.snomed import SnomedConcept, SnomedDescription, SnomedRelationship
from app.schemas.snomed import SnomedConceptOut
from .constants import FULLY_SPECIFIED_NAME, IS_A, SYNONYM


def get_concept(db: Session, id: int):
    terms = (
        db.query(
            SnomedConcept.active,
            SnomedDescription.term,
            SnomedDescription.typeId,
        )
        .filter(SnomedConcept.id == id)
        .filter(SnomedConcept.id == SnomedDescription.conceptId)
        .all()
    )

    is_a = (
        db.query(
            SnomedRelationship.destinationId,
        )
        .filter(SnomedConcept.id == id)
        .filter(SnomedConcept.id == SnomedRelationship.sourceId)
        .filter(SnomedRelationship.typeId == IS_A)
        .all()
    )

    active = terms[0].active

    is_a = [is_a.destinationId for is_a in is_a]  # parents

    fsn = None
    synonyms = []
    for term in terms:
        print(term.typeId)
        if term.typeId == FULLY_SPECIFIED_NAME:
            fsn = term.term
        elif term.typeId == SYNONYM:
            synonyms.append(term.term)

    return SnomedConceptOut(
        id=id,
        active=active,
        fsn=fsn,
        synonyms=synonyms,
        is_a=is_a,
    )


def text_search():
    pass
