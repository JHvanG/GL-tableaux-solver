class Connective(object):
    def __init__(self, binary = True, formula_one, formula_two = None):
        # boolean for binary connective
        self.binary = binary
        # connected formulae
        self.formula_one = formula_one
        self.formula_two = formula_two

    def find_unique(self):
        