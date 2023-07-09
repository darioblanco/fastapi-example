import json

from httpx import AsyncClient
from pytest import mark
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.space_agencies.api import crud
from tests.initialize import load_space_agencies

BASE_URL = "http://test"


# -- GET /space-agencies
async def test_list_space_agencies_comes_empty():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/api/v1/space-agencies")
        assert response.status_code == 200
        assert json.loads(response.content) == {"data": [], "count": 0}


async def test_list_space_agencies_returns_data(db_session: AsyncSession):
    await load_space_agencies(db_session)
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/api/v1/space-agencies?limit=5")
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["data"][0]["id"] == "a2db7679-1c0d-4e56-916c-fee0a431c1fa"
        assert data["data"][1]["id"] == "3d2bfdab-aca1-4b0c-8f62-4867aad0173f"
        assert data["data"][2]["id"] == "08d21955-51b6-44e5-83d3-adebb66e7ebd"
        assert data["data"][3]["id"] == "4d3fe717-fd2f-44f2-aa8e-8052f261c094"
        assert data["count"] == 4


async def test_list_space_agencies_returns_500(monkeypatch):
    async def mock_count_space_agencies(*args, **kwargs):
        raise Exception("a problem happened")

    monkeypatch.setattr(crud, "count_space_agencies", mock_count_space_agencies)

    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/api/v1/space-agencies")
        assert response.status_code == 500
        assert json.loads(response.content) == {
            "detail": "An unexpected error happened"
        }


# -- POST /space-agencies
@mark.parametrize(
    "name, status_code, data",
    [
        (
            "Create valid space agency",
            201,
            {
                "name": "GUASA",
                "description": "Spanish Space Agency",
                "website": "",
            },
        ),
    ],
)
async def test_post_space_agency_data(name, status_code, data):
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post("/api/v1/space-agencies", json=data)
    assert response.status_code == status_code


# -- GET /space-agencies/{space_agency_id}
async def test_get_space_agency_by_id_returns_404():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        url = "/api/v1/space-agencies/da380101-5a03-4dbc-8367-63f88e1ed235"
        response = await client.get(url)
        assert response.status_code == 404
        assert json.loads(response.content) == {
            "detail": "Space Agency not found"
        }


async def test_get_space_agency_by_id_returns_data(db_session: AsyncSession):
    await load_space_agencies(db_session)
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        url = "/api/v1/space-agencies/a2db7679-1c0d-4e56-916c-fee0a431c1fa"
        response = await client.get(url)
        assert response.status_code == 200
        result = json.loads(response.content)

        # The response contains:
        #  * data (with space agency's data)

        # ---------------------------------------
        assert "data" in result
        data_expected = {
            "name": "ESA",
            "description": (
                "The European Space Agency is an intergovernmental organisation of 22 member states dedicated to the exploration of space."
            ),
            "id": "a2db7679-1c0d-4e56-916c-fee0a431c1fa",
            "website": "https://www.esa.int",
        }
        for key in data_expected.keys():
            assert key in result["data"]
            assert data_expected[key] == result["data"][key]


# -- PUT /space-agencies/{space_agency_id}
space_agency_data = {
    "name": "Roscosmos",
    "description": "Edited description",
    "website": "https://www.roscosmos.ru",
}


async def test_update_space_agency_returns_404():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        url = f"/api/v1/space-agencies/23dde05f-1c94-46b6-8c42-4c64e0932fa3"
        response = await client.put(url, json=space_agency_data)
        assert response.status_code == 404
        assert json.loads(response.content) == {
            "detail": "Space Agency not found"
        }


async def test_update_space_agency_returns_updated_data(db_session):
    await load_space_agencies(db_session)
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        url = "/api/v1/space-agencies/08d21955-51b6-44e5-83d3-adebb66e7ebd"
        response = await client.put(url, json=space_agency_data)
        assert response.status_code == 200
        result = json.loads(response.content)
        assert result["name"] == "Roscosmos"


# -- DELETE /space-agencies/{space_agency_id}
async def test_delete_space_agency_returns_404():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        url = f"/api/v1/space-agencies/23dde05f-1c94-46b6-8c42-4c64e0932fa3"
        response = await client.delete(url)
        assert response.status_code == 404
        assert json.loads(response.content) == {
            "detail": "Space Agency not found"
        }


async def test_delete_space_agency_returns_204(db_session):
    await load_space_agencies(db_session)
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        url = f"/api/v1/space-agencies/08d21955-51b6-44e5-83d3-adebb66e7ebd"
        response = await client.delete(url)
        assert response.status_code == 204
