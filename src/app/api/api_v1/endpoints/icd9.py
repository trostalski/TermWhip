from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.icd9 import ICD9CodeOut
from app.api import deps
from app.models.icd9.ICD9DiagnosisCode import ICD9DiagnosisCode
from app.schemas.snomed import SmomedCodedTerm, SnomedFtsOut

router = APIRouter()


def parse_input_code(code: str):
    res = code.replace(".", "").replace(" ", "")
    return res


@router.get("/code/{code}", response_model=ICD9CodeOut)
def read_code(
    code: str,
    db: Session = Depends(deps.get_db),
):
    code = parse_input_code(code)
    db_code = db.get(ICD9DiagnosisCode, code)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    return db_code


@router.get("/fts", response_model=SnomedFtsOut)
def read_fts(search_term: str, limit: str = 100, db: Session = Depends(deps.get_db)):
    query = text(
        """
            SELECT short_description, code, ts_rank(fts_ts_vector, to_tsquery(:term)) AS rank
            FROM  icd9_codes
            WHERE to_tsquery(:term) @@ fts_ts_vector
            ORDER BY rank DESC, CHAR_LENGTH(short_description) ASC
            LIMIT :limit;
        """
    )
    terms = db.execute(
        query,
        {"term": search_term, "limit": limit},
    )

    coded_terms = [SmomedCodedTerm(term=t[0], code=t[1]) for t in terms]
    return SnomedFtsOut(coded_terms=coded_terms)
