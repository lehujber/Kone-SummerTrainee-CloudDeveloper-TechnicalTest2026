import os
import sys
import pathlib
import pytest
from sqlalchemy import create_engine
from httpx import ASGITransport, AsyncClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("DATABASE_URI", "sqlite:///./test.db")

from api.src.persistence.sql import Base
from api.src.main import app


@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    db_path = pathlib.Path("test.db")
    try:
        db_path.unlink()
    except FileNotFoundError:
        pass

    engine = create_engine(os.environ["DATABASE_URI"])
    Base.metadata.create_all(engine)
    yield
    engine.dispose()
    try:
        db_path.unlink()
    except FileNotFoundError:
        pass


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac
