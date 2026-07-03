from backend.services.agents.decision.prompt_builder import PromptBuilder
from backend.services.agents.decision.models import DecisionContext


def test_prompt_builder():
    builder = PromptBuilder()
    context = DecisionContext(analysis_data={"key": "value"})

    prompt = builder.build_prompt(context)

    assert "value" in prompt
    assert "action" in prompt
    assert "confidence" in prompt
