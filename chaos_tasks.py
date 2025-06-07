import os
import logging
from celery import Celery
from celery.exceptions import Retry
import redis
import random

r = redis.Redis()
app = Celery('chaos_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs/chaos_tasks.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


@app.task(bind=True, max_retries=3)
def chaos_task(self, job_id, succes_chance):
    logger.info(f"Starting job {job_id} with success chance {succes_chance}")
    try:
        if random.random() < succes_chance:
            if self.request.retries >= self.max_retries:
                r.incr("failed")
                logger.error(f"Job {job_id} failed after {self.request.retries} retries")
            else:
                r.incr("retry")
                logger.warning(f"Job {job_id} retry {self.request.retries + 1}")
            raise self.retry(countdown=2 ** self.request.retries)
        r.incr("success")
        logger.info(f"Job {job_id} succeeded")
        return f"{job_id} succeeded"
    except Retry:
        raise
    except Exception as e:
        logger.error(f"Job {job_id} error: {e}")
        raise
