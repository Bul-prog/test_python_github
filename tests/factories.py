import factory
from faker import Faker
from app.models import Client, Parking

fake = Faker()

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = None  # будет подставлен при вызове из фикстуры

    name = factory.LazyAttribute(lambda _: fake.first_name())
    surname = factory.LazyAttribute(lambda _: fake.last_name())
    credit_card = factory.LazyAttribute(lambda _: fake.credit_card_number() if fake.boolean() else None)
    car_number = factory.LazyAttribute(lambda _: fake.bothify(text='???-####'))


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = None  # будет подставлен при вызове из фикстуры

    address = factory.LazyAttribute(lambda _: fake.address())
    opened = factory.LazyAttribute(lambda _: fake.boolean())
    count_places = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))
    count_available_places = factory.LazyAttribute(lambda o: o.count_places)
