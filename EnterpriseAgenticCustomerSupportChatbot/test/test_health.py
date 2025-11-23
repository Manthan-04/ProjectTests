from httpx import AsyncClient
import pytest

# To run below tests use command: pytest -q

@pytest.mark.asyncio
async def test_helth():
    async with AsyncClient(base_url="http://127.0.0.1:8000/api/v1") as client:
        res = await client.get('/health')
        assert res.status_code == 200
        assert res.json() == {'status': 'ok.'}

@pytest.mark.asyncio
async def test_chat():
    async with AsyncClient(base_url="http://127.0.0.1:8000/api/v1") as client:
        res = await client.post('/chat', json={"userName": "Manthan Phadse","message": "Hi."})
        assert res.status_code == 200
        assert res.json() == {"status": "ok","body": {"userName": "Manthan Phadse","message": "Hi."}}