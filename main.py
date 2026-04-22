from src.config.logging_config import init_logging
log = init_logging()

import asyncio
import json
import os
from typing import Any, Dict, List

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
    _search_service,
    _index_initializer,
    PROFILES_INDEX_MAPPING,
)
from src.config import exception

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
    await _index_initializer.ensure_index("profiles", PROFILES_INDEX_MAPPING)


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


# ── SQS event source mapping handler ─────────────────────────────────────────
# 當 AWS 透過 SQS event source mapping 觸發時，event["Records"][0]["eventSource"]
# 會是 "aws:sqs"，與 API Gateway event 的結構完全不同，Mangum 無法處理。
# 在同一個 Lambda function 裡做 dispatch，保持 Lambda 數量不變。

async def _handle_sqs_async(event: Dict[str, Any]) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = event.get("Records", []) or []
    batch_item_failures: List[Dict[str, str]] = []

    for record in records:
        message_id = record.get("messageId")
        try:
            body = record.get("body")
            if not body:
                raise ValueError(f"empty SQS record body, messageId={message_id}")
            payload: Dict[str, Any] = json.loads(body)
            await _search_service.subscribe_mentor_update(payload)
        except Exception as e:
            log.error(
                "[SQS] failed to process messageId=%s: %s", message_id, str(e)
            )
            if message_id:
                batch_item_failures.append({"itemIdentifier": message_id})

    return {"batchItemFailures": batch_item_failures}


_mangum_handler = Mangum(app)


def handler(event: Dict[str, Any], context: Any) -> Any:
    records = event.get("Records")
    if records and records[0].get("eventSource") == "aws:sqs":
        return asyncio.run(_handle_sqs_async(event))
    return _mangum_handler(event, context)
