import logging
import os
from datetime import datetime

import pytz
from fastapi import FastAPI, HTTPException, Request, status

from app.space_agencies.api import router as space_agencies_router

# from app.launching_sites.api import router as launching_sites_router
# from app.satellites.api import router as satellites_router

tags_metadata = [
    {
        "name": "Space Agencies",
        "description": "Create, read, list, update and delete space agencies.",
    },
    # {
    #     "name": "Launching Sites",
    #     "description": "Create, read, list, update and delete launching sites.",
    # },
    # {
    #     "name": "Satellites",
    #     "description": "Create, read, list, update and delete satellites.",
    # },
]


readyness_file_path = "/tmp/fastapi-example.txt"

app = FastAPI(
    title="Satellites API Service",
    version="0.1.0",
    openapi_tags=tags_metadata,
)


@app.on_event("startup")
def startup_event():
    fmt = (
        "%(asctime)s %(name)-15s %(levelname)-7s "
        "%(filename)s:%(funcName)s():L%(lineno)s %(message)s"
    )
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL"), format=fmt, datefmt="%Y-%m-%d %H:%M:%S"
    )
    readyness_file = open(readyness_file_path, "w")
    tstamp = datetime.now().replace(tzinfo=pytz.UTC)
    line = f"{tstamp.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    readyness_file.write(f"{line}: Service is ready.\n")
    readyness_file.close()


@app.on_event("shutdown")
def shutdown_event():
    if os.path.exists(readyness_file_path):
        os.remove(readyness_file_path)


app.include_router(space_agencies_router, tags=["Space Agencies"])
# app.include_router(launching_sites_router, tags=["Launching Sites"])
# app.include_router(satellites_router, tags=["Satellites"])


@app.get("/")
@app.get("/health")
def main():
    return {"status": "ok"}


# --------------------------------------
# Catch all get requests intended to hit
# the API but without endpoint defined.


@app.get("/{catchall:path}")
def api_catchall_gets(request: Request):
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Method Not Allowed",
    )
