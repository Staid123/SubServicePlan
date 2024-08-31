

async def test_create_plan(ac):
    response = await ac.post(
        url="/plan/",
        json={
            "plan_type": "full",
            "discount_percent": 0
        }
    )
    assert response.status_code == 201, "Bad status code"
    assert response.json() == {
            "id": 1,
            "plan_type": "full",
            "discount_percent": 0
        }