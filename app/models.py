from .extensions import db
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    def __repr__(self):
        return f'<Client {self.name} {self.surname}>'


class Parking(db.Model):
    __tablename__ = 'parking'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Parking {self.address}>'


class ClientParking(db.Model):
    __tablename__ = 'client_parking'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime, default=datetime.utcnow)
    time_out = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),)

    client = db.relationship('Client', backref=db.backref('parkings', lazy=True))
    parking = db.relationship('Parking', backref=db.backref('clients', lazy=True))

    def __repr__(self):
        return f'<ClientParking client_id={self.client_id}, parking_id={self.parking_id}>'
