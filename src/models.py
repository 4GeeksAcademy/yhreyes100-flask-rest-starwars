from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    user_name   = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    birth_year = db.Column(db.String(20), nullable=True)
    eye_color = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    hair_color  = db.Column(db.String(50), nullable=True)
    height = db.Column(db.String(50), nullable=True)
    mass   = db.Column(db.String(50), nullable=True)
    name   = db.Column(db.String(100), nullable=True) 
    skin_color = db.Column(db.String(50), nullable=True)
    created = db.Column(db.String(80), nullable=True)
    edited  = db.Column(db.String(80), nullable=True)
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "name": self.name,
            "skin_color": self.skin_color,
            "created": self.created,
            "edited": self.edited,
            # do not serialize the password, its a security breach
        }    

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name   = db.Column(db.String(100), nullable=True) 
    diameter = db.Column(db.String(100), nullable=True) 
    climate = db.Column(db.String(100), nullable=True) 
    population   = db.Column(db.String(100), nullable=True) 
    gravity = db.Column(db.String(100), nullable=True)
    terrain = db.Column(db.String(100), nullable=True)
    rotation_period = db.Column(db.String(100), nullable=True)
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "population": self.population,
            "gravity": self.gravity,
            "name": self.name,
            "terrain": self.terrain,
            "rotation_period": self.rotation_period,
            # do not serialize the password, its a security breach
        } 

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(100), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user =  db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey(Character.id))
    character =  db.relationship(Character)
    planet_id = db.Column(db.Integer, db.ForeignKey(Planet.id))
    planet =  db.relationship(Planet)
    
    def __repr__(self):
        return '<Favorite %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        } 
   