from util.formula import Formula


class Negation(Formula):
    def __init__(self, formula):
        super().__init__(character="~", formula_one=formula, formula_two=None, is_atom=False, binary=False)
        pass
