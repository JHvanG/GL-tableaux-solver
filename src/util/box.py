from .formula import Formula
import copy


class Box(Formula):
    def __init__(self, formula, world=None):
        super().__init__(character="+", formula_one=formula, formula_two=None, is_atom=False, binary=False, world=world, twitter_character='\u25A1')
        self.applied_relations = []
        self.applied_to_all = False
        pass

    def branch(self, solver):
        i = self.world
        all_relations = [item for sublist in solver.relations for item in sublist]
        return_list = []
        for relation in all_relations:
            if relation[0] == i and relation not in self.applied_relations:
                j = relation[1]
                form_a = copy.deepcopy(self.formula_one)
                form_b = copy.deepcopy(self.formula_one)
                self.applied_relations.append([i, j])
                form_b.world = j
                #if not solver.already_on_branch(Box(form_a, j), branch):
                return_list.append(Box(form_a, j))
                #if not solver.already_on_branch(form_b, branch):
                return_list.append(form_b)

        return return_list

    def branch_negated(self, solver):
        from .diamond import Diamond
        from .negation import Negation
        #branch.append(Diamond(Negation(self.formula_one), self.world))
        #return branch
        return [Diamond(Negation(self.formula_one), self.world)]
