from util import formula, negation, box, diamond, conjunction, disjunction, implication, bi_implication
import tracemalloc, itertools


class Solver(object):
    def __init__(self):
        self.tree = []
        self.worlds = [0]
        self.relations = []
        self.applied_rules = []
        self.open_branch = False
        self.new_relation = False

    def reset(self):
        self.tree = []
        self.worlds = [0]
        self.relations = []
        self.applied_rules = []
        self.open_branch = False
        self.new_relation = False

    # This method applies the transitivity rule to the relations
    def apply_transitivity(self):
        '''for relation_a in self.relations:
            for relation_b in self.relations:
                if relation_a != relation_b:
                    if relation_a[0] == relation_b[1]:
                        new_relation = [relation_a[0], relation_b[1]]
                        if new_relation not in self.relations:
                            self.relations.append(new_relation)
                    elif relation_a[1] == relation_b[0]:
                        new_relation = [relation_b[0], relation_a[1]]
                        if new_relation not in self.relations:
                            self.relations.append(new_relation)'''
        new_relation = None
        for i,j in itertools.combinations(self.relations, 2):
            if i[1] == j[0]:
                new_relation = [i[0], j[1]]
            elif j[1] == i[0]:
                new_relation = [j[0], i[1]]
            if new_relation and new_relation not in self.relations:
                self.relations.append(new_relation)



    # This method orders the input branch so that all atoms and negated atoms are last to allow the loop to work
    def order_tree(self, branch):
        rank0, rank1, rank2, rank3, rank4, rank5, rank6 = ([] for i in range(7))

        if branch:
            for form in branch:
                if isinstance(form, formula.Formula):
                    if form.is_atom and form.formula_one == '#':
                        rank0.append(form)
                    elif isinstance(form, conjunction.Conjunction):
                        rank1.append(form)
                    elif isinstance(form, disjunction.Disjunction) or isinstance(form, implication.Implication) or\
                            isinstance(form, bi_implication.BiImplication):
                        rank2.append(form)
                    elif isinstance(form, box.Box):
                        if form.applied_to_all:
                            rank6.append(form)
                        else:
                            rank3.append(form)
                    elif isinstance(form, diamond.Diamond):
                        rank4.append(form)
                    elif isinstance(form, negation.Negation):
                        new_form = form.formula_one
                        if isinstance(new_form, disjunction.Disjunction) or isinstance(new_form, implication.Implication) or\
                                isinstance(new_form, box.Box) or isinstance(new_form, diamond.Diamond) or isinstance(new_form, negation.Negation):
                            rank1.append(form)
                        elif isinstance(new_form, conjunction.Conjunction) or isinstance(new_form, bi_implication.BiImplication):
                            rank2.append(form)
                        elif new_form.is_atom:
                            rank6.append(form)
                    elif form.is_atom:
                        rank6.append(form)
                elif isinstance(form, list):
                    rank5.append(form)
            return rank0 + rank1 + rank2 + rank3 + rank4 + rank5 + rank6
        else:
            return None

    # This method is used to check whether there is a contradiction within the tree
    def has_contradiction(self, branch):
        form = branch[0]
        for item in branch:
            if not isinstance(item, list):
                #if form == negation.Negation(item, world=item.world):
                if form.equals(negation.Negation(item, world=item.world)):
                    return True
                #elif negation.Negation(form, world=form.world) == item:
                elif item.equals(negation.Negation(form, world=form.world)):
                    return True
        for lst in self.applied_rules:
            for item in lst:
                if not isinstance(item, list):
                    #if form == negation.Negation(item, world=item.world):
                    if form.equals(negation.Negation(item, world=item.world)):
                        return True
                    #elif negation.Negation(form, world=form.world) == item:
                    elif item.equals(negation.Negation(form, world=form.world)):
                        return True
        return False

    # This method is used to check the validity of a branch
    def check_branch(self, branch):
        while branch:
            # temporary print statements for debugging
            print('\n\ncurrent:')
            for form in branch:
                if isinstance(form, list):
                    print('branch')
                else:
                    print(form.convert_to_string(), form.world)
            print('\napplied:')
            for lst in self.applied_rules:
                for form in lst:
                    print(form.convert_to_string(), form.world)


            # if a new relation has just been added to the branch, we must check all box formulas again
            if self.new_relation:
                for form in [x for x in branch if isinstance(x, box.Box)]:
                    form.applied_to_all = False
                self.new_relation = False
                branch = self.order_tree(branch)

            if isinstance(branch[0], formula.Formula):
                print('relations:')
                for relation in self.relations:
                    print(relation)
                if self.has_contradiction(branch):
                    return
                # a contradiction immediately closes the present branch
                elif branch[0].is_atom and branch[0].formula_one == '#':
                    return
                # a negated contradiction is always true, hence it can be removed without consequence
                elif isinstance(branch[0], negation.Negation) and branch[0].formula_one.is_atom and branch[0].formula_one.formula_one == '#':
                    branch.remove(branch[0])
                # apply branch rule
                elif not branch[0].is_atom and not (isinstance(branch[0], negation.Negation) and branch[0].formula_one.is_atom):
                    # Box rules are unique in that they persist in the branch
                    if isinstance(branch[0], box.Box):
                        if not branch[0].applied_to_all:
                            branch = branch[0].branch(branch, self)
                            branch[0].applied_to_all = True
                        # if we were to find a box that has been applied to all relations, all rules are applied and
                        # the branch does not close
                        else:
                            # in this case, we encounter an applied box rule without having anything to further the branch
                            self.open_branch = True
                            return
                    # for all other connectives, apply the rule, add it to the applied_rules list and remove from the active branch
                    else:
                        branch = branch[0].branch(branch, self)
                        self.applied_rules[len(self.applied_rules) - 1].append(branch[0])
                        branch.remove(branch[0])
                    # reorganise the branch
                    branch = self.order_tree(branch)
                else:
                    self.open_branch = True
                    return
            elif isinstance(branch[0], list):
                self.applied_rules.append([])
                self.check_branch(branch[0])
                self.applied_rules.remove(self.applied_rules[len(self.applied_rules) - 1])

                # TODO: this is probably not entirely correct
                if self.open_branch:
                    return
                else:
                    branch.remove(branch[0])
                    return

    # This is the main method of the solver which negates the input formula and determines the validity
    def solve_formula(self, form):
        tracemalloc.start()

        self.tree.append(negation.Negation(form, self.worlds[0]))
        self.applied_rules.append([])
        self.check_branch(self.tree)

        if self.open_branch:
            print("invalid formula")
        else:
            print("valid formula")

        current, peak = tracemalloc.get_traced_memory()
        snapshot = tracemalloc.take_snapshot()

        print(current, peak)
        stats = snapshot.statistics('lineno')
        for stat in stats:
            print(stat)

        tracemalloc.stop()

        self.reset()


if __name__ == "__main__":
    #test = conjunction.Conjunction(formula.Formula(None, "A", None, True, False), negation.Negation(formula.Formula(None, "A", None, True, False)))
    #test = disjunction.Disjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    #test = disjunction.Disjunction(negation.Negation(formula.Formula(None, "A", None, True, False)),
                                   #formula.Formula(None, "A", None, True, False))
    #test = implication.Implication(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    #test = implication.Implication(box.Box(formula.Formula(None, "A", None, True, False)), box.Box(box.Box(formula.Formula(None, "A", None, True, False))))
    #test = negation.Negation(formula.Formula(None, '#', None, True, False, None))
    #test = box.Box(box.Box(formula.Formula(None, "A", None, True, False)))
    test = conjunction.Conjunction(disjunction.Disjunction(formula.Formula(None, 'A', None, True, False, None), negation.Negation(formula.Formula(None, 'A', None, True, False, None))), formula.Formula(None, '#', None, True, False, None))
    solver = Solver()
    solver.solve_formula(test)
