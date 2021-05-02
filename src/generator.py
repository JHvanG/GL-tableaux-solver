from util import negation, conjunction
from util import formula
from util import connective_enum


class Generator(object):
    def __init__(self):
        self.total_length = 1
        self.position = 0
        self.intermediate_formula = None
        self.resulting_formula = None

    def get_total_length(self):
        return self.total_length

    def set_total_length(self, new_length):
        self.total_length = new_length

    def create_formula(self, formula_length):
        if formula_length == 1:
            # TODO: have more than one letter
            self.position += 1
            self.update_resulting_formula(formula.Formula(None, "A", None, True, False))
            self.check_complete()
            self.position -= 1
        elif formula_length == 2:
            # TODO: also add box and diamond based on what has been used using the ENUM (+1)
            self.position += 2
            self.update_resulting_formula(negation.Negation("A"))
            self.check_complete()
            self.position -= 2
        else:
            # TODO: make sure any connective can be used here
            len_one = formula_length - 2
            len_two = formula_length - len_one - 1

            while len_one >= 1:
                print("Hello")
                # note that the first AND second formulas are set to None, these are filled in recursively
                self.update_resulting_formula(conjunction.Conjunction(None, None))
                # TODO: this currently assumes a binary connective is used!!!
                self.create_formula(len_one)
                self.position += (formula_length - len_two)
                self.create_formula(len_two)
                self.position -= (formula_length - len_two)

                len_one -= 1
                len_two += 1

    # this method is responsible for keeping the resulting formula up to date
    def update_resulting_formula(self, filler):
        if self.resulting_formula is None:
            self.resulting_formula = filler
        else:
            self.resulting_formula.fill_in(filler)

    # this method checks whether a complete formula is produced and prints if that is the case
    def check_complete(self):
        if self.position == self.total_length:
            print(self.resulting_formula.convert_to_string())
            # TODO: remove the last formula, either through a method or by setting a boolean
            """
            for this a method needs to be designed that removes the deepest nested connective
                for binary connectives this should go right unless this is none, then left should be investigated
                if both are None, remove the connective itself and return
                for unary connectives this should only remove itself if its formula is None
            """

    # this method removes the last element in depth first manner
    def remove_element(self, formula):
        # remove last element of binary connective
        # else remove first element
        # else remove entire connective
        # do this in a depth first manner

        if formula.binary and not formula.get_formula_two() is None:
            # check formula


        

    def start(self):
        while True:
            self.create_formula(self.total_length)
            self.total_length += 1


if __name__ == "__main__":
    generator = Generator()
    generator.start()
