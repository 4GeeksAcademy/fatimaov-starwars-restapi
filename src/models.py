from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

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
    # favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(
    #     "FavoritePlanet",
    #     back_populates="user"
    # )
    # favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(
    #     "FavoriteCharacter",
    #     back_populates="user"
    # )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            # "favorite_planets": [fav_planet.serialize() for fav_planet in self.favorite_planets],
            # "favorite_characters": [fav_character.serialize() for fav_character in self.favorite_characters]
            # do not serialize the password, its a security breach
        }
