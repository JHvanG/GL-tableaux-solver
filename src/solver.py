from util import formula, negation, box, diamond, conjunction, disjunction, implication, bi_implication


class Solver(object):
    def __init__(self):
        self.tree = []
        self.worlds = [1]
        self.relations = []
        self.open_branch = False

    # This method applies the transitivity rule to the relations
    def apply_transitivity(self):
        for relation_a in self.relations:
            for relation_b in self.relations:
                if relation_a != relation_b:
                    if relation_a[0] == relation_b[1]:
                        new_relation = [relation_a[0], relation_b[1]]
                        if new_relation not in self.relations:
                            self.relations.append(new_relation)
                    elif relation_a[1] == relation_b[0]:
                        new_relation = [relation_b[0], relation_a[1]]
                        if new_relation not in self.relations:
                            self.relations.append(new_relation)

    # This method orders the input branch so that all atoms and negated atoms are last to allow the loop to work
    def order_tree(self, branch):
        atoms, branches, conjuncts, disjuncts, implications, biimplications, negations, boxes, diamonds = ([] for i in
                                                                                                           range(9))

        #TODO: CHANGE ORDERING

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
                    if form.formula_one.is_atom:
                        atoms.append(form)
                    else:
                        negations.append(form)
                elif isinstance(form, list):
                    branches.append(form)
            return negations + conjuncts + boxes + diamonds + disjuncts + implications + biimplications + branches + atoms
        else:
            return None

    # This method is used to check the validity of a branch
    def check_branch(self, branch):
        # TODO: negation of formula is checked incorrectly at world num
        while branch:
            if isinstance(branch[0], formula.Formula):
                if negation.Negation(branch[0]) in self.tree:
                    return
                elif isinstance(branch[0], negation.Negation) and branch[0].formula_one in self.tree:
                    return
                elif not branch[0].is_atom and not (isinstance(branch[0], negation.Negation) and branch[0].formula_one.is_atom):
                    print(branch[0].convert_to_string(), branch[0].world)
                    branch = branch[0].branch(branch, self)
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
        # TODO: add transitivity
        #       avoid infinite branches
        self.tree.append(negation.Negation(form, self.worlds[0]))

        self.check_branch(self.tree)
        if self.open_branch:
            print("invalid formula")
        else:
            print("valid formula")


if __name__ == "__main__":
    #test = conjunction.Conjunction(formula.Formula(None, "A", None, True, False), negation.Negation(formula.Formula(None, "A", None, True, False)))
    #test = disjunction.Disjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    #test = disjunction.Disjunction(negation.Negation(formula.Formula(None, "A", None, True, False)),
                                   #formula.Formula(None, "A", None, True, False))
    #test = implication.Implication(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    test = implication.Implication(box.Box(formula.Formula(None, "A", None, True, False)), box.Box(box.Box(formula.Formula(None, "A", None, True, False))))
    solver = Solver()
    solver.solve_formula(test)
