import functools
import inspect
import logging

from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config.conf import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    **settings.SQLALCHEMY_ENGINE_OPTIONS,
    echo=True,
    future=True
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


async def get_db():
    async with SessionLocal() as session:
        yield session


def managed_transaction(func):
    """
    wrap request in single transation
    """

    @functools.wraps(func)
    async def wrapper(*args, db: AsyncSession = Depends(get_db), **kwargs):
        try:
            if inspect.iscoroutinefunction(func):
                result = await func(*args, db=db, **kwargs)
            else:
                result = func(*args, db=db, **kwargs)
            await db.commit()
            return result
        except Exception:
            await db.rollback()
            raise

    return wrapper


# connect event on instance of Engine
@event.listens_for(engine.sync_engine, "connect")
def my_on_connect(dbapi_con, connection_record):
    logging.info("New DBAPI connection:", dbapi_con)
    cursor = dbapi_con.cursor()

    # sync style API use for adapted DBAPI connection / cursor
    cursor.execute("select 'execute from event'")
    logging.info(cursor.fetchone()[0])


## ORM events ##
# https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine
