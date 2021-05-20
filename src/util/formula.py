class Formula(object):
    # TODO: I think I should actually remove all getters and setters
    def __init__(self, character, formula_one, formula_two=None, is_atom=False, binary=True, world=None):
        # character representing connective
        self.character = character
        # boolean for a single atom
        self.is_atom = is_atom
        # boolean for binary connective
        self.binary = binary
        # connected formulae
        self.formula_one = formula_one
        self.formula_two = formula_two
        # world of the formula
        self.world = world

    def __eq__(self, other):
        if not isinstance(other, Formula):
            return False
        else:
            return self.character == other.character and self.formula_one == other.formula_one and \
                   self.formula_two == other.formula_two and self.is_atom == other.is_atom and \
                   self.binary == other.binary and self.world == other.world

    # method to fill in the first empty spot in a formula being generated
    # returns true if a None element is filled in, else it returns false
    '''
    def fill_in(self, filler):
        if not self.is_atom:
            if self.formula_one is None:
                self.formula_one = filler
                return True
            elif self.binary and self.formula_two is None:
                self.formula_two = filler
                return True
            else:
                if not self.formula_one.is_atom:
                    if self.formula_one.fill_in(filler):
                        return True
                elif self.binary and not self.formula_two.is_atom:
                    return self.formula_two.fill_in(filler)
        
        return False
    '''

    # method to print the formula with proper brackets in place
    def convert_to_string(self):
        if self.is_atom:
            return str(self.formula_one)
        elif not self.binary:
            return self.character + self.formula_one.convert_to_string()
        else:
            if self.formula_one.binary:
                formula_as_string = "(" + self.formula_one.convert_to_string() + ")"
            else:
                formula_as_string = self.formula_one.convert_to_string()

            formula_as_string += self.character

            if self.formula_two.binary:
                formula_as_string += "(" + self.formula_two.convert_to_string() + ")"
            else:
                formula_as_string += self.formula_two.convert_to_string()

            return formula_as_string
