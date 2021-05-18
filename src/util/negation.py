from .formula import Formula


class Negation(Formula):
    def __init__(self, formula, world=None):
        super().__init__(character="~", formula_one=formula, formula_two=None, is_atom=False, binary=False, world=world)
        pass

    def branch(self, branch, solver):
        return self.formula_one.branch_negated(branch, solver)

    def branch_negated(self, branch, solver):
        # TODO: add world number to new formula
        self.formula_one.world = self.world
        branch.append(self.formula_one)
        return branch
