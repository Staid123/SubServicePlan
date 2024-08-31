
import pytest
from conftest import client


def test_create_plan():
    response = client.post(
        url="/api/v1/plan/",
        json={
            "plan_type": "full",
            "discount_percent": 0
        }
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {
            "id": 1,
            "plan_type": "full",
            "discount_percent": 0
        }
    
@pytest.mark.asyncio
async def test_get_all_plans(ac):
    response = await ac.get(url="/api/v1/plan/all/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "plan_type": "full",
            "discount_percent": 0
        }
    ]

@pytest.mark.asyncio
async def test_get_plan_by_id(ac):
    response = await ac.get(url="/api/v1/plan/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "plan_type": "full",
        "discount_percent": 0
    }

@pytest.mark.asyncio
async def test_update_plan(ac):
    response = await ac.patch(
        url="/api/v1/plan/1/", 
        json={
            "discount_percent": 1
        }
    )
    assert response.status_code == 200
    assert response.json() ==  {
        "id": 1,
        "plan_type": "full",
        "discount_percent": 1
    }
