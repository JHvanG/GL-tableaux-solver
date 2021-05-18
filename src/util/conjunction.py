from .formula import Formula
from .negation import Negation


class Conjunction(Formula):
    def __init__(self, formula_one, formula_two, world=None):
        super().__init__(character="&", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True, world=world)
        pass

    def branch(self, branch, solver):
        # TODO: set world of both formulas
        self.formula_one.world = self.world
        self.formula_two.world = self.world
        branch.append(self.formula_one)
        branch.append(self.formula_two)
        return branch

    def branch_negated(self, branch, solver):
        # TODO: add world number to new formula
        branch.append([Negation(self.formula_one, self.world)])
        branch.append([Negation(self.formula_two, self.world)])
        # from .disjunction import Disjunction
        # branch.append(Disjunction(Negation(self.formula_one), Negation(self.formula_two)))
        return branch
