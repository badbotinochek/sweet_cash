
from flask import Flask
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager

import config


engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)


def create_app():

    from api.routes.auth import auth_api

    app = Flask(__name__)
    app.config.from_object(config)
    jwt = JWTManager(app)

    @app.teardown_appcontext
    def shutdown_session(exseption=None):
        session.remove()

    app.register_blueprint(auth_api)

    return app


if __name__ == '__main__':
    try:
        app = create_app()
        app.run()
    except Exception as e:
        print(e)

"""
# Просмотр всех операций
@app.route('/costs', methods=['GET'])
@jwt_required()
def get_costs():
    costs = Costs.query.all()
    serialized = []
    for cost in costs:
        serialized.append({
            'id': cost.id,
            'category': cost.category,
            'amount': cost.amount,
            'description': cost.description,
            'date': cost.date,
            'type': cost.type
        })
    return jsonify(serialized)


# Добавление новой операции
@app.route('/costs', methods=['POST'])
@jwt_required()
def update_costs():
    new_one = Costs(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'category': new_one.category,
        'amount': new_one.amount,
        'description': new_one.description,
        'date': new_one.date,
        'type': new_one.type
    }
    return jsonify(serialized)


# Изменение операции
@app.route('/costs/<int:cost_id>', methods=['PUT'])
@jwt_required()
def change_cost(cost_id):
    item = Costs.query.filter(Costs.id == cost_id).first()
    params = request.json
    if not item:
        return {'message': 'Траты с таким номером не существует'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': item.id,
        'category': item.category,
        'amount': item.amount,
        'description': item.description,
        'date': item.date,
        'type': item.type
    }
    return jsonify(serialized)


# Удаление операции
@app.route('/costs/<int:cost_id>', methods=['DELETE'])
@jwt_required()
def delete_cost(cost_id):
    item = Costs.query.filter(Costs.id == cost_id).first()
    params = request.json
    if not item:
        return {'message': 'Траты с таким номером не существует'}, 400
    session.delete(item)
    session.commit()
    return '', 204


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}
"""



