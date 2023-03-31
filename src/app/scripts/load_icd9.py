# Description: Loads ICD-9 from https://www.cms.gov/Medicare/Coding/ICD9ProviderDiagnosticCodes/codesdata into the database
import sys
import csv
import logging
from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.icd9 import ICD9DiagnosisCode, ICD9ProcedureCode
from app.scripts.helper import get_dir_in_downloads
from app.core.decorators import log_error

logger = logging.getLogger(__name__)

# TODO: This is a hack to get around the fact that the Snomed CT files are too big for the default csv field size limit
csv.field_size_limit(sys.maxsize)


@log_error
def load_icd9_file(db: Session, table, file_path: str, file_type: str):
    logger.info(f"Loading {table.__tablename__} from {file_path}, {datetime.now()}")
    with open(file_path, encoding="latin-1") as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.split(" ")
            code = line_list[0]
            description = " ".join(line_list[1:])
            description = description.lstrip()
            description = description.rstrip()
            code = code.lstrip()

            db_entry = db.query(table).filter(table.code == code).first()
            if db_entry:
                if file_type == "long":
                    db_entry.long_description = description
                elif file_type == "short":
                    db_entry.short_description = description
            else:
                if file_type == "long":
                    query = insert(table).values(
                        code=code, long_description=description
                    )
                elif file_type == "short":
                    query = insert(table).values(
                        code=code, short_description=description
                    )
                db.execute(query)
        db.commit()
    logger.info(f"Finished loading {table.__tablename__}, {datetime.now()}")


if __name__ == "__main__":
    logging.basicConfig(
        filename="./logs/icd9_upload.log", encoding="utf-8", level=logging.DEBUG
    )
    logger.info(f"Starting upload of ICD-9, {datetime.now()}")
    session = SessionLocal()

    files_dir = get_dir_in_downloads(startswith="ICD-9", dir_path=".")

    for file in files_dir.iterdir():
        if "LONG_DX.txt" in file.name:
            load_icd9_file(session, ICD9DiagnosisCode, file.absolute(), "long")
        elif "LONG_SG.txt" in file.name:
            load_icd9_file(session, ICD9ProcedureCode, file.absolute(), "long")
        elif "SHORT_DX.txt" in file.name:
            load_icd9_file(session, ICD9DiagnosisCode, file.absolute(), "short")
        elif "SHORT_SG.txt" in file.name:
            load_icd9_file(session, ICD9ProcedureCode, file.absolute(), "short")
