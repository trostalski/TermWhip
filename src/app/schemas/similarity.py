from pydantic import BaseModel, validator
from typing import List, Optional


class SimilarityNode(BaseModel):
    code: str
    weight: Optional[float] = 1.0

    class Config:
        validate_assignment = True

    @validator("weight")
    def set_weight(cls, v):
        return v or 1.0


class NodePairSimilarityIn(BaseModel):
    node_a: SimilarityNode
    node_b: SimilarityNode
    ic_metric: Optional[str] = "intrinsic_ic_sanchez"


class NodeSetSimilarityIn(BaseModel):
    nodes_a: List[SimilarityNode]
    nodes_b: List[SimilarityNode]
    cs_metric: Optional[str] = "lin"
    ic_metric: Optional[str] = "intrinsic_ic_sanchez"


class ConceptSimilarityOut(BaseModel):
    node_a: str
    node_b: str
    node_a_subsumes_b: bool
    node_b_subsumes_a: bool
    depth: int
    n_common_ancestors: int
    n_union_ancestors: int
    batet: float
    batet_log: float
    ic_metric: str
    mica: str
    resnik: float
    resnik_scaled: float
    lin: float
    jiang: float
    jiang_seco: float
