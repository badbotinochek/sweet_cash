




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