from .formula import Formula
import copy


class Box(Formula):
    def __init__(self, formula, world=None):
        super().__init__(character="+", formula_one=formula, formula_two=None, is_atom=False, binary=False, world=world, twitter_character='\u25A1')
        self.applied_relations = []
        self.applied_to_all = False
        pass

    def branch(self, branch, solver):
        i = self.world
        for relation in solver.relations:
            if relation[0] == i and relation not in self.applied_relations:
                j = relation[1]
                formula_a = copy.deepcopy(self.formula_one)
                formula_b = copy.deepcopy(self.formula_one)
                self.applied_relations.append([i, j])
                branch.append(Box(formula_a, j))
                formula_b.world = j
                branch.append(formula_b)

        return branch

    def branch_negated(self, branch, solver):
        from .diamond import Diamond
        from .negation import Negation
        branch.append(Diamond(Negation(self.formula_one), self.world))
        return branch
