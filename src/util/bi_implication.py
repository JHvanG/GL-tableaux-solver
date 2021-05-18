from .formula import Formula
from .negation import Negation


class BiImplication(Formula):
    def __init__(self, formula_one, formula_two, world=None):
        super().__init__(character="<->", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True, world=world)
        pass

    def branch(self, branch):
        # TODO: add world number to new formula
        branch.append([self.formula_one, self.formula_two])
        branch.append([Negation(self.formula_two, self.world), Negation(self.formula_two, self.world)])
        return branch

    def branch_negated(self, branch):
        # TODO: add world number to new formula
        neg_one = Negation(self.formula_one, self.world)
        neg_two = Negation(self.formula_two, self.world)
        self.formula_one.world = self.world
        self.formula_two.world = self.world

        branch.append([self.formula_one, neg_two])
        branch.append([neg_one, self.formula_two])

        return branch
