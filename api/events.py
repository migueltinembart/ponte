import logging
from typing import Dict, Literal, Any, Tuple
from uuid import uuid4
from fastapi import APIRouter
from pydantic import BaseModel
from pydantic.types import UUID4
from api.jobs import Job
from modules.github.models.webhook import PullRequestEvent
from modules.github.request import getPonteConfig
import queue
import threading
from loguru import logger


router = APIRouter(prefix="/events")

allowed_providers = Literal["github", "bitbucket"]

class Event(BaseModel):
    id: UUID4
    job: Job
    metadata: Dict[str, Any]

class WebHookData[T: Event](BaseModel):
    metadata: T

def get_config_from_github(event: Event):
    base_url: str = event.metadata['contents_url']
    ref: str = event.metadata['ref']
    
    config = getPonteConfig(base_url=base_url,ref=ref)
    logger.info(config)


@router.post("/{provider}")
def react_to_webhook(provider: allowed_providers, payload: PullRequestEvent | Any):
    if provider == "github":
        job_id: str = f"gh-{payload.pull_request.head.label}-{payload.pull_request.id}"

        webhookEvent: WebHookData[Event] = WebHookData(
            metadata=Event(
                id=uuid4(), 
                job=Job(id=uuid4(), status="registered", service=None), 
                metadata={
                    'job_id': job_id,
                    'ref': payload.pull_request.head.ref,
                    'contents_url': payload.pull_request.head.repo.contents_url
                }
            )
        )
        jobQueue.put(item=(job_id, webhookEvent))
        return {'status': "done"}
    return {'status': "failed"}

jobQueue: queue.Queue[Tuple[str, WebHookData]] = queue.Queue()

def initialize_threads() -> None:

    def process_job(job_id: str, data: WebHookData[Event]) -> None:
        logger.info(f"Started processing job {job_id} with event '{data}'")
        eventdata: Event = data.metadata
        get_config_from_github(event=eventdata)
        logger.info(f"Finished processing job {job_id}")

    def worker():
        while True:
            job_id, data = jobQueue.get()
            try:
                process_job(job_id, data)
            except Exception as e:
                print(f"Error processing job {job_id}: {e}")
            finally:
                jobQueue.task_done()

# Start the background worker thread when the application starts
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()


