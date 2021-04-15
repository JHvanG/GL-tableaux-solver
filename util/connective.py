class Connective(object):
    def __init__(self, character, binary = True, formula_one, formula_two = None):
        # character representing connective
        self.character = character
        # boolean for binary connective
        self.binary = binary
        # connected formulae
        self.formula_one = formula_one
        self.formula_two = formula_two

    def get_character(self):
        return self.character

    def get_binary(self):
        return self.binary

    def get_formula_one(self):
        return self.formula_one

    def get_formula_two(self):
        return self.formula_two

    # each connective has a get next connective method
    # all gets are inherited from here

    def find_unique(self):
        