from rational import RationalFunction

class Integration:

    def __init__(self, expression):
        self.func = RationalFunction(expression)
        self.func.parse_fractionally_rational_function()
        self.result = None

    def integrate(self):
        func_type =