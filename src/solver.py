from util import formula, negation, box, diamond, conjunction, disjunction, implication, bi_implication


class Solver(object):
    def __init__(self):
        self.tree = []
        self.worlds = [1]
        self.relations = []
        self.open_branch = False

    # This method orders the input branch so that all atoms and negated atoms are last to allow the loop to work
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

    # This method returns True when all rules in the branch are applied and False if not
    '''
    def all_rules_applied(self, branch):
        for rule in branch:
            if isinstance(rule, list):
                return False
            elif isinstance(rule, negation.Negation) or isinstance(rule, box.Box) or isinstance(rule, diamond.Diamond):
                if not rule.get_formula_one().get_is_atom():
                    return False
            elif (isinstance(rule, conjunction.Conjunction) or isinstance(rule, disjunction.Disjunction)
                  or isinstance(rule, implication.Implication) or isinstance(rule, bi_implication.BiImplication)):
                return False
        return True
    '''

    # This method is used to check the validity of a branch
    def check_branch(self, branch):
        while branch:
            #if self.all_rules_applied(branch):
            #    self.open_branch = True
            #    return
            if isinstance(branch[0], formula.Formula):
                if negation.Negation(branch[0]) in self.tree:
                    return
                elif isinstance(branch[0], negation.Negation) and branch[0].get_formula_one() in self.tree:
                    return
                elif not branch[0].is_atom and not (isinstance(branch[0], negation.Negation) and branch[0].formula_one.is_atom):
                    print(branch)
                    branch = branch[0].branch(branch)
                    branch.remove(branch[0])
                    self.order_tree(branch)
                else:
                    self.open_branch = True
                    return
            elif isinstance(branch[0], list):
                self.check_branch(branch[0])
                if self.open_branch:
                    return
                else:
                    branch.remove(branch[0])
                    return

    # This is the main method of the solver which negates the input formula and determines the validity
    def solve_formula(self, form):
        # add possibility for world
        self.tree.append(negation.Negation(form))

        self.check_branch(self.tree)
        if self.open_branch:
            print("invalid formula")
        else:
            print("valid formula")


if __name__ == "__main__":
    test = conjunction.Conjunction(formula.Formula(None, "A", None, True, False), negation.Negation(formula.Formula(None, "A", None, True, False)))
    #test = disjunction.Disjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    #test = disjunction.Disjunction(negation.Negation(formula.Formula(None, "A", None, True, False)),
                                   #formula.Formula(None, "A", None, True, False))
    solver = Solver()
    solver.solve_formula(test)
