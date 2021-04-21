from src.util.formula import Formula


class Negation(Formula):
    def __init__(self, formula):
        Formula.__init__(character="~", formula_one=formula, binary=False)
