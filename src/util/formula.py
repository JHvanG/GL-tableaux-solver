class Formula(object):
    def __init__(self, character, formula_one, formula_two=None, is_atom=False, binary=True):
        # character representing connective
        self.character = character
        # boolean for a single atom
        self.is_atom = is_atom
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

    def set_formula_one(self, formula):
        self.formula_one = formula
        return

    def get_formula_two(self):
        return self.formula_two

    def set_formula_two(self, formula):
        self.formula_two = formula

    # method to fill in the first empty spot in a formula being generated
    # returns true if a None element is filled in, else it returns false
    def fill_in(self, filler):
        if not self.is_atom:
            if self.formula_one() is None:
                self.formula_one = filler
                return True
            elif self.binary and self.formula_two() is None:
                self.formula_two = filler
                return True
            else:
                if not self.formula_one.is_atom():
                    if self.formula_one.fill_in(filler):
                        return True
                elif self.binary and not self.formula_two.is_atom():
                    return self.formula_two.fill_in(filler)
        
        return False

    # method to print the formula with proper brackets in place
    def print_formula(self):


    # each connective has a get next connective method
    # all gets are inherited from here

    # def find_unique(self):
