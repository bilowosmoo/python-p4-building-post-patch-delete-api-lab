#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET/POST/PATCH/DELETE API</h1>'

# ---------------- GET ROUTES ----------------
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries]), 200

@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([good.to_dict() for good in goods]), 200

@app.route('/baked_goods/most_expensive')
def most_expensive():
    item = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(item.to_dict()), 200

# ---------------- POST ROUTE ----------------
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    try:
        new_good = BakedGood(
            name=data['name'],
            price=float(data['price']),
            bakery_id=int(data['bakery_id'])
        )
        db.session.add(new_good)
        db.session.commit()
        return jsonify(new_good.to_dict()), 201
    except Exception as e:
        return make_response({'error': str(e)}, 400)

# ---------------- PATCH ROUTE ----------------
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    data = request.form
    if 'name' in data:
        bakery.name = data['name']
    db.session.commit()
    return jsonify(bakery.to_dict()), 200

# ---------------- DELETE ROUTE ----------------
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    good = BakedGood.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()
    return jsonify({'message': 'Baked good deleted successfully.'}), 200

# Run server
if __name__ == '__main__':
    app.run(port=5555, debug=True)
