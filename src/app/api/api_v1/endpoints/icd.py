from fastapi import Depends, HTTPException, APIRouter
from nxontology import NXOntology
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.icd9 import ICD9CodeOut
from app.schemas.icd10 import ICD10CodeOut
from app.models.icd9.ICD9DiagnosisCode import ICD9DiagnosisCode
from app.models.icd10.ICD10Code import ICD10Code
from app.logic.icd10 import read

router = APIRouter()


@router.get("/{code}", response_model=ICD9CodeOut | ICD10CodeOut)
def read_code(
    code: str,
    db: Session = Depends(deps.get_db),
    G: NXOntology = Depends(deps.get_icd10_graph),
):
    db_code = db.get(ICD9DiagnosisCode, code)
    if db_code:
        return db_code
    else:
        db_code = db.get(ICD10Code, code)
        if db_code is None:
            raise HTTPException(status_code=404, detail="Concept not found")
        else:
            return_code = read.get_code(db=db, code=code, G=G)
            return return_code
