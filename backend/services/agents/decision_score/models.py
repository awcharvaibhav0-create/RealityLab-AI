from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class ScenarioOutput:
    scenario_id: str
    strategy_id: str
    metrics: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass
class NormalizedScore:
    scenario_id: str
    strategy_id: str
    normalized_metrics: Dict[str, float]
    confidence: float


@dataclass
class CompositeScore:
    strategy_id: str
    total_score: float
    component_scores: Dict[str, float]
    overall_confidence: float


@dataclass
class StrategyRanking:
    strategy_id: str
    rank: int
    score: CompositeScore
    is_tie: bool = False


@dataclass
class Recommendation:
    recommended_strategy_id: str
    rankings: List[StrategyRanking]
    rationale: str
