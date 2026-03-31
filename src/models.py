from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relationship One - Many
    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="user")
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship("FavoriteCharacter",back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "favorite_planets": [fav_planet.serialize() for fav_planet in self.favorite_planets],
            "favorite_characters": [fav_character.serialize() for fav_character in self.favorite_characters]
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[int] = mapped_column(Integer(), nullable=True)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)

    # Relationship One - Many
    favorites: Mapped[list["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "climate": self.climate,
            "favorites": [fav_planet.serialize() for fav_planet in self.favorites ]
        }
    
class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(120), nullable=True)

    # Relationship One - Many
    favorites: Mapped[list["FavoriteCharacter"]] = relationship(
        "FavoriteCharacter",
        back_populates="character"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }

class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    # ForeignKeys
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    # Relationship Many - One
    user: Mapped["User"] = relationship("User", back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship("Planet",back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.name
        }

class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    # ForeignKeys
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    # Relationship Many - One
    user: Mapped["User"] = relationship("User",back_populates="favorite_characters")
    character: Mapped["Character"] = relationship("Character",back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.name
        }