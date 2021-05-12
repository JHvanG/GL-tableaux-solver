from .formula import Formula


class Implication(Formula):
    def __init__(self, formula_one, formula_two):
        super().__init__(character="->", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True)
        pass