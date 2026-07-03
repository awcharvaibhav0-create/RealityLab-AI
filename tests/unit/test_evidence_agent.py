from backend.services.agents.evidence.models import (
    Evidence,
    EvidenceSource,
    ConfidenceLevel,
)
from backend.services.agents.evidence.evidence_engine import EvidenceEngine
from backend.services.agents.evidence.evidence_agent import EvidenceAgent


def test_evidence_model_creation():
    source = EvidenceSource(source_id="1", agent_name="test_agent")
    ev = Evidence(evidence_id="ev_1", content="Test content", source=source)
    assert ev.evidence_id == "ev_1"
    assert ev.content == "Test content"
    assert ev.source.agent_name == "test_agent"
    assert ev.confidence == ConfidenceLevel.MEDIUM


def test_evidence_engine_processing():
    engine = EvidenceEngine()
    source = EvidenceSource(source_id="1", agent_name="test_agent")
    ev = Evidence(
        evidence_id="ev_1",
        content="Test content",
        source=source,
        confidence=ConfidenceLevel.HIGH,
    )
    assert engine.process_new_evidence(ev) == True

    ranked = engine.get_processed_evidence()
    assert len(ranked) == 1
    assert ranked[0].evidence_id == "ev_1"


def test_evidence_agent():
    agent = EvidenceAgent(agent_id="agent_1")
    success = agent.receive_evidence(
        content="The sky is blue",
        source_agent="weather_agent",
        evidence_id="ev_1",
        confidence=ConfidenceLevel.CERTAIN,
    )
    assert success == True

    state = agent.analyze_current_state()
    assert state["evidence_count"] == 1
    assert state["conflict_count"] == 0
    assert "The sky is blue" in state["report"]


def test_conflict_detection():
    engine = EvidenceEngine()
    source = EvidenceSource(source_id="1", agent_name="test_agent")
    ev1 = Evidence(evidence_id="ev_1", content="is true", source=source)
    ev2 = Evidence(evidence_id="ev_2", content="is false", source=source)
    engine.process_new_evidence(ev1)
    engine.process_new_evidence(ev2)

    conflicts = engine.get_conflicts()
    assert len(conflicts) == 1
