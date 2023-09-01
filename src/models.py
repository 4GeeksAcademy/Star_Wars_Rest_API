from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id= db.Column(db.Integer, db.ForeignKey("character.id"))
    planet_id= db.Column(db.Integer, db.ForeignKey("planet.id"))

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(120), nullable=True)
    hair_color = db.Column(db.String(120), nullable=True)
    eye_color = db.Column(db.String(120), nullable=True)
    birth_year = db.Column(db.String(120), nullable=True)
    rotation_period = db.Column(db.String(120), nullable=True)
    height = db.Column(db.String(3), nullable=True)
    skin_color = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "rotation_period": self.rotation_period,
            "height": self.height,
            "skin_color": self.skin_color,
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(120), nullable=True)
    population = db.Column(db.String(120), nullable=True)
    orbital_period = db.Column(db.String(120), nullable=True)
    rotation_period = db.Column(db.String(120), nullable=True)
    diameter = db.Column(db.String(3), nullable=True)
    terrain = db.Column(db.String(120), nullable=True)
    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            "terrain": self.terrain,
        }