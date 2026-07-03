from .models import Scenario, ScenarioConfig, ScenarioContext, ResourceAllocation


class ScenarioBuilder:
    def __init__(self, name):
        self.name = name
        self.context = ScenarioContext()
        self.resources = ResourceAllocation()

    def with_context_variable(self, k, v):
        self.context.variables[k] = v
        return self

    def with_resources(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self.resources, k, v)
        return self

    def build(self):
        config = ScenarioConfig(name=self.name, resources=self.resources)
        return Scenario(config=config, context=self.context)
