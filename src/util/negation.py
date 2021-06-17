from .formula import Formula


class Negation(Formula):
    def __init__(self, formula, world=None):
        super().__init__(character="~", formula_one=formula, formula_two=None, is_atom=False, binary=False, world=world, twitter_character='\u00AC')
        pass

    def branch(self, solver):
        self.formula_one.world = self.world
        #return self.formula_one.branch_negated(branch, solver)
        return self.formula_one.branch_negated(solver)

    def branch_negated(self, solver):
        self.formula_one.world = self.world
        #if not solver.already_on_branch(self.formula_one, branch):
        #    branch.append(self.formula_one)
        #return branch
        return [self.formula_one]
