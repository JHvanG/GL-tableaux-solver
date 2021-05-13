from .formula import Formula
from .negation import Negation


class Disjunction(Formula):
    def __init__(self, formula_one, formula_two):
        super().__init__(character="|", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True)
        pass

    def branch(self, branch):
        branch.append([self.formula_one])
        branch.append([self.formula_two])
        return branch

    def branch_negated(self, branch):
        from .conjunction import Conjunction
        branch.append(Conjunction(Negation(self.formula_one), Negation(self.formula_two)))
        return branch
