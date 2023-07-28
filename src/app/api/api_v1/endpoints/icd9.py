from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.schemas.icd9 import ICD9CodeOut
from app.api import deps
from app.models.icd9.ICD9DiagnosisCode import ICD9DiagnosisCode

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
