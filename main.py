import os
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
    _queue_adapter,
    _dlq_adapter,
    _search_service,
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
    # init global connection pool
    await _resource_manager.initial()
    asyncio.create_task(_resource_manager.keeping_probe())

    # subscribe messages(SQS)
    asyncio.create_task(
        _queue_adapter.subscribe_messages(
            _search_service.subscribe_mentor_update,
        )
    )
    # subscribe DLQ messages(SQS)
    asyncio.create_task(
        _dlq_adapter.subscribe_messages(
            _search_service.subscribe_mentor_update,
        )
    )


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


# Mangum Handler, this is so important
handler = Mangum(app)
