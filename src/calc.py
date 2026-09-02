class Calc:
    def __init__(self, initial_value=0):
        self.value = initial_value

    def add(self, x):
        self.value += x
        return self.value

    def subtract(self, x):
        self.value -= x
        return self.value
