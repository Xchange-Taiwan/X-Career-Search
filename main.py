from src.config.logging_config import init_logging
log = init_logging()

import os
import json
import asyncio
from mangum import Mangum
from fastapi import (
    FastAPI,
    status,
    Request,
    Header,
    Path,
    Query,
    Body,
    HTTPException,
    APIRouter,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.router.v1 import search, search_internal
from src.app._di.injection import (
    _resource_manager,
    _search_service,
    _index_initializer,
    PROFILES_INDEX_MAPPING,
)
from src.config import exception
from src.config.conf import PROFILE_INDEX_NAME

STAGE = os.environ.get("STAGE")
root_path = "/" if not STAGE else f"/{STAGE}"
app = FastAPI(title="X-Career: Search", root_path=root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # ensure OpenSearch index exists with the correct mapping
    await _index_initializer.ensure_index(PROFILE_INDEX_NAME, PROFILES_INDEX_MAPPING)

    # init global connection pool
    await _resource_manager.initial()
    asyncio.create_task(_resource_manager.keeping_probe())


@app.on_event("shutdown")
async def shutdown_event():
    # close connection pool
    await _resource_manager.close()


router_v1 = APIRouter(prefix="/search-service/api/v1")
router_v1.include_router(search.router)
router_v1.include_router(search_internal.router)

app.include_router(router_v1)

exception.include_app(app)


@app.get("/search-service/{term}")
async def info(term: str):
    print(term == "yolo")
    if term != "yolo":
        raise HTTPException(status_code=418, detail="Oops! Wrong phrase. Guess again?")
    return JSONResponse(content={"mention": "You only live once."})


_mangum = Mangum(app)


def handler(event, context):
    # SQS event source delivers a batch of records; route to the SQS handler
    # so we can ack successes and report partial failures back to Lambda.
    if (
        isinstance(event, dict)
        and isinstance(event.get("Records"), list)
        and event["Records"]
        and all(r.get("eventSource") == "aws:sqs" for r in event["Records"])
    ):
        return _handle_sqs_event(event)
    return _mangum(event, context)


def _handle_sqs_event(event):
    failures = []

    async def _process_all():
        for record in event["Records"]:
            try:
                body = json.loads(record["body"])
                await _search_service.subscribe_mentor_update(body)
            except Exception as e:
                log.error(
                    "[SQS] failed to process messageId=%s: %s",
                    record.get("messageId"),
                    e,
                )
                failures.append({"itemIdentifier": record["messageId"]})

    # Don't use asyncio.run() — on exit it calls events.set_event_loop(None)
    # and closes the loop. Once set_event_loop has been called even once on a
    # thread, Python 3.9's asyncio.get_event_loop() refuses to auto-create a
    # new loop and raises "RuntimeError: There is no current event loop in
    # thread 'MainThread'". Mangum.LifespanCycle.__init__ calls exactly that
    # function, so the *next* HTTP invocation in the same warm Lambda container
    # would 502 — and every subsequent HTTP invocation in that container too.
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("loop closed")
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(_process_all())
    return {"batchItemFailures": failures}
