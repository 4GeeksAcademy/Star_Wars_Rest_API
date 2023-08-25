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

    return jsonify([x.serialize() for x in users]), 200

# Get one specific favorite with a specific user
@app.route('/users/favorites', methods=['GET'])
def handle_favorites():
    user_id=2
    request.method == 'GET'
    favorites = Favorite.query.filter_by(id=user_id).all()
    return jsonify([x.serialize() for x in favorites]), 200


# Get all the Characters
@app.route('/characters', methods=['GET'])
def handle_characters_all():
   
    characters = Character.query.all()
    return jsonify([x.serialize() for x in characters]), 200

# Get one specific Character
@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_characters(character_id):
    character_id=1

    favorites = Favorite.query.filter_by(id=character_id).all()
    return jsonify([x.serialize() for x in favorites]), 200

# Post the favorite with a specific character
@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
def create_characters(character_id):
    
    body = request.get_json()
    print(body)
    favorite = Favorite(
        user_id = 2,
        character_id = character_id
    )
    favorite.character_id = body['character_id']
   
    if character_id not in body:
        return jsonify({"error": "Character ID is required"}), 400

    
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": f"Favorite added",
        "inserted_id": f"{favorite.character_id}"
    }), 200

# Delete one specific favorite with a specific Character
@app.route('/favorite/characters/<int:character_id>', methods=['DELETE'])
def delete_characters(character_id):

    body = request.get_json()
    print(body)
    favorite = Favorite(
        user_id = 2,
        character_id = character_id
    )
    favorite.character_id = body['character_id']
   
    if character_id not in body:
        return jsonify({"error": "Character ID is required"}), 400

    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "msg": f"Favorite eliminated",
        "eliminated_id": f"{favorite.character_id}"
    }), 200

# Get all the planets
@app.route('/planets', methods=['GET'])
def handle_planets_all():
   
    planets = Planet.query.all()
    return jsonify([x.serialize() for x in planets]), 200

# Get one specific Planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planets(planet_id):

        favorites = Favorite.query.filter_by(id=planet_id).all()
        return jsonify([x.serialize() for x in favorites]), 200

# Post one specific favorite with a specific Planet
@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def create_planets(planet_id):

    body = request.get_json()
    print(body)
    favorite = Favorite(
        user_id = 2,
        planet_id = planet_id
        )
    favorite.planet_id = body['planet_id']
   
    if 'planet_id' not in body:
        return jsonify({"error": "Planet ID is required"}), 400

    
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": f"Favorite added",
        "inserted_id": f"{favorite.planet_id}"
    }), 200

# Delete one specific favorite with a specific Planet
@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_planets(planet_id):

    body = request.get_json()
    print(body)
    favorite = Favorite(
        user_id = 2,
        planet_id = planet_id
        )
    favorite.planet_id = body['planet_id']
   
    if 'planet_id' not in body:
        return jsonify({"error": "Planet ID is required"}), 400

    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "msg": f"Favorite eliminated",
        "eliminated_id": f"{favorite.planet_id}"
    }), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
