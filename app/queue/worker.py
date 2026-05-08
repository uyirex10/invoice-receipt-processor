import threading
import time

from app.utils.logger import get_logger


logger = get_logger(__name__)


class BackgroundWorker:
    """
    Background job worker.

    Responsibilities:
    - Continuously process jobs
    - Run invoice processing asynchronously
    """

    def __init__(
        self,
        job_queue,
        invoice_processing_service,
    ):
        self.job_queue = job_queue
        self.invoice_processing_service = (
            invoice_processing_service
        )

        self.running = False

    def start(self) -> None:

        logger.info("Starting background worker.")

        self.running = True

        worker_thread = threading.Thread(
            target=self.run,
            daemon=True,
        )

        worker_thread.start()

    def stop(self) -> None:

        logger.info("Stopping background worker.")

        self.running = False

    def run(self) -> None:

        while self.running:

            try:

                if self.job_queue.size() == 0:
                    time.sleep(1)
                    continue

                job = self.job_queue.dequeue()

                logger.info(
                    "Processing background job: %s",
                    job,
                )

                self.invoice_processing_service.process_invoice(
                    document_id=job["document_id"],
                    file_path=job["file_path"],
                )

                logger.info(
                    "Background job completed successfully."
                )

            except Exception as error:

                logger.error(
                    "Background worker failed: %s",
                    error,
                )