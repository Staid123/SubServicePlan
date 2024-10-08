

async def test_create_plan(ac):
    response = await ac.post(
        url="/api/v1/plan/",
        json={
            "plan_type": "full",
            "discount_percent": 0
        }
    )
    assert response.status_code == 201
    assert response.json() == {
            "id": 1,
            "plan_type": "full",
            "discount_percent": 0
        }
    
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

async def test_get_plan_by_id(ac):
    response = await ac.get(url="/api/v1/plan/1/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "plan_type": "full",
        "discount_percent": 0
    }

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
