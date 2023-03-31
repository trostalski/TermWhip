from typing import Generator

from app.db.session import SessionLocal
from app import main


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_snomed_graph():
    G = main.snomed_graph
    return G


def get_icd10_graph():
    G = main.icd10_graph
    return G
