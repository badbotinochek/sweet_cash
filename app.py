
from flask import Flask
from flask_jwt_extended import JWTManager
import logging

from db import db
from config import Config


logging.basicConfig(filename="logs.log",
                    level=logging.INFO,
                    format='%(levelname)s:%(name)s:%(asctime)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)


def create_app():
    # import errors
    import api.errors as error

    # import routes
    from api.routes.auth import auth_api
    from api.routes.transactions import transactions_api
    from api.routes.transaction_categories import transaction_categories_api
    from api.routes.transaction_types import transaction_types_api

    # db
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # jwt
    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY
    jwt = JWTManager(app)

    app.register_blueprint(auth_api)
    app.register_blueprint(transactions_api)
    app.register_blueprint(transaction_categories_api)
    app.register_blueprint(transaction_types_api)
    app.register_blueprint(error.blueprint)

    return app


if __name__ == '__main__':
    try:
        app = create_app()
        app.run(debug=True, host='0.0.0.0')
    except Exception as e:
        print(e)
