class Drink:
    def __init__(self, name, degrees, quantity):
        self.name = name
        self.degrees = degrees
        self.quantity = quantity

    def to_client(self):
        return {
            'name': self.name,
            'degrees': self.degrees,
            'quantity': self.quantity
        }