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

# Get all the users
@app.route('/users', methods=['GET'])
def handle_users_all():
   
    users = User.query.all()
    return jsonify(users), 200

# Get one specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def handle_users(user_id):

    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        return jsonify(user.serialize()), 200

    return jsonify({"msg": "Request not valid"}), 400

# Get and Post one specific favorite with a specific user
@app.route('/users/favorites', methods=['GET', 'POST'])
def handle_favorites(user_id=None):
    if user_id is None:
        return jsonify({"msg": "This endpoint needs a user_id"}), 400

    if request.method == 'GET':
        favorites = Favorite.query.filter_by(id=user_id).all()
        return jsonify([x.serialize() for x in favorites]), 200

    if request.method == 'POST':
        body = request.get_json()
        favorite = Favorite()
        favorite.user_id = user_id
        if 'character_id' in body:
            favorite.character_id = body['character_id']
        else:
            favorite.planet_id = body['planet_id']

        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            "msg": f"Favorite added",
            "inserted_id": f"{favorite.id}"
        }), 200


    return jsonify({"msg": f"{request.method}: Request not valid"}), 400


# Get all the Characters
@app.route('/characters', methods=['GET'])
def handle_characters_all():
   
    characters = Character.query.all()
    return jsonify(characters), 200

# Get and Post one specific favorite with a specific Character
@app.route('/favorite/characters/<int:character_id>', methods=['GET', 'POST', 'DELETE'])
def handle_characters(character_id=None):
    if character_id is None:
        return jsonify({"msg": "This endpoint needs a character_id"}), 400

    if request.method == 'GET':
        favorites = Favorite.query.filter_by(id=character_id).all()
        return jsonify([x.serialize() for x in favorites]), 200

    if request.method == 'POST':
        body = request.get_json()
        favorite = Favorite()
        favorite.character_id = character_id
        if 'character_id' in body:
            favorite.character_id = body['character_id']
        else:
            favorite.planet_id = body['planet_id']

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": f"Favorite added",
        "inserted_id": f"{favorite.id}"
    }), 200


# Planets
@app.route('/planets', methods=['GET'])
def handle_planets_all():
   
    planets = Planet.query.all()
    return jsonify(planets), 200

# Get and Post one specific favorite with a specific Planet
@app.route('/favorite/planets/<int:planet_id>', methods=['GET', 'POST', 'DELETE'])
def handle_planets(planet_id=None):
    if planet_id is None:
        return jsonify({"msg": "This endpoint needs a planet_id"}), 400

    if request.method == 'GET':
        favorites = Favorite.query.filter_by(id=planet_id).all()
        return jsonify([x.serialize() for x in favorites]), 200

    if request.method == 'POST':
        body = request.get_json()
        favorite = Favorite()
        favorite.planet_id = planet_id
        if 'planet_id' in body:
            favorite.planet_id = body['planet_id']
        else:
            favorite.planet_id = body['planet_id']

   
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": f"Favorite added",
        "inserted_id": f"{favorite.id}"
    }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
