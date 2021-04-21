from src.util.formula import Formula


class Conjunction(Formula):
    def __init__(self, formula_one, formula_two):
        Formula.__init__(character="&", formula_one=formula_one, formula_two=formula_two)

    # def branch(self):
    # add two formula instances to current branch
