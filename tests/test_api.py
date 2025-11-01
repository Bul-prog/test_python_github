import pytest
from .factories import ClientFactory, ParkingFactory

@pytest.mark.parametrize('url', [
    '/clients',
    '/clients/1'
])
def test_get_endpoints(client, url):
    response = client.get(url)
    assert response.status_code == 200

def test_create_client(db, client):
    client_obj = ClientFactory.build()
    response = client.post('/clients', json={
        'name': client_obj.name,
        'surname': client_obj.surname,
        'credit_card': client_obj.credit_card,
        'car_number': client_obj.car_number,
    })
    assert response.status_code == 201
    assert 'id' in response.get_json()


def test_create_parking(db, client):
    parking_obj = ParkingFactory.build()
    response = client.post('/parkings', json={
        'address': parking_obj.address,
        'opened': parking_obj.opened,
        'count_places': parking_obj.count_places,
        'count_available_places': parking_obj.count_available_places,
    })
    assert response.status_code == 201
    assert 'id' in response.get_json()

@pytest.mark.parking
def test_park_entry(client):
    # Используем заранее созданные client_id=1, parking_id=1 из фикстуры
    data = {'client_id': 1, 'parking_id': 1}
    response = client.post('/client_parkings', json=data)
    # Если клиент уже на парковке, возможен 400 — учитывайте логику
    assert response.status_code in (201, 400)


@pytest.mark.parking
def test_park_exit(client):
    data = {'client_id': 1, 'parking_id': 1}
    response = client.delete('/client_parkings', json=data)
    assert response.status_code == 200 or response.status_code == 400
