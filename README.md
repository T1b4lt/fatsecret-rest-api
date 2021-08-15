# fatsecret-rest-api

![FatsecretIMG](https://a.ftscrt.com/static/images/def20/Fatsecret_logo.png)

Fatsecret superficial REST API

----

This fastsecret REST API tries to cover a series of basic needs when obtaining nutritional information from fatsecret.

Its main purpose is to return nutritional information about the food you are requesting for.

The main petition is as follows,
````
/food/{lang}/{food_name}
````
where _lang_ indicates the language in which you are making the request and _food_name_ the name of the food you are looking for information.

The response of the API is as follows,
````
{
    "type": 'food',
    "lang": <lang>, [Actually EN and ES are supported]
    "timestamp": <timestamp>,
    "food_array": [array, of, food, objects]
}
````
where a _food object_ is as follows,
````
{
    "food_name": 'food_name'
    "food_brand": 'food_brand'
    "protein": 0.0
    "carbs": 0.0
    "fat": 0.0
    "kcal": 0.0
    "unit": 'units'
    "quantity": 0.0
}
````

This API also comes with swagger doc in ```/``` path.

----
## Try it!
1. Clone the repo:
````
git clone https://github.com/T1b4lt/fatsecret-rest-api.git
cd fatsecret-rest-api
````
2. Create a virtual Python environment the way you prefer (I usually use this):
````
python3 -m venv fatsecret_env
````
3. Activate the enviroment:
````
source fatsecret_env/bin/activate
````
4. Install all dependencies:
````
pip install -r requirements.txt
````
5. Run app.py
````
python app.py
````






