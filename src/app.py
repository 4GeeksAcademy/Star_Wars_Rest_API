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

from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.url_map.strict_slashes = False

#setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')
jwt = JWTManager(app)

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

#Create a route to authenticate your users.
#Create_acess_token() function is used to actually generate the JWT.
@app.route('/token', methods=['POST'])
def handle_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    new_token = User.query.filter_by(email=email, password=password).first()
    if new_token is None:
        return jsonify({"msg": " This email or password is incorrect"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Create users
@app.route('/create-user', methods=['POST'])
def create_user():
    
    user = User()
    user.email = request.json.get("email", None)
    user.password = request.json.get("password", None)
    new_user = User.query.filter_by(email=user.email, password=user.password).first()
    if new_user is None:
        return jsonify({"msg": " This email or password is incorrect"}), 401
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)

# Get all the users
@app.route('/users', methods=['GET'])
@jwt_required()
def handle_users_all():
   
    users = User.query.all()

    return jsonify([x.serialize() for x in users]), 200

# Get one specific favorite with a specific user
@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def handle_favorites():
    user = User.query.filter_by(email=get_jwt_identity()).first()
    favorites = Favorite.query.filter_by(user_id=user.id).all()
    return jsonify([x.serialize() for x in favorites]), 200

# Get all the Characters
@app.route('/characters', methods=['GET'])
@jwt_required()

def handle_characters_all():
    get_jwt_identity()
    characters = Character.query.all()
    return jsonify([x.serialize() for x in characters]), 200

# Get one specific Character
@app.route('/characters/<int:character_id>', methods=['GET'])
@jwt_required()
def handle_characters(character_id):
    favorites = Favorite.query.filter_by(id=character_id).all()
    return jsonify([x.serialize() for x in favorites]), 200

# Post the favorite with a specific character
@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
@jwt_required()
def create_characters(character_id):
    try:
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        if character_id is None:
            return jsonify({"error": "Character ID is required"}), 400

        favorite = Favorite(user_id=user.id, character_id=character_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            "msg": "Favorite added",
            "inserted_id": favorite.id  # Assuming `id` is the primary key of the Favorite model
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500   

# Delete one specific favorite with a specific Character
@app.route('/favorite/characters/<int:character_id>', methods=['DELETE'])
@jwt_required()
def delete_characters(character_id):

    # Check if a favorite record as the given character_id and match to the user_id from the token of the user that are autorized in the moment that method are called in
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    favorite = Favorite.query.filter_by(user_id=user.id, character_id=character_id).first()

    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    try:
        db.session.delete(favorite)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "msg": f"Favorite eliminated",
        "eliminated_id": f"{character_id}"
    }), 200

# Update the character with a specific id
@app.route('/characters/<int:id>', methods=['PUT'])
@jwt_required()
def update_characters(id):
    # Check if the character with the given ID exists in the database
    character = Character.query.get(id)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    # Make the necessary updates to the character (for example, modifying its attributes)
    # character.some_attribute = request.json.get("some_attribute")

    # Commit the changes to the database
    # Commit the changes to the database
    character.verified = True
    db.session.commit()

    return jsonify({
        "msg": f"Character updated",
        "updated_id": id
    }), 200

# Get all the planets
@app.route('/planets', methods=['GET'])
@jwt_required()
def handle_planets_all():
   
    planets = Planet.query.all()
    return jsonify([x.serialize() for x in planets]), 200

# Get one specific Planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
@jwt_required()
def handle_planets(planet_id):

        favorites = Favorite.query.filter_by(id=planet_id).all()
        return jsonify([x.serialize() for x in favorites]), 200

# Post one specific favorite with a specific Planet
@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
@jwt_required()
def create_planets(planet_id):
    try:
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        if planet_id is None:
            return jsonify({"error": "planet ID is required"}), 400

        favorite = Favorite(user_id=user.id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify({
            "msg": "Favorite added",
            "inserted_id": favorite.id  # Assuming `id` is the primary key of the Favorite model
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500   

# Delete one specific favorite with a specific Planet
@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_planets(planet_id):
    # Check if a favorite record as the given character_id and match to the user_id from the token of the user that are autorized in the moment that method are called in
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()

    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    try:
        db.session.delete(favorite)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "msg": f"Favorite eliminated",
        "eliminated_id": f"{planet_id}"
    }), 200

# Update the planet with a specific id
@app.route('/planets/<int:id>', methods=['PUT'])
@jwt_required()
def update_planets(id):
    # Check if the planet with the given ID exists in the database
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"error": "planet not found"}), 404

    # Make the necessary updates to the planet (for example, modifying its attributes)
    # planet.some_attribute = request.json.get("some_attribute")

    # Commit the changes to the database
    planet.verified = True
    db.session.commit()

    return jsonify({
        "msg": f"planet updated",
        "updated_id": id
    }), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

