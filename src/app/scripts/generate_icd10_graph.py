# Description: Generate a graph of ICD10 codes and their relationships
import networkx as nx

from app.db.session import SessionLocal
from app.models.icd10.ICD10Code import ICD10Code


if __name__ == "__main__":
    db = SessionLocal()
    G = nx.DiGraph()

    # Add nodes
    codes = db.query(ICD10Code).all()
    for code in codes:
        G.add_node(code.code)

    # Add edges
    for code in codes:
        parent_code = code.code[: len(code.code) - 1]
        if parent_code in G.nodes:
            G.add_edge(parent_code, code.code)

    # Save graph
    nx.write_gpickle(G, "./app/graphs/icd10_nx.gpickle")
    print("Saved graph to ./app/graphs/icd10_nx.gpickle")
