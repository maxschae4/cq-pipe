import os

from cq_pipe.celery import app
from cq_pipe.fetch import fetch_hosts

# This isn't the best place for loading, we should leverage the celery worker_init signal
# and we should probably create a config object instead of loading globals
API_TOKEN = os.getenv("API_TOKEN", "")
API_URL = os.getenv("API_URL", "")
CROWDSTRIKE_ENDPOINT = os.getenv("CROWDSTRIKE_ENDPOINT", "")
QUALYS_ENDPOINT = os.getenv("QUALYS_ENDPOINT", "")


@app.task
def extract_crowdstrike_hosts() -> None:
    """
    Control loop for fetching all hosts from a crowdstrike endpoint and generating tasks

    Defined as a celery task so we can leverage celery beat to schedule execution
    """
    endpoint = f"{API_URL}/{CROWDSTRIKE_ENDPOINT}"
    # limit is 1 due to the behavior of the API when the final request is made.
    # while 2 is the allowed limit, an odd number of records cannot be retrieved using a limit of 2
    # this is another opportunity for optimization should the need arise.
    for batch in fetch_hosts(endpoint, API_TOKEN, limit=1):
        for host in batch:
            # this generates a chain of tasks to act on each host in each batch
            chain = transform_crowdstrike_host.s(host) | load_host.s()
            chain()


@app.task
def extract_qualys_hosts() -> None:
    """
    Control loop for fetching all hosts from a qualys endpoint and generating tasks

    Defined as a celery task so we can leverage celery beat to schedule execution
    """
    endpoint = f"{API_URL}/{QUALYS_ENDPOINT}"
    # limit is 1 due to the behavior of the API when the final request is made.
    # while 2 is the allowed limit, an odd number of records cannot be retrieved using a limit of 2
    # this is another opportunity for optimization should the need arise.
    for batch in fetch_hosts(endpoint, API_TOKEN, limit=1):
        for host in batch:
            chain = transform_qualys_host.s(host) | load_host.s()
            chain()


@app.task
def transform_crowdstrike_host(host) -> dict:
    """
    Stub entry for transforming the crowdstrike host into our defined model
    """
    return host


@app.task
def transform_qualys_host(host):
    """
    Stub entry for transforming the qualys host into our defined model
    """
    return host


@app.task
def load_host(host):
    """
    Stub entry for loading hosts into mongo
    """
    pass
