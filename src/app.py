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
from models import db, User, Planet, Character, FavoriteCharacter, FavoritePlanet
from sqlalchemy import select, delete
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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
    planet = db.get_or_404(Planet, planet_id, description="No planet found")
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
    character = db.get_or_404(Character, character_id,
                              description="No character found")
    response_body = character.serialize()

    return jsonify(response_body), 200

# GET user's favorite planets and characters
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = db.get_or_404(User, user_id, description="No user found")
    response_body = {
        "favorite_planets": [favplanet.planet.name for favplanet in user.favorite_planets],
        "favorite_characters": [favcharacter.character.name for favcharacter in user.favorite_characters]
    }

    return jsonify(response_body), 200

# POST user's favorite planet
@app.route('/users/<int:user_id>/add_favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(user_id, planet_id):
    user = db.get_or_404(User, user_id, description="No user found")
    planet = db.get_or_404(Planet, planet_id, description="No planet found")
    if user and planet:
        favorite_exists = db.session.execute(
            select(FavoritePlanet)
            .where(
                FavoritePlanet.user_id == user_id,
                FavoritePlanet.planet_id == planet_id)
        ).scalar_one_or_none() is not None

        if not favorite_exists:
            db.session.add(FavoritePlanet(
                user_id=user_id, planet_id=planet_id))
            db.session.commit()
            msg = f'Planet "{planet.name}" has been added to favorites'
        else:
            msg = f'Planet "{planet.name}" is already in favorites'

    return msg, 200

# POST user's favorite character
@app.route('/users/<int:user_id>/add_favorite/character/<int:character_id>', methods=['POST'])
def post_favorite_character(user_id, character_id):
    user = db.get_or_404(User, user_id, description="No user found")
    character = db.get_or_404(Character, character_id, description="No character found")
    if user and character:
        favorite_exists = db.session.execute(
            select(FavoriteCharacter)
            .where(
                FavoriteCharacter.user_id == user_id,
                FavoriteCharacter.character_id == character_id)
        ).scalar_one_or_none() is not None

        if not favorite_exists:
            db.session.add(FavoriteCharacter(
                user_id=user_id, character_id=character_id))
            db.session.commit()
            msg = f'Character "{character.name}" has been added to favorites'
        else:
            msg = f'Character "{character.name}" is already in favorites'

    return msg, 200

# DELETE user's favorite planet
@app.route('/users/<int:user_id>/delete_favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = db.get_or_404(User, user_id, description="No user found")
    planet = db.get_or_404(Planet, planet_id, description="No planet found")
    if user and planet:
        favorite_exists = db.session.execute(
            select(FavoritePlanet)
            .where(
                FavoritePlanet.user_id == user_id,
                FavoritePlanet.planet_id == planet_id)
        ).scalar_one_or_none() is not None
        if favorite_exists:
            db.session.execute(
                delete(FavoritePlanet).where(
                FavoritePlanet.user_id == user_id,
                FavoritePlanet.planet_id == planet_id
                )
            )
            db.session.commit()
            msg = f'Planet "{planet.name}" has been removed from favorites'
        else: 
            msg = f'Planet "{planet.name}" is not in favorites'

    return msg, 200

# DELETE user's favorite character
@app.route('/users/<int:user_id>/delete_favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    user = db.get_or_404(User, user_id, description="No user found")
    character = db.get_or_404(Character, character_id, description="No character found")
    if user and character:
        favorite_exists = db.session.execute(
            select(FavoriteCharacter)
            .where(
                FavoriteCharacter.user_id == user_id,
                FavoriteCharacter.character_id == character_id)
        ).scalar_one_or_none() is not None
        if favorite_exists:
            db.session.execute(
                delete(FavoriteCharacter).where(
                FavoriteCharacter.user_id == user_id,
                FavoriteCharacter.character_id == character_id
                )
            )
            db.session.commit()
            msg = f'Character "{character.name}" has been removed from favorites'
        else: 
            msg = f'Character "{character.name}" is not in favorites'

    return msg, 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
