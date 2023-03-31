from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.schemas.icd9 import ICD9CodeOut
from app.api import deps
from app.models.icd9.ICD9DiagnosisCode import ICD9DiagnosisCode

router = APIRouter()


@router.get("/{code}", response_model=ICD9CodeOut)
def read_code(
    code: str,
    db: Session = Depends(deps.get_db),
):
    db_code = db.get(ICD9DiagnosisCode, code)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    return db_code
