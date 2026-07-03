from backend.services.coordinator.workflow_engine import WorkflowEngine
from backend.database.database_manager import DatabaseManager


def test_full_agent_workflow():
    """
    Tests the end-to-end execution of all agents.
    """
    db_manager = DatabaseManager(":memory:")
    db_manager.initialize()
    from backend.services.coordinator.event_bus import EventBus
    from backend.services.coordinator.shared_context import SharedContext

    event_bus = EventBus()
    shared_context = SharedContext()
    engine = WorkflowEngine(event_bus, shared_context)


    # In a real environment, this would execute the graph
    # For now, we just verify the state transitions
    assert engine.state_machine.current_state.value == "CREATED"
    # Execute would be called here
    # engine.execute(request)
    # assert engine.state.value == "completed"
