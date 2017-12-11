class Drink:
    def __init__(self, name, degrees, quantity):
        self.name = name
        self.degrees = degrees
        self.quantity = quantity

    @classmethod
    def from_redis(cls, data):
        return Drink(data['name'], data['degrees'], data['quantity'])

    def to_client(self):
        return {
            'name': self.name,
            'degrees': self.degrees,
            'quantity': self.quantity
        }