class Food:
    def __init__(self, food_name):
        self.food_name = food_name
        self.protein = 0.0
        self.carbs = 0.0
        self.fat = 0.0
        self.kcal = 0.0
        self.unit = ''
        self.quantity = 0.0

    def to_json(self):
        return dict(title=self.food_name)