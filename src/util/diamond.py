import copy

from .formula import Formula


class Diamond(Formula):
    def __init__(self, formula, world=None):
        super().__init__(character="-", formula_one=formula, formula_two=None, is_atom=False, binary=False, world=world, twitter_character='\u25C7')
        pass

    def branch(self, solver):
        from .diamond import Diamond
        from .negation import Negation
        i = self.world
        j = solver.worlds[len(solver.worlds) - 1] + 1
        solver.worlds.append(j)
        solver.relations[len(solver.relations) - 1].append([i, j])
        solver.apply_transitivity()

        #if not solver.already_on_branch(Negation(Diamond(self.formula_one), j), branch):
        #    branch.append(Negation(Diamond(self.formula_one), j))

        self.formula_one.world = j
        form_a = copy.deepcopy(self.formula_one)
        #if not solver.already_on_branch(self.formula_one, branch):
        #    branch.append(self.formula_one)

        solver.new_relation = True

        return [Negation(Diamond(self.formula_one), j), form_a]

    def branch_negated(self, solver):
        from .box import Box
        from .negation import Negation
        #if not solver.already_on_branch(Box(Negation(self.formula_one), self.world), branch):
        #    branch.append(Box(Negation(self.formula_one), self.world))
        #return branch
        return [Box(Negation(self.formula_one), self.world)]
