from .formula import Formula
from .negation import Negation
import copy

class BiImplication(Formula):
    def __init__(self, formula_one, formula_two, world=None):
        super().__init__(character="=", formula_one=formula_one, formula_two=formula_two, is_atom=False, binary=True, world=world, twitter_character='\u21FF')
        pass

    def branch(self, solver):
        form_a = copy.deepcopy(self.formula_one)
        form_b = copy.deepcopy(self.formula_two)
        form_a.world = self.world
        form_b.world = self.world
        neg_a = Negation(self.formula_one, self.world)
        neg_b = Negation(self.formula_two, self.world)
        #branch.append([Negation(self.formula_one, self.world), Negation(self.formula_two, self.world)])
        #self.formula_one.world = self.world
        #self.formula_two.world = self.world
        #branch.append([self.formula_one, self.formula_two])
        #return branch
        return [[form_a, form_b], [neg_a, neg_b]]

    def branch_negated(self, solver):
        form_a = copy.deepcopy(self.formula_one)
        form_b = copy.deepcopy(self.formula_two)
        form_a.world = self.world
        form_b.world = self.world
        neg_a = Negation(self.formula_one, self.world)
        neg_b = Negation(self.formula_two, self.world)
        #neg_one = Negation(self.formula_one, self.world)
        #neg_two = Negation(self.formula_two, self.world)
        #self.formula_one.world = self.world
        #self.formula_two.world = self.world
        #branch.append([self.formula_one, neg_two])
        #branch.append([neg_one, self.formula_two])
        #return branch
        return [[form_a, neg_b], [neg_a, form_b]]

    '''
        def branch(self, branch, solver):
        branch.append([Negation(self.formula_one, self.world), Negation(self.formula_two, self.world)])
        form_a = copy.deepcopy(self.formula_one)
        form_b = copy.deepcopy(self.formula_two)
        form_a.world = self.world
        form_b.world = self.world
        branch.append([form_a, form_b])
        return branch

    def branch_negated(self, branch, solver):
        neg_one = Negation(self.formula_one, self.world)
        neg_two = Negation(self.formula_two, self.world)
        form_a = copy.deepcopy(self.formula_one)
        form_b = copy.deepcopy(self.formula_two)
        form_a.world = self.world
        form_b.world = self.world

        branch.append([form_a, neg_two])
        branch.append([neg_one, form_b])

        return branch
    '''
