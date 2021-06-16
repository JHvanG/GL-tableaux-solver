class Formula(object):
    # TODO: I think I should actually remove all getters and setters
    def __init__(self, character, formula_one, formula_two=None, is_atom=False, binary=True, world=None, twitter_character=None):
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
        # unicode character
        self.twitter_character = twitter_character

    # overwritten standard method called when == is used, which does not check world number
    def __eq__(self, other):
        if not isinstance(other, Formula):
            return False
        else:
            return self.character == other.character and self.formula_one == other.formula_one and \
                   self.formula_two == other.formula_two and self.is_atom == other.is_atom and \
                   self.binary == other.binary  # and self.world == other.world

    # this function includes a check for the correct world of the outer connective, as well as equality for the formula
    def equals(self, other):
        return self.world == other.world and self == other

    # this function returns the length of the string representation fo the formula (including brackets)
    def get_length(self):
        return len(self.convert_to_string())

    # this function returns the string representation of a formula
    def convert_to_string(self):
        # any binary connective within another connective is put between brackets
        if self.is_atom:
            return str(self.formula_one)
        elif not self.binary:
            if self.formula_one.binary:
                return self.character + '(' + self.formula_one.convert_to_string() + ')'
            else:
                return self.character + self.formula_one.convert_to_string()
        else:
            if self.formula_one.binary:
                formula_as_string = '(' + self.formula_one.convert_to_string() + ')'
            else:
                formula_as_string = self.formula_one.convert_to_string()

            formula_as_string += self.character

            if self.formula_two.binary:
                formula_as_string = formula_as_string + '(' + self.formula_two.convert_to_string() + ')'
            else:
                formula_as_string = formula_as_string + self.formula_two.convert_to_string()

            return formula_as_string

    # this function returns the string representation of a formula with the unicode characters
    def convert_to_tweet(self):
        if self.is_atom:
            if str(self.formula_one) == '#':
                return self.twitter_character
            else:
                return str(self.formula_one)
        elif not self.binary:
            if self.formula_one.binary:
                return self.twitter_character + '(' + self.formula_one.convert_to_string() + ')'
            else:
                return self.twitter_character + self.formula_one.convert_to_string()
        else:
            if self.formula_one.binary:
                formula_as_string = '(' + self.formula_one.convert_to_string() + ')'
            else:
                formula_as_string = self.formula_one.convert_to_string()

            formula_as_string += self.twitter_character

            if self.formula_two.binary:
                formula_as_string = formula_as_string + '(' + self.formula_two.convert_to_string() + ')'
            else:
                formula_as_string = formula_as_string + self.formula_two.convert_to_string()

            return formula_as_string
