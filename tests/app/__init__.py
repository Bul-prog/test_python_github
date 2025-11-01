from flask import Flask
from .extensions import db


def create_app():
    app = Flask(__name__)

    # Пример конфигурации (для продакшена вынесите в config.py)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models  # Импорт моделей для регистрации с SQLAlchemy
        db.create_all()  # Создаем таблицы в БД, если их нет
    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    return app
