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
from models import db, User, Planet, Character
from sqlalchemy import select
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

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = db.session.execute(select(User)).scalars().all()
    response_body = [user.serialize() for user in all_users]
    
    return jsonify(response_body), 200

# GET all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = db.session.execute(select(Planet)).scalars().all()
    response_body = [planet.serialize() for planet in all_planets]
    
    return jsonify(response_body), 200

# GET single planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
    response_body = planet.serialize()
    
    return jsonify(response_body), 200

# GET all characters
@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = db.session.execute(select(Character)).scalars().all()
    response_body = [character.serialize() for character in all_characters]
    
    return jsonify(response_body), 200

# GET single character
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    character = db.session.get(Character, character_id)
    response_body = character.serialize()
    
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
