from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.loinc import LoincCodeOut
from app.api import deps
from app.logic.loinc import read
from app.schemas.loinc import LoincCodedTerm, LoincFtsOut

router = APIRouter()


@router.get("/code/{code}", response_model=LoincCodeOut)
def read_concept(code: str, db: Session = Depends(deps.get_db)):
    db_concept = read.get_code(db, code=code)
    if db_concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    return LoincCodeOut(
        code=db_concept.code,
        component=db_concept.component,
    )


@router.get("/fts", response_model=LoincFtsOut)
def read_fts(search_term: str, limit: str = 100, db: Session = Depends(deps.get_db)):
    query = text(
        """
            SELECT component, code, ts_rank(fts_ts_vector, to_tsquery(:term)) AS rank
            FROM loinc_codes
            WHERE to_tsquery(:term) @@ fts_ts_vector
            AND status = 'ACTIVE'
            ORDER BY rank DESC, CHAR_LENGTH(component) ASC
            LIMIT :limit;
        """
    )
    terms = db.execute(
        query,
        {"term": search_term, "limit": limit},
    )

    coded_terms = [LoincCodedTerm(term=t[0], code=t[1]) for t in terms]
    return LoincFtsOut(coded_terms=coded_terms)
