from fastapi import APIRouter

from app.api.api_v1.endpoints import snomed
from app.api.api_v1.endpoints import icd10
from app.api.api_v1.endpoints import icd9
from app.api.api_v1.endpoints import loinc

api_router = APIRouter()
api_router.include_router(snomed.router, prefix="/snomed", tags=["snomed"])
api_router.include_router(icd10.router, prefix="/icd10", tags=["icd10"])
api_router.include_router(icd9.router, prefix="/icd9", tags=["icd9"])
api_router.include_router(loinc.router, prefix="/loinc", tags=["loi"])
