from app import app, db
from models import FavoritePlanet, User, Planet, Character, FavoriteCharacter

with app.app_context():

    # Users
    db.session.add_all([
        User(
            username="jdoe",
            first_name="John",
            last_name="Doe",
            email="jdoe@mail.com",
            password="hashed_password_1",
            is_active=True
        ),
        User(
            username="asmith",
            first_name="Anna",
            last_name="Smith",
            email="asmith@mail.com",
            password="hashed_password_2",
            is_active=True
        ),
        User(
            username="mgarcia",
            first_name="Maria",
            last_name="Garcia",
            email="mgarcia@mail.com",
            password="hashed_password_3",
            is_active=True
        ),
        User(
            username="lmartin",
            first_name="Lucas",
            last_name="Martin",
            email="lmartin@mail.com",
            password="hashed_password_4",
            is_active=True
        )
    ])


    # Planets
    db.session.add_all([
        Planet(
            name="Tatooine",
            terrain="desert",
            population=200000,
            climate="arid"
        ),
        Planet(
            name="Alderaan",
            terrain="grasslands, mountains",
            population=2000000000,
            climate="temperate"
        ),
        Planet(
            name="Yavin IV",
            terrain="jungle, rainforests",
            population=1000,
            climate="temperate, tropical"
        ),
        Planet(
            name="Hoth",
            terrain="frozen",
            population=None,
            climate="tundra, ice caves, mountain ranges"
        )
    ])
    

    # Characters
    db.session.add_all([
        Character(
            name="Luke Skywalker",
            gender="male",
            hair_color="blond",
            eye_color="blue"
        ),
        Character(
            name="C-3PO",
            gender=None,
            hair_color=None,
            eye_color="yellow"
        ),
        Character(
            name="Darth Vader",
            gender="male",
            hair_color=None,
            eye_color="yellow"
        ),
        Character(
            name="Owen Lars",
            gender="male",
            hair_color="brown, grey",
            eye_color="blue"
        )
    ])
    

    # Favorite Planets
    db.session.add_all([
        FavoritePlanet(user_id=2, planet_id=1),
        FavoritePlanet(user_id=2, planet_id=2),
        FavoritePlanet(user_id=1, planet_id=4),
        FavoritePlanet(user_id=3, planet_id=4),
        FavoritePlanet(user_id=3, planet_id=2),
        FavoritePlanet(user_id=4, planet_id=1),
        FavoritePlanet(user_id=4, planet_id=2),
        FavoritePlanet(user_id=4, planet_id=4),
    ])


    # Favorite Characters
    db.session.add_all([
        FavoriteCharacter(user_id=2, character_id=1),
        FavoriteCharacter(user_id=2, character_id=2),
        FavoriteCharacter(user_id=1, character_id=4),
        FavoriteCharacter(user_id=3, character_id=4),
        FavoriteCharacter(user_id=3, character_id=2),
        FavoriteCharacter(user_id=4, character_id=1),
        FavoriteCharacter(user_id=4, character_id=2),
        FavoriteCharacter(user_id=4, character_id=4),
    ])

    db.session.commit()

    print("✅ seed data added")
