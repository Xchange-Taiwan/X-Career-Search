import logging
import os

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src.config import exception
from src.db.session import get_db
from src.router.v1 import search

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

router_v1 = APIRouter(prefix="/search-service/api/v1")
router_v1.include_router(search.router)

app.include_router(router_v1)

exception.include_app(app)


@app.get("/search-service/{term}")
async def info(term: str):
    if term != "yolo":
        raise HTTPException(
            status_code=418, detail="Oops! Wrong phrase. Guess again?"
        )
    return JSONResponse(content={"mention": "You only live once."})


@app.get("/db/health")
async def db_connection_test(db: AsyncSession = Depends(get_db)):
    """
    DB connection test
    """
    try:
        await db.execute(
            text(
                'CREATE TABLE IF NOT EXISTS "user" (id SERIAL PRIMARY KEY,name VARCHAR)'
            )
        )
        await db.commit()

        logging.info("User table created successfully.")

        await db.execute(text('DROP TABLE "user"'))
        await db.commit()

        logging.info("User table dropped successfully.")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Database is not healthy")

    return JSONResponse(content={"message": "Database is healthy!"})


# Mangum Handler, this is so important
handler = Mangum(app)
