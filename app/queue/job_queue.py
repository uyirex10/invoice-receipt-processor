from queue import Queue

from app.utils.logger import get_logger


logger = get_logger(__name__)


class JobQueue:
    """
    Simple in-memory job queue.

    Responsibilities:
    - Store pending jobs
    - Provide jobs to workers

    This simulates production queue systems like:
    - Redis queues
    - RabbitMQ
    - Kafka
    """

    def __init__(self):
        self.queue = Queue()

    def enqueue(
        self,
        job_data: dict,
    ) -> None:

        logger.info(
            "Enqueuing processing job: %s",
            job_data,
        )

        self.queue.put(job_data)

    def dequeue(self) -> dict:

        job = self.queue.get()

        logger.info(
            "Dequeued processing job: %s",
            job,
        )

        return job

    def size(self) -> int:

        return self.queue.qsize()