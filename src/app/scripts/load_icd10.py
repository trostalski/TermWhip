# Description: Loads ICD-10 from https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-CM-and-GEMs into the database
import sys
import csv
import logging
from datetime import datetime
import xml.etree.ElementTree as ET

from sqlalchemy import insert

from app.db.session import SessionLocal
from app.models.icd10 import ICD10Chapter, ICD10Code, ICD10Group
from app.scripts.helper import get_dir_in_downloads

logger = logging.getLogger(__name__)

# TODO: This is a hack to get around the fact that the Snomed CT files are too big for the default csv field size limit
csv.field_size_limit(sys.maxsize)


def add_chapter(chapter_code: str, desc: str):
    query = insert(ICD10Chapter).values(chapter_code=chapter_code, description=desc)
    session.execute(query)


def add_group(group_code: str, desc: str, chapter_code: str):
    chapter_id = (
        session.query(ICD10Chapter)
        .filter(ICD10Chapter.chapter_code == chapter_code)
        .first()
        .id
    )
    query = insert(ICD10Group).values(
        group_code=group_code, description=desc, chapter_id=chapter_id
    )
    session.execute(query)


def add_code(code: str, desc: str, group_code: str):
    code = code.replace(".", "")
    group = (
        session.query(ICD10Group).filter(ICD10Group.group_code == group_code).first()
    )
    query = insert(ICD10Code).values(
        code=code, description=desc, group_id=group.id, chapter_id=group.chapter_id
    )
    session.execute(query)


def load_icd10_file(file_path: str):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for chapter in root.findall("chapter"):
        chapter_code = chapter.find("name").text
        desc = chapter.find("desc").text
        add_chapter(chapter_code=chapter_code, desc=desc)
        for section_ref in chapter.findall("sectionIndex/sectionRef"):
            group_code = section_ref.attrib["id"].strip()
            desc = section_ref.text.strip()
            add_group(group_code=group_code, desc=desc, chapter_code=chapter_code)
        for section in chapter.findall("section"):
            for el in section.iter():
                if el.tag == "diag":
                    code = el.find("name").text
                    desc = el.find("desc").text
                    add_code(code=code, desc=desc, group_code=group_code)
    session.commit()


if __name__ == "__main__":
    logging.basicConfig(
        filename="./logs/icd10_upload.log", encoding="utf-8", level=logging.DEBUG
    )
    logger.info(f"Starting upload of ICD-10, {datetime.now()}")
    session = SessionLocal()

    files_dir = get_dir_in_downloads(startswith="2018 Code", dir_path=".")

    for file in files_dir.iterdir():
        if "tabular" in file.name and "xml" in file.name:
            load_icd10_file(file.absolute())
    logging.info(f"Finished upload of ICD-10, {datetime.now()}")
