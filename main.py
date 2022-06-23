from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary={}
        for column in self.__table__columns():
            dictionary[column.name]=getattr(self, column.name)
        return dictionary


all_cafe=db.session.query(Cafe).all()





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def random_cafe():
    cafe = random.choice(all_cafe)
    cafe_json={'cafe':{'name': cafe.name, 'location':cafe.location, 'map_url':cafe.map_url, 'img_url':cafe.img_url,'locaiton': cafe.location, 'seats':cafe.seats,'has_toilet':cafe.has_toilet,'has_sockets':cafe.has_sockets, 'cafe_has_wifi':cafe.has_wifi,'location':cafe.location,'seats':cafe.seats,'id':cafe.id}}
    cafe_json=jsonify(cafe_json.to_dict())
    return cafe_json
    

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
