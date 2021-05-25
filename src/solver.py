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
        rank1, rank2, rank3, rank4, rank5, rank6 = ([] for i in range(6))

        if branch:
            for form in branch:
                if isinstance(form, conjunction.Conjunction):
                    rank1.append(form)
                elif isinstance(form, disjunction.Disjunction) or isinstance(form, implication.Implication) or isinstance(form, bi_implication.BiImplication):
                    rank2.append(form)
                elif isinstance(form, box.Box):
                    rank3.append(form)
                elif isinstance(form, diamond.Diamond):
                    rank4.append(form)
                elif isinstance(form, negation.Negation):
                    new_form = form.formula_one
                    if isinstance(new_form, disjunction.Disjunction) or isinstance(new_form, implication.Implication):
                        rank1.append(form)
                    elif isinstance(new_form, conjunction.Conjunction) or isinstance(new_form, bi_implication.BiImplication):
                        rank2.append(form)
                    elif isinstance(new_form, diamond.Diamond):
                        rank3.append(form)
                    elif isinstance(new_form, box.Box):
                        rank4.append(form)
                    elif new_form.is_atom:
                        rank6.append(form)
                elif isinstance(form, list):
                    rank5.append(form)
                elif form.is_atom:
                    rank6.append(form)

            return rank1 + rank2 + rank3 + rank4 + rank5 + rank6
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
                    if isinstance(branch[0], box.Box):
                        if not branch[0].is_applied:
                            branch = branch[0].branch(branch, self)
                            branch[0].is_applied = True
                            # TODO: adjust sorting
                            #       reset is_applied booleans when diamond rule is applied
                        else:
                            # in this case, we encounter an applied box rule without having anything to further the branch
                            return
                    else:
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
        #       implement sleep of box operator
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
