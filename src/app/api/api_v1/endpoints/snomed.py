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
def read_fts(search_term: str, limit: str = 100, db: Session = Depends(deps.get_db)):
    query = text(
        """
            SELECT d.term, c.id, ts_rank(fts_ts_vector, to_tsquery(:term)) AS rank
            FROM snomed_descriptions d
            JOIN snomed_concepts c ON c.id = d.concept_id
            WHERE to_tsquery(:term) @@ fts_ts_vector
            AND d.type_id = '900000000000003001'
            AND c.active = '1'
            AND d.active = '1'
            ORDER BY rank DESC, CHAR_LENGTH(d.term) ASC
            LIMIT :limit;
        """
    )
    terms = db.execute(
        query,
        {"term": search_term, "limit": limit},
    )

    coded_terms = [CodedTerm(term=t[0], code=t[1]) for t in terms]
    return FtsOut(coded_terms=coded_terms)
