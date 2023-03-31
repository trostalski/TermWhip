from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.schemas.snomed import SnomedConceptOut
from app.api import deps
from app.logic.snomed import read

router = APIRouter()


@router.get("/{id}", response_model=SnomedConceptOut)
def read_concept(id: int, db: Session = Depends(deps.get_db)):
    db_concept = read.get_concept(db, id=id)
    if db_concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    return db_concept
