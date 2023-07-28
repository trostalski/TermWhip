from sqlalchemy.orm import Session
from app.models.loinc.LoincCode import LoincCode
from app.schemas.loinc import LoincCodeOut


def get_code(db: Session, code: str):
    code_data = db.get(LoincCode, code)
    return code_data
