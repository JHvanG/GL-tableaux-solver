from .formula import Formula


class Box(Formula):
    def __init__(self, formula, world=None):
        super().__init__(character="[]", formula_one=formula, formula_two=None, is_atom=False, binary=False, world=world)
        self.applied_relations = []
        self.applied_to_all = False
        pass

    def branch(self, branch, solver):
        i = self.world
        # TODO: what if there is no unapplied rule? -> if box is last rule before atoms, remove box rule
        for relation in solver.relations:
            if relation[0] == i and relation not in self.applied_relations:
                j = relation[1]

                self.applied_relations.append([i, j])
                branch.append(Box(self.formula_one, j))
                self.formula_one.world = j
                branch.append(self.formula_one)

        return branch

    def branch_negated(self, branch, solver):
        from .diamond import Diamond
        from .negation import Negation
        branch.append(Diamond(Negation(self.formula_one), self.world))
        return branch
