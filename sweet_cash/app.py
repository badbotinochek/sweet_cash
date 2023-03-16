from flask import Flask
from flask_jwt_extended import JWTManager
import logging
import redis

from sweet_cash.db import db
from sweet_cash.config import Config
from sweet_cash.api.services.notification_processing.notification_processor import NotificationProcessor
from sweet_cash.message_queue import MessageQueue

logging.basicConfig(filename="logs.log",
                    level=logging.INFO,
                    format='%(levelname)s:%(name)s:%(asctime)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

messages_queue = MessageQueue()

redis = redis.Redis(Config.REDIS_HOST,
                    Config.REDIS_PORT,
                    Config.REDIS_DB,
                    Config.REDIS_PASSWORD)


def create_app():
    # db
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # with app.app_context():
    #     db.create_all()
    #     db.session.commit()

    # import errors
    import sweet_cash.api.errors as error
    # import routes
    from sweet_cash.api.routes.auth import auth_api
    from sweet_cash.api.routes.transactions import transactions_api
    from sweet_cash.api.routes.external_auth import external_auth_api
    from sweet_cash.api.routes.receipts import receipts_api
    from sweet_cash.api.routes.events import events_api
    from sweet_cash.api.routes.views import views_api

    app.register_blueprint(auth_api)
    app.register_blueprint(transactions_api)
    app.register_blueprint(external_auth_api)
    app.register_blueprint(receipts_api)
    app.register_blueprint(events_api)
    app.register_blueprint(error.blueprint)
    app.register_blueprint(views_api)

    # jwt
    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY
    jwt = JWTManager(app)

    # Run notification processing
    processors_names = Config.EVENT_PROCESSORS
    processors = [NotificationProcessor(name=name, q=messages_queue) for name in processors_names]
    for processor in processors:
        processor.start()

    return app


create_app()
with app.app_context():
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    try:
        # app = create_app()
        app.run(debug=Config.DEBUG, host='0.0.0.0')
    except Exception as e:
        print(e)
