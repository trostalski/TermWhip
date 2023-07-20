from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.schemas.snomed import SnomedConceptOut, FtsOut, CodedTerm
from app.models.snomed import SnomedConcept, SnomedDescription
from app.api import deps
from app.logic.snomed import read

router = APIRouter()


@router.get("/code/{id}", response_model=SnomedConceptOut)
def read_concept(id: int, db: Session = Depends(deps.get_db)):
    db_concept = read.get_concept(db, id=id)
    if db_concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    return db_concept


@router.get("/fts", response_model=FtsOut)
def read_fts(search_term: str, db: Session = Depends(deps.get_db)):
    query = text(
        """
        select d.term, c.id from snomed_descriptions d, snomed_concepts c
        where c.id = d.concept_id AND to_tsquery(:term) @@ term_ts_vector
        limit 10;
        """
    )
    terms = db.execute(
        query,
        {"term": search_term},
    )

    coded_terms = [CodedTerm(term=t[0], code=t[1]) for t in terms]
    return FtsOut(coded_terms=coded_terms)
