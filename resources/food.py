class Food:
    def __init__(self, food_name):
        self.food_name = food_name

    def to_json(self):
        return dict(title=self.food_name)