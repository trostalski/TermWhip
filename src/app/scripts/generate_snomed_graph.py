# Description: Generate a graph of ICD10 codes and their relationships
import networkx as nx

from app.db.session import SessionLocal
from app.models.snomed.SnomedConcept import SnomedConcept
from app.models.snomed.SnomedRelationship import SnomedRelationship

IS_A = 116680003

if __name__ == "__main__":
    db = SessionLocal()
    G = nx.DiGraph()

    codes = db.query(SnomedConcept).all()
    relationships = db.query(SnomedRelationship).all()

    # for code in codes:
    #     if not code.active:
    #         continue
    #     G.add_node(code.id)

    for relationship in relationships:
        if not relationship.active == '1' or not relationship.typeId == IS_A:
            continue
        source = str(relationship.sourceId)
        target = str(relationship.destinationId)
        G.add_edge(target, source)

    print(f"Graph has {len(G.nodes)} nodes and {len(G.edges)} edges")
    nx.write_gpickle(G, "./app/graphs/snomed.gpickle")
    print("Saved graph to ./app/graphs/snomed.gpickle")
