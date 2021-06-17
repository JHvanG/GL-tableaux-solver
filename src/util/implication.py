from .formula import Formula
from .negation import Negation


class Implication(Formula):
    def __init__(self, formula_one, formula_two, world=None):
        super().__init__(character=">", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True, world=world, twitter_character='\u21FE')
        pass

    def branch(self, solver):
        #branch.append([Negation(self.formula_one, self.world)])
        self.formula_two.world = self.world
        #branch.append([self.formula_two])
        #return branch
        return [[Negation(self.formula_one, self.world)], [self.formula_two]]

    def branch_negated(self, solver):
        self.formula_one.world = self.world
        #if not solver.already_on_branch(self.formula_one, branch):
        #    branch.append(self.formula_one)
        #if not solver.already_on_branch(Negation(self.formula_two, self.world), branch):
        #    branch.append(Negation(self.formula_two, self.world))
        #return branch
        return [self.formula_one, Negation(self.formula_two, self.world)]
