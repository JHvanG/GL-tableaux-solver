from .formula import Formula
from .negation import Negation


class Conjunction(Formula):
    def __init__(self, formula_one, formula_two):
        super().__init__(character="&", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True)
        pass

    def branch(self, branch):
        # TODO: set world of both formulas
        branch.append(self.formula_one)
        branch.append(self.formula_two)
        print(branch)
        return branch

    def branch_negated(self, branch):
        branch.append([Negation(self.formula_one)])
        branch.append([Negation(self.formula_two)])
        return branch