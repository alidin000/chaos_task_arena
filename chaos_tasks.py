# celery tasks will be created here
from celery import Celery
from celery.exceptions import Retry
import redis

import random

r = redis.Redis()
app = Celery('chaos_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3)
def chaos_task(self, job_id, succes_chance):
    if random.random() < succes_chance:
        if self.request.retries >= self.max_retries:
            r.incr("failed")
        else:
            r.incr("retry")
        raise self.retry(countdown=2 ** self.request.retries)
    r.incr("success")
    return f"{job_id} succeeded"