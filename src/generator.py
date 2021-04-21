from src.util import negation, conjunction
from util import formula
from util import connective_enum


class Generator(object):
    def __init__(self):
        self.total_length = 1
        self.intermediate_formula = None
        self.resulting_formula = None
        self.position = 0

        while True:
            self.create_formula()

    def create_formula(self, initial_length, formula_length):
        if formula_length == 1:
            # TODO: have more than one letter
            self.position += 1
            self.update_resulting_formula(formula.Formula(None, "A", None, True, False))
            self.position -= 1
        elif formula_length == 2:
            # TODO: also add box and diamond based on what has been used using the ENUM (+1)
            self.position += 2
            self.update_resulting_formula(formula.Formula("~", "A", None, False, False))
            self.position -= 2
        else:
            # TODO: make sure any connective can be used here
            len_one = formula_length - 2
            len_two = formula_length - len_one

            while len_one > 1:
                # note that the first AND second formulas are set to None, these are filled in recursively
                self.update_resulting_formula(formula.Formula("&", None, None, False, True))


    # this method is responsible for keeping the resulting formula up to date
    def update_resulting_formula(self, formula):
        if self.resulting_formula is None:
            self.resulting_formula = formula
        else:
            self.resulting_formula.fill_in(formula)


if __name__ == "__main__":
    generator = Generator()
