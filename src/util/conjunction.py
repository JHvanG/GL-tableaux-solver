from .formula import Formula


class Conjunction(Formula):
    def __init__(self, formula_one, formula_two):
        super().__init__(character="&", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True)
        pass

    # def branch(self):
    # add two formula instances to current branch
