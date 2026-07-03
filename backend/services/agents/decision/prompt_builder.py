from .prompt_templates import TEMPLATES
from .prompt_versions import PROMPT_VERSIONS, CURRENT_VERSION
from .context_builder import ContextBuilder
from .models import DecisionContext


class PromptBuilder:
    def __init__(self):
        self.context_builder = ContextBuilder()

    def build_prompt(
        self, context: DecisionContext, version: str = CURRENT_VERSION
    ) -> str:
        template_name = PROMPT_VERSIONS[version]["template_name"]
        template = TEMPLATES[template_name]
        context_str = self.context_builder.build(context)
        return template.format(context=context_str)
