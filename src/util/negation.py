from .formula import Formula


class Negation(Formula):
    def __init__(self, formula):
        super().__init__(character="~", formula_one=formula, formula_two=None, is_atom=False, binary=False)
        pass

    def branch(self, branch):
        return self.formula_one.branch_negated(branch)

    def branch_negated(self, branch):
        branch.append(self.formula_one)
        return branch
