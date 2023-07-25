import networkx as nx
import nxontology


def load_snomed(path: str = "./app/graphs/snomed_nx.gpickle"):
    print(f"Loading SNOMED graph from {path}...")
    G_default = nx.read_gpickle(path)
    G = nxontology.NXOntology(G_default)
    G.freeze()
    return G


def load_icd10(path: str = "./app/graphs/icd10_nx.gpickle"):
    print(f"Loading ICD10 graph from {path}...")
    G_default = nx.read_gpickle(path)
    G = nxontology.NXOntology(G_default)
    G.freeze()
    return G
