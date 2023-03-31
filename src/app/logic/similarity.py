from nxontology import NXOntology
from sqlalchemy.orm import Session

from app.models.icd10.ICD9ToICD10Map import ICD9ToICD10Map
from app.schemas.similarity import SimilarityNode


def get_node_similarity(
    G: NXOntology,
    node_a: SimilarityNode,
    node_b: SimilarityNode,
    ic_metric: str,
):
    similarity = G.similarity(
        node_0=node_a.code, node_1=node_b.code, ic_metric=ic_metric
    )
    return similarity.results()


def node_set_similarity_jia(
    G: NXOntology,
    nodes_a: list[SimilarityNode],
    nodes_b: list[SimilarityNode],
    ic_metric: str,
    cs_metric: str,
):
    """Derived from https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-019-0807-y"""
    lhs = 0
    rhs = 0
    node_sim_ba = []
    node_sim_ab = []

    for node_a in nodes_a:
        code_a = node_a.code
        node_sim_ab = []
        for node_b in nodes_b:
            code_b = node_b.code
            similarity = G.similarity(code_a, code_b, ic_metric)
            similarity = getattr(similarity, cs_metric)
            similarity *= (node_a.weight + node_b.weight) / 2
            node_sim_ab.append(similarity)
        lhs += max(node_sim_ab, default=0)

    for node_b in nodes_b:
        code_b = node_b.code
        node_sim_ba = []
        for node_a in nodes_a:
            code_a = node_a.code
            similarity = G.similarity(code_b, code_a, ic_metric)
            similarity = getattr(similarity, cs_metric)
            similarity *= (node_a.weight + node_b.weight) / 2
            node_sim_ba.append(similarity)
        rhs += max(node_sim_ba, default=0)

    if len(node_sim_ab) == 0 or len(node_sim_ba) == 0:
        return 0

    factor = 1 / (len(node_sim_ab) + len(node_sim_ba))
    result = factor * (lhs + rhs)
    return result


def node_is_valid(G: NXOntology, node: str):
    result = True
    if node not in G.graph.nodes():
        result = False
    return result


def convert_i9_to_i10(db: Session, code: str):
    db_code = db.query(ICD9ToICD10Map).filter(ICD9ToICD10Map.icd9_code == code).first()
    if db_code is not None:
        return db_code.icd10_code
    else:
        return None


def get_valid_nodes(nodes: list[SimilarityNode], db: Session, G: NXOntology):
    valid_nodes = []
    for node in nodes:
        if node_is_valid(G, node.code):
            valid_nodes.append(node)
        else:
            code = convert_i9_to_i10(db=db, code=node.code)
            if code is not None and node_is_valid(G, code):
                node.code = code
                valid_nodes.append(node)
    return valid_nodes


def get_node_set_similarity(
    G: NXOntology,
    nodes_a: list[SimilarityNode],
    nodes_b: list[SimilarityNode],
    db: Session,
    ic_metric: str,
    cs_metric: str,
    method="jia",
):
    nodes_a = get_valid_nodes(db=db, nodes=nodes_a, G=G)
    nodes_b = get_valid_nodes(db=db, nodes=nodes_b, G=G)
    if method == "jia":
        result = node_set_similarity_jia(
            G=G,
            nodes_a=nodes_a,
            nodes_b=nodes_b,
            ic_metric=ic_metric,
            cs_metric=cs_metric,
        )
    return result
