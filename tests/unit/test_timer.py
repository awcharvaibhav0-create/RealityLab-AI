import time
from shared.utils.timer import Timer, timer_decorator


def test_timer_context_manager():
    with Timer() as t:
        time.sleep(0.01)

    assert t.elapsed > 0.0


def test_timer_decorator():
    @timer_decorator("test_func")
    def my_func():
        time.sleep(0.01)
        return "done"

    result = my_func()
    assert result == "done"
