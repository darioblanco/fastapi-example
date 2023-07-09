import subprocess
from unittest.mock import MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from app.scripts import load_data
from app.space_agencies import crud
from tests.initialize import TestingSessionLocal


# ---------------------------------------------------------------------
async def test_load_data_from_cmd_line(db_session: AsyncSession):
    count_before = await crud.count_space_agencies(db_session)
    assert count_before == 0
    subprocess.run(
        ["poetry", "run", "python", "-m", "app.scripts.load_data"],
        capture_output=True,
    )
    count_after = await crud.count_space_agencies(db_session)
    assert count_after == 4


# ---------------------------------------------------------------------
_mocked_loop = None


def mock_new_event_loop():
    global _mocked_loop
    _mocked_loop = MagicMock()
    return _mocked_loop


def test_run(monkeypatch):
    monkeypatch.setattr(
        load_data.asyncio, "new_event_loop", mock_new_event_loop
    )
    load_data.run()
    assert _mocked_loop.has_been_called()
    assert _mocked_loop.called_with(load_data.populate_space_agencies)


# ---------------------------------------------------------------------
async def test_populate_space_agencies():
    async with TestingSessionLocal() as session:
        count_before = await crud.count_space_agencies(session)
        assert count_before == 0
        await load_data.populate_space_agencies(verbose=False)
        count_after = await crud.count_space_agencies(session)
        assert count_after == 4
