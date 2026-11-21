import os
import time
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger("sql_profiler")
logger.setLevel(logging.INFO)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lab7.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.perf_counter())
    conn.info["query_count"] = conn.info.get("query_count", 0) + 1


@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    start_times = conn.info.get("query_start_time", [])
    if start_times:
        elapsed_ms = (time.perf_counter() - start_times.pop()) * 1000
        logger.info(f"[{elapsed_ms:.2f} ms] {statement}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
