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
        for column in self.__table__.columns:
            dictionary[column.name]=getattr(self, column.name)
        return dictionary


all_cafe=db.session.query(Cafe).all()





@app.route("/")
def home():
    return render_template("index.html")

@app.route("/all")
def all():
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafe])

@app.route("/add", methods=["POST","GET"])
def add():

    cafe_response=request.form.to_dict()
    for key,value in cafe_response.items():
        if value.lower()=="true":
            cafe_response[key]=bool('True')
        elif value.lower()=="false":
            cafe_response[key]=bool('')
    new_cafe=Cafe(**cafe_response)
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success" :"Cafe added to database"})

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})



@app.route("/random", methods=["GET"])
def delete():
    cafe = random.choice(all_cafe)
    cafe_json={'cafe':{'name': cafe.name, 'location':cafe.location, 'map_url':cafe.map_url, 'img_url':cafe.img_url,'location': cafe.location, 'seats':cafe.seats,'has_toilet':cafe.has_toilet,'has_sockets':cafe.has_sockets, 'cafe_has_wifi':cafe.has_wifi,'location':cafe.location,'seats':cafe.seats,'id':cafe.id}}
    cafe_json=jsonify(cafe=cafe.to_dict())
    return cafe_json

@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def report_closed(cafe_id):
    api_key=request.args.get("api-key")


    if  api_key=="TopSecretApiKey":
        cafe_to_delete = db.session.query(Cafe).get(cafe_id)

        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
             #200 = OK
            return jsonify(success={"success":"cafe deleted"}),200
        else:
            #404 = Resource not found
            return jsonify(error={"Not found":"Sorry a cafe with such id was not found"}),404
    else :
        return jsonify(error={"Forbidden": "Sorry the api_key is wrong make sure you have the correct one "}), 403






if __name__ == '__main__':
    app.run(debug=True)
