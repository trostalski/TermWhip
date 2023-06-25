from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.schemas.snomed import SnomedConceptOut, ECLQuery
from app.api import deps
from app.logic.snomed import read, ecl

router = APIRouter()


@router.get("/{id}", response_model=SnomedConceptOut)
def read_concept(id: int, db: Session = Depends(deps.get_db)):
    db_concept = read.get_concept(db, id=id)
    if db_concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    return db_concept


@router.post("/ecl", response_model=list[SnomedConceptOut])
def read_concept(ecl_expression: ECLQuery, db: Session = Depends(deps.get_db)):
    psql_query = ecl.transform_ecl_to_sql(ecl_expression=ecl_expression.ecl_expression)
    print(psql_query)
    db.query(psql_query)
    return None
