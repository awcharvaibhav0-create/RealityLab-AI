class TemplateManager:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir

    def render(self, template_name: str, context: dict) -> str:
        """Mock template rendering"""
        return f"Rendered {template_name} with {context.get('title')}"
