from .models import ScenarioStatus, SimulationResult


class ScenarioSimulationEngine:
    def __init__(self):
        self.handlers = {}

    def register_execution_handler(self, name, handler):
        self.handlers[name] = handler

    def run_scenario(self, scenario, handler_name=None):
        if scenario.config.resources.cpu_cores > 50:
            return SimulationResult(
                scenario_id=scenario.id,
                status=ScenarioStatus.FAILED,
                output_state={},
                metrics={},
                error_message="Insufficient resources.",
            )
        if handler_name and handler_name in self.handlers:
            res = self.handlers[handler_name](scenario)
            return SimulationResult(
                scenario_id=scenario.id,
                status=ScenarioStatus.COMPLETED,
                output_state=res.get("state", {}),
                metrics=res.get("metrics", {}),
            )
        return SimulationResult(
            scenario_id=scenario.id,
            status=ScenarioStatus.COMPLETED,
            output_state={"time_series": [], "final_state": {}},
            metrics={},
        )
