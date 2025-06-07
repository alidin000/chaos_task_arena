import redis
from chaos_tasks import chaos_task, r

def test_task_success():
    r.set("success", 0)
    result = chaos_task.apply(args=["job_123", 1.0])
    assert result.successful()
    assert b"done" in result.result.encode()
    assert int(r.get("success")) >= 1

def test_task_failure_after_retries():
    r.set("failed", 0)
    try:
        chaos_task.apply(args=["job_fail", 0.0])
    except Exception:
        pass
    assert int(r.get("failed")) >= 1
