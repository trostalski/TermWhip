from sqlalchemy.orm import Session

from app.schemas.icd10 import ICD10CodeOut
from app.models.icd10.ICD10Code import ICD10Code
from app.models.icd10.ICD10Group import ICD10Group
from app.models.icd10.ICD10Chapter import ICD10Chapter

from nxontology import NXOntology


def get_children_for_code(code: str, G: NXOntology):
    children = G.graph.successors(code)
    children = list(children)
    return children


def get_parent_for_code(code: str, G: NXOntology):
    result = ""
    parent = list(G.graph.predecessors(code))
    if len(parent) > 0:
        result = parent[0]
    return result


def get_code(db: Session, code: str, G: NXOntology):
    code_data = db.get(ICD10Code, code)
    group_data = db.get(ICD10Group, code_data.group_id)
    chapter_data = db.get(ICD10Chapter, code_data.chapter_id)

    children = get_children_for_code(code, G)
    parent = get_parent_for_code(code, G)

    return ICD10CodeOut(
        code=code_data.code,
        description=code_data.description,
        chapter_code=chapter_data.chapter_code,
        chapter_description=chapter_data.description,
        group_code=group_data.group_code,
        group_description=group_data.description,
        children=children,
        parent=parent,
    )
