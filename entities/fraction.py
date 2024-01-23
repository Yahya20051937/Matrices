class Fraction:
    @staticmethod
    def add(fraction1, fraction2):
        return Fraction(
            numerator=fraction1.numerator * fraction2.denominator + fraction2.numerator * fraction1.denominator,
            denominator=fraction1.denominator * fraction2.denominator)

    @staticmethod
    def multiply(fraction1, fraction2):
        return Fraction(numerator=fraction1.numerator * fraction2.numerator, denominator=fraction1.denominator * fraction2.denominator)

    @staticmethod
    def divide(fraction1, fraction2):
        return Fraction(numerator=fraction1.numerator * fraction2.denominator, denominator=fraction1.denominator * fraction2.numerator)

    def __init__(self, numerator, denominator):
        if denominator != 0:
            self.numerator = numerator
            self.denominator = denominator
        else:
            raise Exception

    def __str__(self):
        if self.denominator != 1:
            return f"{self.numerator}/{self.denominator}"
        else:
            return self.numerator


