from resources.food import Food
from bs4 import BeautifulSoup
import requests
import re
from lxml import etree
import unidecode

def get_info_es(food_info):
    food_info = food_info.replace(',', '.')
    food_info = unidecode.unidecode(food_info)
    unit_quantity_part = food_info.split('-')[0]
    macro_nutrient_part = food_info.split('-')[1]
    array_macro = [re.findall("\d+\.?\d+", part)
                   for part in macro_nutrient_part.split('|')]
    kcal = array_macro[0][0] if len(array_macro[0]) > 0 else 0.0
    fat = array_macro[1][0] if len(array_macro[1]) > 0 else 0.0
    carbs = array_macro[2][0] if len(array_macro[2]) > 0 else 0.0
    prot = array_macro[3][0] if len(array_macro[3]) > 0 else 0.0
    quantity_unit = re.findall("\d+ ?[a-z]+", unit_quantity_part)[0]
    quantity = re.findall("\d+", quantity_unit)[0]
    unit = re.findall("[a-z]+", quantity_unit)[0]

    return (quantity, unit, kcal, fat, carbs, prot)


def get_info(row, lang):
    food_name = row.xpath('.//a[contains(@class, "prominent")]')[0].text
    food_brand = row.xpath('.//a[contains(@class, "brand")]')[0].text if \
        len(row.xpath('.//a[contains(@class, "brand")]')) > 0 else None
    food_info = row.xpath('.//div')[0].text
    food_info = re.sub(r"[\t\r\n]", "", food_info)
    if lang == 'es':
        quantity, unit, kcal, fat, carbs, prot = get_info_es(food_info)

    return (food_name, food_brand, quantity, unit, kcal, fat, carbs, prot)

def get_food(url_domain, url_resource, food_name):
    URL = 'https://www.fatsecret.'+url_domain+'/'+url_resource+'/search?q='+food_name
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    result_rows = dom.xpath('//table[@class="generic searchResult"]//tr')
    result = [get_info(row, url_domain) for row in result_rows]
    food_array = []
    for element in result:
        food_obj = Food(element[0])
        food_obj.food_brand = element[1]
        food_obj.quantity = element[2]
        food_obj.unit = element[3]
        food_obj.kcal = element[4]
        food_obj.fat = element[5]
        food_obj.carbs = element[6]
        food_obj.protein = element[7]
        food_array.append(food_obj)
    return food_array