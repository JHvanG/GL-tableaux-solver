from .formula import Formula


class Diamond(Formula):
    def __init__(self, formula, world=None):
        super().__init__(character="<>", formula_one=formula, formula_two=None, is_atom=False, binary=False, world=world)
        pass

    def branch(self, branch, solver):
        from .diamond import Diamond
        from .negation import Negation
        i = self.world
        j = solver.worlds[len(solver.worlds)-1] + 1
        solver.worlds.append(j)
        solver.relations.append([i, j])

        branch.append(Negation(Diamond(self.formula_one), j))
        self.formula_one.world = j
        branch.append(self.formula_one)

        return branch

    def branch_negated(self, branch, solver):
        from .box import Box
        from .negation import Negation
        branch.append(Box(Negation(self.formula_one), self.world))
        return branch
