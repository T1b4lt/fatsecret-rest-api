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
    def get(self, lang, food_name):
        """
        get endpoint
        ---      
        tags:
          - Food API Endpoint
        parameters:
          - name: lang
            in: path
            type: string
            required: true
            description: language of the food_name (supported [en, es])
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
                lang:
                  type: string
                  description: Language of the petition
                food_name:
                  type: food
                  description: The food we are looking for           
        """
        url_domain = config_data['langs'][lang]['domain']
        url_resource = config_data['langs'][lang]['resource']
        food_name = food_name.replace(' ', '+')
        food_array = get_food(url_domain, url_resource, food_name)
        return jsonify({
            "type": 'food',
            "lang": lang,
            "food_array": [food_obj.to_json() for food_obj in food_array],
            "timestamp": time.time()
        })


# Api resource routing
api.add_resource(FoodEndpoint, '/food/<string:lang>/<string:food_name>')


if __name__ == "__main__":
    app.run(debug=True)
