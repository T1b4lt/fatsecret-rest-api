import json
import os
import logging
import sys
import config
import requests
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from
from resources.food import Food


# Setup Flask Server
app = Flask(__name__)


# Create an APISpec
template = {
    "swagger": "2.0",
    "info": {
        "title": "Fatsecret API",
        "description": "A Restful API for Fatsecret food info",
        "version": "0.1.1",
        "contact": {
            "name": "T1b4lt",
            "github": "https://github.com/T1b4lt",
        }
    }
}

app.config['SWAGGER'] = {
    'title': 'Fatsecret API',
    'uiversion': 3,
    "specs_route": "/swagger/"
}
swagger = Swagger(app, template=template)
app.config.from_object(config.Config)
api = Api(app)

class Welcome(Resource):
  def get(self):
    """
    get endpoint
    ---
    tags:
     - Welcome endpoint
    """
    return "Visit /swagger"


class FoodEndpoint(Resource):
    def get(self, food_name):
        """
        get endpoint
        ---      
        tags:
          - Food API Endpoint
        parameters:
          - name: food_name
            in: path
            type: string
            required: true
            description: name of the food
        responses:
          500:
            description: NOT OK
          200:
            description: OK
            schema:
              id: food
              properties:
                type:
                  type: string
                  description: Type of object
                food_name:
                  type: food
                  description: The food we are looking for           
        """
        food_object = Food(food_name)
        return jsonify({
            "type": 'food',
            "food_object": food_object.to_json()
        })


# Api resource routing
api.add_resource(FoodEndpoint, '/food/<string:food_name>')
api.add_resource(Welcome, '/')


if __name__ == "__main__":
    app.run(debug=True)
