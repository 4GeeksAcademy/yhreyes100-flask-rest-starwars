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
from models import db, User,Character,Planet,Favorite
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

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    response_body = {
    "users":users
    }

    return jsonify(response_body), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    response_body = {
    "user":user.serialize()
    }
    return jsonify(response_body), 200
"""use this on the fronted user creation{
                                        "username":"test12",
                                        "password":"test123"
                                        }
"""
@app.route('/user', methods=['POST'])
def create_user():
    data =  request.json
    user1 = User(user_name=data["username"], password=data["password"])
    db.session.add(user1)
    db.session.commit()
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    response_body = {
    "users":users
    }

    return jsonify(response_body), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get([id])
    db.session.delete(user)
    db.session.commit()
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))
    response_body = {
    "users":users
    }
    return jsonify(response_body), 200

"""Use this on the fronted character creation {
                                                "birth_year":"N/A",
                                                "eye_color":"green",
                                                "gender":"male",
                                                "height":"193",
                                                "mass":"210",
                                                "name":"Luke Skywalker"
                                            }
"""

@app.route('/character', methods=['POST'])
def create_character():
    data =  request.json
    character1 = Character(birth_year=data["birth_year"], eye_color=data["eye_color"], gender=data["gender"], height=data["height"], mass=data["mass"], name=data["name"])
    db.session.add(character1)
    db.session.commit()
    characters = Character.query.all()
    characters = list(map(lambda x: x.serialize(), characters))
    response_body = {
    "characters":characters
    }

    return jsonify(response_body), 200
"""use this on the fronted planet creation  {
                                                "diameter":"464464564",
                                                "climate":"cold",
                                                "population":"3698552114",
                                                "gravity":"N/A",
                                                "terrain":"desert",
                                                "rotation_period":"N/A",
                                                "name":"Javin IV"
                                            }
"""
@app.route('/planet', methods=['POST'])
def create_planet():
    data =  request.json
    planet1 = Planet(diameter=data["diameter"], climate=data["climate"], population=data["population"], gravity=data["gravity"], terrain=data["terrain"],rotation_period=data["rotation_period"], name=data["name"])
    db.session.add(planet1)
    db.session.commit()
    planets = Planet.query.all()
    planets = list(map(lambda x: x.serialize(), planets))
    response_body = {
    "Planets":planets
    }

    return jsonify(response_body), 200
""" use this on the favorite creation   {
                                            "category":"character" or "planet",
                                            "entity_id":1,
                                            "user_id":1
                                        }"""
@app.route('/favorite', methods=['POST'])
def create_favorite():
    data =  request.json
    if(data["category"]=="planet"):
        fav1 = Favorite(user_id=data["user_id"], planet_id=data["entity_id"])
    elif(data["category"]=="character"):
        fav1 = Favorite(user_id=data["user_id"], character_id=data["entity_id"])    
    db.session.add(fav1)
    db.session.commit()
    fav = Favorite.query.all()
    fav = list(map(lambda x: x.serialize(), fav))
    response_body = {
    "fav":fav
    }

    return jsonify(response_body), 200

@app.route('/favorite/<int:id>', methods=['DELETE'])
def delete_Favorite(id):
    fav = Favorite.query.get([id])
    db.session.delete(fav)
    db.session.commit()
    favorites = Favorite.query.all()
    favorites = list(map(lambda x: x.serialize(), favorites))
    response_body = {
    "favorites":favorites
    }
    return jsonify(response_body), 200


@app.route('/favorite/<int:id>', methods=['GET'])
def get_favoriteByUser(id):
    favorites = Favorite.query.filter_by(user_id=id).all()
    favorites = list(map(lambda x: x.serialize(), favorites))
    response_body = {
    "favorites":favorites
    }
    return jsonify(response_body), 200

@app.route('/favorite', methods=['GET'])
def get_favorite():
    favorites = Favorite.query.all()
    favorites = list(map(lambda x: x.serialize(), favorites))
    response_body = {
    "favorites":favorites
    }
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
