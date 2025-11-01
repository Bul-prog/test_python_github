from flask import Blueprint, request, jsonify, abort
from .models import db, Client, Parking, ClientParking

from sqlalchemy import func


bp = Blueprint('api', __name__)


@bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'surname': c.surname,
        'credit_card': c.credit_card,
        'car_number': c.car_number
    } for c in clients])


@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'name': client.name,
        'surname': client.surname,
        'credit_card': client.credit_card,
        'car_number': client.car_number
    })


@bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    required_fields = ['name', 'surname', 'car_number']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Ошибка': 'Отсутствуют обязательные поля'}), 400

    new_client = Client(
        name=data['name'],
        surname=data['surname'],
        credit_card=data.get('credit_card'),
        car_number=data['car_number']
    )
    db.session.add(new_client)
    db.session.commit()

    return jsonify({'id': new_client.id}), 201


@bp.route('/parkings', methods=['POST'])
def create_parking():
    data = request.get_json()
    required_fields = ['address', 'opened', 'count_places', 'count_available_places']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'Ошибка': 'Отсутствуют обязательные поля'}), 400

    parking = Parking(
        address=data['address'],
        opened=data['opened'],
        count_places=data['count_places'],
        count_available_places=data['count_available_places']
    )
    db.session.add(parking)
    db.session.commit()

    return jsonify({'id': parking.id}), 201


@bp.route('/client_parkings', methods=['POST'])
def park_entry():
    data = request.get_json()
    if not data or 'client_id' not in data or 'parking_id' not in data:
        return jsonify({'Ошибка': 'Отсутствует идентификатор клиента или идентификатор парковки'}), 400

    client = Client.query.get(data['client_id'])
    parking = Parking.query.get(data['parking_id'])
    if not client or not parking:
        return jsonify({'Ошибка': 'Клиент или парковка не найдены'}), 404

    if not parking.opened:
        return jsonify({'Ошибка': 'Парковка закрыта'}), 400

    if parking.count_available_places <= 0:
        return jsonify({'Ошибка': 'Свободных мест нет'}), 400

    # Проверим, что у клиента нет активной парковки на этой парковке
    active_park = ClientParking.query.filter_by(
        client_id=client.id, parking_id=parking.id, time_out=None).first()
    if active_park:
        return jsonify({'Ошибка': 'Клиент уже припарковался здесь'}), 400

    # Создаем запись заезда
    client_parking = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=func.now()
    )
    parking.count_available_places -= 1

    db.session.add(client_parking)
    db.session.commit()

    return jsonify({'Сообщение': 'Запись создана'}), 201


@bp.route('/client_parkings', methods=['DELETE'])
def park_exit():
    data = request.get_json()
    if not data or 'client_id' not in data or 'parking_id' not in data:
        return jsonify({'Ошибка': 'Отсутствует идентификатор клиента или идентификатор парковки'}), 400

    client = Client.query.get(data['client_id'])
    parking = Parking.query.get(data['parking_id'])
    if not client or not parking:
        return jsonify({'Ошибка': 'Клиент или парковка не найдены'}), 404

    if not client.credit_card:
        return jsonify({'Ошибка': 'У клиента нет привязанной кредитной карты'}), 400

    # Ищем активную парковку (без time_out)
    active_park = ClientParking.query.filter_by(
        client_id=client.id, parking_id=parking.id, time_out=None).first()
    if not active_park:
        return jsonify({'Ошибка': 'Для клиента не найдено активной парковки'}), 400

    active_park.time_out = func.now()
    parking.count_available_places += 1

    # Здесь можно добавить логику списания средств с карты (эмуляция)
    # Например: charge_client(client.credit_card, calculate_fee(active_park))

    db.session.commit()

    return jsonify({'Сообщение': 'Регистрация выхода и обработка платежа'})
