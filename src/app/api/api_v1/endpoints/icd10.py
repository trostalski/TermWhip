from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from nxontology import NXOntology

from app.schemas.icd10 import ICD10CodeOut
from app.api import deps
from app.logic.icd10 import read
from app.models.icd10.ICD10Code import ICD10Code

router = APIRouter()


@router.get("/{code}", response_model=ICD10CodeOut)
def read_code(
    code: str,
    db: Session = Depends(deps.get_db),
    G: NXOntology = Depends(deps.get_icd10_graph),
):
    db_code = db.get(ICD10Code, code)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    return_code = read.get_code(db=db, code=code, G=G)
    return return_code
