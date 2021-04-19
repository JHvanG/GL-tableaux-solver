class Conjunction(Connective):
    def __init__(self, character, binary = True, formula_one, formula_two = None):
        Connective.__init__(character, binary, formula_one, formula_two)

    def branch(self):
        # add two formula instances to current branch