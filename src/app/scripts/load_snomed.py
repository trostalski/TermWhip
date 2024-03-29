import multiprocessing
import sys
import csv
import logging
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.scripts.helper import get_dir_in_downloads
from app.models.snomed import (
    SnomedDescription,
    SnomedConcept,
    SnomedRelationship,
    SnomedOwlExpression,
    SnomedRelationshipConcreteValue,
    SnomedStatedRelationship,
    SnomedTextDefinition,
)
from app.core.decorators import log_error

logger = logging.getLogger(__name__)

# TODO: This is a hack to get around the fact that the Snomed CT files are too big for the default csv field size limit
csv.field_size_limit(sys.maxsize)


@log_error
def load_snomed_file(db: Session, table, file_path: str):
    logger.info(f"Loading {table.__tablename__} from {file_path}, {datetime.now()}")
    with open(file_path) as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader, None)
        for row in reader:
            query = insert(table).values(tuple(row))
            db.execute(query)
        db.commit()
    logger.info(f"Finished loading {table.__tablename__}, {datetime.now()}")


if __name__ == "__main__":
    logging.basicConfig(
        filename="./logs/snomed_upload.log", encoding="utf-8", level=logging.DEBUG
    )
    logging.info(f"Starting upload of Snomed CT, {datetime.now()}")
    session = SessionLocal()
    files_dir = get_dir_in_downloads(
        startswith="SnomedCT", dir_path="Snapshot/Terminology/"
    )

    # First load the concept file, the other files reference it
    found_concept_file = False
    for file in files_dir.iterdir():
        if "Concept" in file.name:
            found_concept_file = True
            load_snomed_file(session, SnomedConcept, file.absolute())
    if not found_concept_file:
        raise FileNotFoundError("Could not find Snomed CT Concept file")

    # Now load the rest of the files
    for file in files_dir.iterdir():
        if "Description" in file.name:
            load_snomed_file(session, SnomedDescription, file.absolute())
        elif "Relationship_" in file.name:
            load_snomed_file(session, SnomedRelationship, file.absolute())
        elif "RelationshipConcreteValues" in file.name:
            load_snomed_file(session, SnomedRelationshipConcreteValue, file.absolute())
        elif "sRefset_OWLExpression" in file.name:
            load_snomed_file(session, SnomedOwlExpression, file.absolute())
        elif "StatedRelationship" in file.name:
            load_snomed_file(session, SnomedStatedRelationship, file.absolute())
        elif "TextDefinition" in file.name:
            load_snomed_file(session, SnomedTextDefinition, file.absolute())
        else:
            print(f"Unknown file: {file.name}")

    # enter data into fts_ts_vector column
    session.execute("")
