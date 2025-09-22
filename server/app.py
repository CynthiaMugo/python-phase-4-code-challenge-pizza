#!/usr/bin/env python3
from models import db, Restaurant,Pizza, RestaurantPizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = []

    for restaurant in restaurants:
        restaurant_list.append({
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name
        })
    return restaurant_list

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)

    restaurant_data = {
        "address": restaurant.address,
        "id": restaurant.id,
        "name": restaurant.name,
        "restaurant_pizzas": [
            {
                "id": rp.id,
                "price": rp.price,
                "pizza": {
                    "id": rp.pizza.id,
                    "ingredients": rp.pizza.ingredients,
                    "name": rp.pizza.name
                }
            } for rp in restaurant.restaurant_pizzas
        ]
    }
    return restaurant_data

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)

    db.session.delete(restaurant)
    db.session.commit()
    return {"Message": f"Restaurant id {id} deleted"}, 204

@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []

    for pizza in pizzas:
        pizza_list.append({
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name
        })
    return pizza_list

@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        new_rp = RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"]
        )
        db.session.add(new_rp)
        db.session.commit()

        response = {
            "id": new_rp.id,
            "price": new_rp.price,
            "pizza_id": new_rp.pizza_id,
            "restaurant_id": new_rp.restaurant_id,
            "pizza": {
                "id": new_rp.pizza.id,
                "name": new_rp.pizza.name,
                "ingredients": new_rp.pizza.ingredients
            },
            "restaurant": {
                "id": new_rp.restaurant.id,
                "name": new_rp.restaurant.name,
                "address": new_rp.restaurant.address
            }
        }
        return make_response(jsonify(response), 201)
    except ValueError:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
