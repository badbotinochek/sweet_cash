
from flask import Flask
from flask_jwt_extended import JWTManager
import logging

from db import db
from config import Config
from api.services.notification_processing.notification_processor import NotificationProcessor
from message_queue import MessageQueue


logging.basicConfig(filename="../logs.log",
                    level=logging.INFO,
                    format='%(levelname)s:%(name)s:%(asctime)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)

messages_queue = MessageQueue()


def create_app():
    # import errors
    import api.errors as error

    # import routes
    from api.routes.auth import auth_api
    from api.routes.transactions import transactions_api
    from api.routes.transaction_categories import transaction_categories_api
    from api.routes.external_auth import external_auth_api
    from api.routes.receipts import receipts_api

    # db
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # jwt
    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY
    jwt = JWTManager(app)

    app.register_blueprint(auth_api)
    app.register_blueprint(transactions_api)
    app.register_blueprint(transaction_categories_api)
    app.register_blueprint(external_auth_api)
    app.register_blueprint(receipts_api)
    app.register_blueprint(error.blueprint)

    # Run notification processing
    processors_names = ['Processor-1']  # TODO в config
    processors = [NotificationProcessor(name=name, q=messages_queue) for name in processors_names]
    for processor in processors:
        processor.start()

    return app


if __name__ == '__main__':
    try:
        app = create_app()
        app.run(debug=True)  # , host='0.0.0.0')  # TODO  debug to config
    except Exception as e:
        print(e)
