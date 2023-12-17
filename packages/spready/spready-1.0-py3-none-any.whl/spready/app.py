#!/usr/bin/env python
import os
from redis import Redis
import logging
from rq import Worker


# logger = logging.getLogger("rq.worker")
# logger.propagate = False
# logger.disabled = True

appLogger = logging.getLogger("app")
appLogger.log(10, "Starting worker")


def run(host, port, db, password, modulePath="."):
    conn = Redis(
        host=host,
        port=port,
        db=db,
        password=password,
    )
    os.environ["SPREADY_MODULES"] = modulePath

    # Provide the worker with the list of queues (str) to listen to.
    w = Worker(["myjob"], connection=conn, log_job_description=False)
    w.work()

if __name__ == "__main__":
    run(
        os.getenv("REDIS_HOST"),
        os.getenv("REDIS_PORT"),
        0,
        os.getenv("REDIS_PASSWORD"),
    )   