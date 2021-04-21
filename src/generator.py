from src.util import negation
from util import formula
from util import connective_enum


class Generator(object):
    def __init__(self):
        self.total_length = 1
        self.resulting_formula = None

        while True:
            self.create_formula()

    def create_formula(self, formula_length):

        if formula_length == 0:
            return None
        elif formula_length == 1:
            # TODO: have more than one letter
            new_form = formula.Formula(None, "A", True, False)
            return new_form
        elif formula_length == 2:
            # TODO: also add box and diamond based on what has been used using the ENUM (+1)
            new_form = negation.Negation("A")
            return new_form
        else:
            len_one = formula_length - 2
            len_two = formula_length - len_one
            while len_one > 1:
                # TODO: also add other binary connectives based on what has been used using the ENUM (+1)
                new_form = formula.Conjunction(self.create_formula(len_one), self.create_formula(len_two))
                len_one -= 1
                len_two += 1

        """
        The plan is to continuously increase the length of the formula once the first formula is done.
        First a sequence of negations
        Might be best to do this in a recursive manner? first n, then n-1 or n-1 or whatever?
        Can also do like: A & B will result in len_A = n - 2, then len_A = n - 3, etc. until len_A = 1, len_B will then
        be the remaining element.
        For all single connectives this is much simpler and based on priority: neg, box, diamond
        For all binary connectives this is con, dis, imp, bi-imp

        Generation is done by: formula --> connective and one or two formula(s) --> both into connectives again...
        This continues until length is 0

        first attempt whether a connective is suitable, then a formula
        
        might be more logical to start at the back?
        
        """

        # this function will generate a new formula of same length as last unless all are already present
        # then it will increase in length and check for all connectives again
        # first only with 1 letter


if __name__ == "__main__":
    generator = Generator()
