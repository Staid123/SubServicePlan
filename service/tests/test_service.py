
async def test_create_service(ac):
    response = await ac.post(
        url="/api/v1/service/",
        json={
            "name": "Hosting",
            "full_price": 1000
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Hosting",
        "full_price": 1000
    }

async def test_get_all_services(ac):
    response = await ac.get(
        url="/api/v1/service/all/"
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Hosting",
            "full_price": 1000
        }
    ]

async def test_get_service_by_id(ac):
    response = await ac.get(
        url="/api/v1/service/1/"
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Hosting",
        "full_price": 1000
    }

async def test_update_service(ac):
    response = await ac.patch(
        url="/api/v1/service/1/",
        json={
            "name": "Tech Support",
            "full_price": 999
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Tech Support",
        "full_price": 999
    }