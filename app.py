import json
import os
import logging
import sys
import config
import requests
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from
from utils.utils import get_food
import yaml
import time


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
    "specs_route": "/"
}
swagger = Swagger(app, template=template)
app.config.from_object(config.Config)
api = Api(app)
config_file = open('config.yaml')
config_data = yaml.load(config_file, Loader=yaml.FullLoader)


class FoodEndpoint(Resource):
    def get(self, country, food_name):
        """
        get endpoint
        ---      
        tags:
          - Food API Endpoint
        parameters:
          - name: country
            in: path
            type: string
            required: true
            description: country from which you want the information (supported [us, es])
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
                country:
                  type: string
                  description: Country from which you want the information
                food_array:
                  type: array of food_objects
                  description: Array of food_objects
                timestamp:
                  type: timestamp
                  description: Timestamp of petition           
        """
        url_domain = config_data['countries'][country]['domain']
        url_resource = config_data['countries'][country]['resource']
        food_name = food_name.replace(' ', '+')
        food_array = get_food(url_domain, url_resource, food_name)
        return jsonify({
            "type": 'food',
            "country": country,
            "food_array": [food_obj.to_json() for food_obj in food_array],
            "timestamp": time.time()
        })


# Api resource routing
api.add_resource(FoodEndpoint, '/food/<string:country>/<string:food_name>')


if __name__ == "__main__":
    app.run(debug=True)
