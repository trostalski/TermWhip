import sys
import csv
import logging
from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.loinc import LoincCode
from app.scripts.helper import get_dir_in_downloads
from app.core.decorators import log_error

logger = logging.getLogger(__name__)

# TODO: This is a hack to get around the fact that the Snomed CT files are too big for the default csv field size limit
csv.field_size_limit(sys.maxsize)


@log_error
def load_loinc_file(db: Session, table, file_path: str):
    logger.info(f"Loading {table.__tablename__} from {file_path}, {datetime.now()}")
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=",", quoting=csv.QUOTE_NONE)
        next(reader, None)
        for row in reader:
            row = [r.replace('"', "") for r in row]
            if len(row) > 16:
                cr = ",".join(row[11:-4])
                row = row[:11] + [cr] + row[-4:]
            query = insert(table).values(tuple(row))
            db.execute(query)
        db.commit()
    logger.info(f"Finished loading {table.__tablename__}, {datetime.now()}")


if __name__ == "__main__":
    logging.basicConfig(
        filename="./logs/loinc_upload.log", encoding="utf-8", level=logging.DEBUG
    )
    logger.info(f"Starting upload of LOINC, {datetime.now()}")
    session = SessionLocal()

    files_dir = get_dir_in_downloads(startswith="Loinc", dir_path="LoincTableCore/")

    for file in files_dir.iterdir():
        if "LoincTableCore.csv" in file.name:
            load_loinc_file(session, LoincCode, file.absolute())
