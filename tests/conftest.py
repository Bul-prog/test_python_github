import pytest
from app import create_app, db as _db
from app.models import Client, Parking, ClientParking
from sqlalchemy import func

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        _db.create_all()

        # Создаем тестовые данные
        client = Client(name='Test', surname='User', credit_card='1234567890123456', car_number='ABC123')
        parking = Parking(address='Test Address', opened=True, count_places=10, count_available_places=10)
        _db.session.add_all([client, parking])
        _db.session.commit()

        # Создаем лог заезда-выезда (заезд сейчас, выезд через час)
        client_parking = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=func.now(),
            time_out=None
        )
        _db.session.add(client_parking)
        _db.session.commit()

    yield app

    # Очистка БД после тестов
    with app.app_context():
        _db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    return _db
