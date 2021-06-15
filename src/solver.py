from util import formula, negation, box, diamond, conjunction, disjunction, implication, bi_implication
import tracemalloc, itertools


class Solver(object):
    def __init__(self):
        self.tree = []
        self.applied_rules = []
        self.worlds = [0]
        self.relations = []
        self.depth = 0
        self.open_branch = False
        self.new_relation = False

    def reset(self):
        self.tree = []
        self.applied_rules = []
        self.worlds = [0]
        self.relations = []
        self.open_branch = False
        self.new_relation = False

    # This method applies the transitivity rule to the relations
    def apply_transitivity(self):
        new_relation = None
        for i,j in itertools.combinations(self.relations, 2):
            if i[1] == j[0]:
                new_relation = [i[0], j[1]]
            elif j[1] == i[0]:
                new_relation = [j[0], i[1]]
            if new_relation and new_relation not in self.relations:
                self.relations.append(new_relation)

    def get_unapplied_rules(self, branch, current_depth):
        # TODO: REMOVE RULES FROM CURRENT BRANCH
        unapplied_rules = []
        branch_found = False
        for item in branch:
            if not isinstance(item, list):
                unapplied_rules.append(item)
            elif not branch_found:
                branch_found = True
                current_depth += 1
                if current_depth < self.depth - 1:
                    unapplied_rules += self.get_unapplied_rules(item, current_depth)
        return unapplied_rules

    def update_branch(self, branch, current_depth, altered_branch):
        for item in branch:
            if isinstance(item, list):
                if current_depth == self.depth - 1:
                    branch[branch.index(item)] = altered_branch
                    return branch
                else:
                    current_depth += 1
                    branch[branch.index(item)] = self.update_branch(item, current_depth, altered_branch)
                    return branch

    def update_tree(self, altered_branch):
        if self.depth == 0:
            self.tree = altered_branch
        else:
            for item in self.tree:
                if isinstance(item, list):
                    if self.depth == 1:
                        self.tree[self.tree.index(item)] = altered_branch
                        break
                    else:
                        self.update_branch(item, 1, altered_branch)

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
                    # make rank 5 rank 2
            return rank0 + rank1 + rank5 + rank2 + rank3 + rank4 + rank6
        else:
            return None

    # This method is used to check whether there is a contradiction within the tree
    def has_contradiction(self, form, branch):
        for item in branch:
            if not isinstance(item, list):
                if form.equals(negation.Negation(item, world=item.world)) or item.equals(negation.Negation(form, world=form.world)):
                    return True
            else:
                return self.has_contradiction(form, item)
        for lst in self.applied_rules:
            for item in lst:
                if not isinstance(item, list):
                    if form.equals(negation.Negation(item, world=item.world)) or item.equals(negation.Negation(form, world=form.world)):
                        return True
        return False

    # This method is used to check the validity of a branch
    def check_branch(self, branch):
        branch_one_opened = False
        branch_two_opened = False
        branch_one_closed = False
        branch_two_closed = False

        while branch and not self.open_branch:
            self.update_tree(branch)

            if branch_one_closed and branch_two_closed:
                return

            # temporary print statements for debugging
            print(self.tree)
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

            if isinstance(branch[0], list) or (branch_one_opened and branch_two_opened):

                self.applied_rules.append([])
                self.depth += 1
                # TODO: MOVE BRANCHES TO ONE
                branch[0] += self.get_unapplied_rules(self.tree, 0)
                self.check_branch(branch[0])
                self.depth -= 1
                self.applied_rules.remove(self.applied_rules[len(self.applied_rules) - 1])

                if self.open_branch:
                    return
                else:
                    if not branch_one_closed:
                        branch_one_closed = True
                    elif not branch_two_closed:
                        branch_two_closed = True
                    branch.remove(branch[0])

            elif isinstance(branch[0], formula.Formula):
                if self.has_contradiction(branch[0], self.tree):
                    return
                # a contradiction immediately closes the present branch
                elif branch[0].is_atom and branch[0].formula_one == '#':
                    return
                # apply branch rule
                elif not branch[0].is_atom and not (isinstance(branch[0], negation.Negation) and branch[0].formula_one.is_atom):
                    # Box rules are unique in that they persist in the branch
                    if isinstance(branch[0], box.Box):
                        if not branch[0].applied_to_all:
                            branch = branch[0].branch(branch, self)
                            branch[0].applied_to_all = True
                        else:
                            self.open_branch = True
                            return
                    # for all other connectives, apply the rule, add it to the applied_rules list and remove from the active branch
                    else:
                        branch = branch[0].branch(branch, self)
                        self.applied_rules[len(self.applied_rules) - 1].append(branch[0])
                        branch.remove(branch[0])
                    # reorganise the branch
                    branch = self.order_tree(branch)

                    print('checking branch: ', branch)
                    for item in branch:
                        if isinstance(item, list):
                            print('found one')
                            if not branch_one_opened:
                                print('one')
                                branch_one_opened = True
                            elif not branch_two_opened:
                                print('two')
                                branch_two_opened = True
                else:
                    self.open_branch = True
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
    #test = disjunction.Disjunction(negation.Negation(formula.Formula(None, "A", None, True, False)), formula.Formula(None, "A", None, True, False))
    #test = implication.Implication(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    #test = implication.Implication(box.Box(formula.Formula(None, "A", None, True, False)), box.Box(box.Box(formula.Formula(None, "A", None, True, False))))
    #test = negation.Negation(formula.Formula(None, '#', None, True, False, None))
    #test = box.Box(box.Box(formula.Formula(None, "A", None, True, False)))
    #test = conjunction.Conjunction(disjunction.Disjunction(formula.Formula(None, 'A', None, True, False, None), negation.Negation(formula.Formula(None, 'A', None, True, False, None))), conjunction.Conjunction(conjunction.Conjunction(negation.Negation(formula.Formula(None, '#', None, True, False, None)),negation.Negation(formula.Formula(None, '#', None, True, False, None))), formula.Formula(None, 'A', None, True, False, None)))
    #test = disjunction.Disjunction(conjunction.Conjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "B", None, True, False)), disjunction.Disjunction(negation.Negation(formula.Formula(None, "A", None, True, False)), negation.Negation(formula.Formula(None, "B", None, True, False))))
    #test = implication.Implication(box.Box(implication.Implication(box.Box(formula.Formula(None, "A", None, True, False)), formula.Formula(None, "A", None, True, False))), box.Box(formula.Formula(None, "A", None, True, False)))
    test = disjunction.Disjunction(conjunction.Conjunction(formula.Formula(None, '#', None, True, False, None), formula.Formula(None, '#', None, True, False, None)), bi_implication.BiImplication(disjunction.Disjunction(formula.Formula(None, 'A', None, True, False, None), formula.Formula(None, 'A', None, True, False, None)), disjunction.Disjunction(formula.Formula(None, "B", None, True, False), formula.Formula(None, "B", None, True, False))))
    solver = Solver()
    solver.solve_formula(test)
