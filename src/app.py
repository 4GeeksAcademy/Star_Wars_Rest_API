"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Users
@app.route('/users', methods=['GET'])
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_users(user_id=None):
    if user_id is None:
        users = User.query.all()
        return jsonify([x.serialize() for x in users]), 200

    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        return jsonify(user.serialize()), 200

    return jsonify({"msg": "Request not valid"}), 400


# Favorites
@app.route('/users/<int:user_id>/favorites', methods=['GET', 'POST', 'DELETE'])
def handle_favorites(user_id=None):
    if user_id is None:
        return jsonify({"msg": "This endpoint needs a user_id"}), 400

    if request.method == 'GET':
        favorites = Favorite.query.filter_by(id=user_id).all()
        return jsonify([x.serialize() for x in favorites]), 200

    if request.method == 'POST':
        body = json.loads(request.data)

        category_id = Category.query.filter_by(
            category_name=body['category_name']).first()

        if category_id is None:
            return jsonify({"msg": f"{body['category_name']} is not a valid category"}), 400

        favorite = Favorite(
            user_id=user_id,
            category_id=category_id.id,
            category_fk_id=body['category_fk_id']
        )

        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            "msg": f"Favorite added",
            "inserted_id": f"{favorite.id}"
        }), 200

    if request.method == 'DELETE':
        body = json.loads(request.data)

        category = Category.query.filter_by(
            category_name=body['category_name']).first()

        if category is None:
            return jsonify({"msg": f"{body['category_name']} is not a category"}), 400

        db.session.delete(category)
        db.session.commit()

        return jsonify({
            "msg": f"Category deleted",
            "deleted_id": f"{category.id}"
        }), 200

    return jsonify({"msg": f"{request.method}: Request not valid"}), 400


# Characters
@app.route('/characters', methods=['GET'])
@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_characters(character_id=None):
    if character_id is None:
        characters = Character.query.all()
        characters = [x.serialize() for x in characters]
        return jsonify(characters), 200

    character = Character.query.filter_by(id=character_id).first()
    if character is not None:
        return jsonify(character.serialize()), 200

    return jsonify({"msg": "Request not valid"}), 400


# Planets
@app.route('/planets', methods=['GET'])
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planets(planet_id=None):
    if planet_id is None:
        planets = Planet.query.all()
        planets = [x.serialize() for x in planets]
        return jsonify(planets), 200

    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is not None:
        return jsonify(planet.serialize()), 200

    return jsonify({"msg": "Request not valid"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
