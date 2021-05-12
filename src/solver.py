from util import formula, negation, box, diamond, conjunction, disjunction, implication, bi_implication


class Solver(object):
    def __init__(self):
        self.tree = []
        self.worlds = [1]
        self.relations = []
        self.valid = False

    # This method checks an entire branch on completeness
    def check_branch(self, branch):
        # this goes over the entire branch. Upon return the branch is deleted, we can reuse code here!
        branch_list = branch

    def order_tree(self, branch):
        atoms, branches, conjuncts, disjuncts, implications, biimplications, negations, boxes, diamonds = ([] for i in
                                                                                                           range(9))

        if branch:
            for form in branch:
                if isinstance(form, conjunction.Conjunction):
                    conjuncts.append(form)
                elif isinstance(form, disjunction.Disjunction):
                    disjuncts.append(form)
                elif isinstance(form, implication.Implication):
                    implications.append(form)
                elif isinstance(form, bi_implication.BiImplication):
                    biimplications.append(form)
                elif isinstance(form, box.Box):
                    boxes.append(form)
                elif isinstance(form, diamond.Diamond):
                    diamonds.append(form)
                elif isinstance(form, negation.Negation):
                    if form.get_formula_one().get_is_atom():
                        atoms.append(form)
                    else:
                        negations.append(form)
                elif isinstance(form, list):
                    branches.append(form)

            return negations + conjuncts + boxes + diamonds + disjuncts + implications + biimplications + branches + atoms

        else:
            return None

    def all_rules_applied(self):
        for rule in self.tree:
            if isinstance(rule, list):
                return False
            elif isinstance(rule, negation.Negation) or isinstance(rule, box.Box) or isinstance(rule, diamond.Diamond):
                if not rule.get_formula_one().get_is_atom():
                    return False
            elif (isinstance(rule, conjunction.Conjunction) or isinstance(rule, disjunction.Disjunction)
                  or isinstance(rule, implication.Implication) or isinstance(rule, bi_implication.BiImplication)):
                return False

        return True

    def solve_formula(self, form):
        # add possibility for world
        self.tree.append(negation.Negation(form))

        while not self.valid:
            if not self.tree:
                self.valid = True
            elif self.all_rules_applied():
                break
            elif isinstance(self.tree[0], formula.Formula):
                next_rule = self.tree[0]

                if negation.Negation(next_rule) in self.tree:
                    self.valid = True
                elif isinstance(next_rule, negation.Negation) and next_rule.get_formula_one() in self.tree:
                    self.valid = True
                elif not next_rule.get_is_atom():
                    print(self.tree)
                    self.tree = next_rule.branch(self.tree)
                    self.tree.remove(next_rule)
                    self.order_tree(self.tree)
            else:
                self.check_branch(self.tree[0])
                self.tree.remove(self.tree[0])

        if self.valid:
            print("yes!")


if __name__ == "__main__":
    # test = conjunction.Conjunction(formula.Formula(None, "A"), negation.Negation(formula.Formula(None, "A")))
    test = conjunction.Conjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    solver = Solver()
    solver.solve_formula(test)
