import copy

from data_handler import DataHandler
from tweeter import Tweeter
from util import formula, negation, box, diamond, conjunction, disjunction, implication, bi_implication
import tracemalloc
import itertools
import timeit


class Solver(object):
    def __init__(self):
        self.applied_rules = []
        self.worlds = [0]
        self.relations = []
        self.open_branch = False
        self.new_relation = False
        self.data_handler = DataHandler()
        self.tweeter = Tweeter()

    def reset(self):
        self.applied_rules = []
        self.worlds = [0]
        self.relations = []
        self.open_branch = False
        self.new_relation = False

    # This function removes all non-branches from the branch
    def clear_branch(self, branch):
        emptied_branch = []
        for item in branch:
            if isinstance(item, list):
                emptied_branch.append(item)
        return emptied_branch

    # This function returns True if the formula form is already on the branch, else it returns False
    def already_on_branch(self, form, branch):
        for item in branch:
            if isinstance(item, formula.Formula):
                if item.equals(form):
                    return True
        return False

    # This function applies the transitivity rule to the relations
    def apply_transitivity(self):
        new_relation = None
        all_relations = [item for sublist in self.relations for item in sublist]
        for i,j in itertools.combinations(all_relations, 2):
            if i[1] == j[0]:
                new_relation = [i[0], j[1]]
            elif j[1] == i[0]:
                new_relation = [j[0], i[1]]
            if new_relation:
                found_new = True
                for lst in self.relations:
                    if new_relation in lst:
                        found_new = False
                        break
                if found_new:
                    self.relations[len(self.relations)-1].append(new_relation)

    # This function returns all rules, except for branches on the current branch
    def get_unapplied_rules(self, branch):
        unapplied_rules = []
        for item in branch:
            if not isinstance(item, list):
                new_item = copy.deepcopy(item)
                unapplied_rules.append(new_item)
        return unapplied_rules

    # This function orders the input branch so that all atoms and negated atoms are last to allow the loop to work
    def order_tree(self, branch):
        rank0, rank1, rank2, rank3, rank4, rank5, rank6, rank7 = ([] for i in range(8))

        if branch:
            for form in branch:
                if isinstance(form, formula.Formula):
                    if form.is_atom and form.formula_one == '#':
                        rank0.append(form)
                    elif isinstance(form, conjunction.Conjunction):
                        rank1.append(form)
                    elif isinstance(form, disjunction.Disjunction) or isinstance(form, implication.Implication) or\
                            isinstance(form, bi_implication.BiImplication):
                        rank5.append(form)
                    elif isinstance(form, box.Box):
                        if form.applied_to_all:
                            rank7.append(form)
                        else:
                            rank2.append(form)
                    elif isinstance(form, diamond.Diamond):
                        rank3.append(form)
                    elif isinstance(form, negation.Negation):
                        new_form = form.formula_one
                        if isinstance(new_form, disjunction.Disjunction) or isinstance(new_form, implication.Implication) or\
                                isinstance(new_form, box.Box) or isinstance(new_form, diamond.Diamond) or isinstance(new_form, negation.Negation):
                            rank1.append(form)
                        elif isinstance(new_form, conjunction.Conjunction) or isinstance(new_form, bi_implication.BiImplication):
                            rank5.append(form)
                        elif new_form.is_atom:
                            rank6.append(form)
                    elif form.is_atom:
                        rank6.append(form)
                elif isinstance(form, list):
                    rank4.append(form)
            return rank0 + rank1 + rank2 + rank3 + rank4 + rank5 + rank6 + rank7
        else:
            return None

    # This function returns True if the formula form contradicts with a formula on the branch or in the applied rules
    def contradiction(self, form, branch):
        for item in branch:
            if not isinstance(item, list):
                if form.equals(negation.Negation(item, world=item.world)) or item.equals(negation.Negation(form, world=form.world)):
                    return True
        for lst in self.applied_rules:
            for item in lst:
                if not isinstance(item, list):
                    if form.equals(negation.Negation(item, world=item.world)) or item.equals(
                            negation.Negation(form, world=form.world)):
                        return True
        return False

    # This function is used to check the validity of a branch
    def check_branch(self, branch):
        branch_one_opened = False
        branch_two_opened = False
        branch_one_closed = False
        branch_two_closed = False

        while branch and not self.open_branch:
            if branch_one_closed and branch_two_closed:
                return

            # if a new relation has just been added to the branch, we must check all box formulas again
            if self.new_relation:
                for form in [x for x in branch if isinstance(x, box.Box)]:
                    form.applied_to_all = False
                self.new_relation = False

            branch = self.order_tree(branch)

            if isinstance(branch[0], list) or (branch_one_opened and branch_two_opened):
                self.applied_rules.append([])
                self.relations.append([])
                branch[0] += self.get_unapplied_rules(branch)

                if branch_one_closed:
                    branch = self.clear_branch(branch)

                self.check_branch(branch[0])
                self.applied_rules.remove(self.applied_rules[len(self.applied_rules) - 1])
                self.relations.remove(self.relations[len(self.relations) - 1])

                if self.open_branch:
                    return
                else:
                    if not branch_one_closed:
                        branch_one_closed = True
                    elif not branch_two_closed:
                        branch_two_closed = True
                    branch.remove(branch[0])

            elif isinstance(branch[0], formula.Formula):
                if self.contradiction(branch[0], branch):
                    return
                # a contradiction immediately closes the present branch
                elif branch[0].is_atom and branch[0].formula_one == '#':
                    return
                # apply branch rule
                elif not branch[0].is_atom and not (isinstance(branch[0], negation.Negation) and branch[0].formula_one.is_atom):
                    # Box rules are unique in that they persist in the branch
                    if isinstance(branch[0], box.Box):
                        if not branch[0].applied_to_all:
                            #branch = branch[0].branch(branch, self)
                            new_formulas = branch[0].branch(self)
                            for item in new_formulas:
                                if isinstance(item, formula.Formula) and not self.already_on_branch(item, branch):
                                    if self.contradiction(item, branch):
                                        return
                                    branch.append(item)
                            branch[0].applied_to_all = True
                        else:
                            self.open_branch = True
                            return
                    # for all other connectives, apply the rule, add it to the applied_rules list and remove from the active branch
                    else:
                        new_formulas = branch[0].branch(self)

                        for item in new_formulas:
                            if isinstance(item, formula.Formula) and not self.already_on_branch(item, branch):
                                if self.contradiction(item, branch):
                                    return
                                branch.append(item)
                            elif isinstance(item, list):
                                contains_contradiction = False
                                formulas_to_add = []
                                for form in item:
                                    if isinstance(form, formula.Formula) and not self.already_on_branch(form, branch):
                                        if self.contradiction(form, branch):
                                            contains_contradiction = True
                                            break
                                        else:
                                            formulas_to_add.append(form)
                                if contains_contradiction:
                                    if not branch_one_closed:
                                        branch_one_closed = True
                                    elif not branch_two_closed:
                                        branch_two_closed = True
                                else:
                                    branch.append(formulas_to_add)

                        self.applied_rules[len(self.applied_rules) - 1].append(branch[0])
                        branch.remove(branch[0])

                    for item in branch:
                        if isinstance(item, list):
                            if not branch_one_opened:
                                branch_one_opened = True
                            elif not branch_two_opened:
                                branch_two_opened = True
                else:
                    self.open_branch = True
                    return

    # This is the main function of the solver which negates the input formula and determines the validity
    def solve_formula(self, form):
        #print(form.convert_to_string())
        #print(form.get_length())

        #start_time = timeit.default_timer()
        #tracemalloc.start()

        self.applied_rules.append([])
        self.relations.append([])
        self.check_branch([negation.Negation(form, self.worlds[0])])

        #if self.open_branch:
        #    print("invalid formula")
        #else:
        #    print("valid formula")

        #current, peak = tracemalloc.get_traced_memory()
        #time = timeit.default_timer() - start_time
        #length = form.get_length()

        if not self.open_branch:
            #print(form.convert_to_tweet())
            #self.data_handler.write_memory_data([length, peak])
            #self.data_handler.write_time_data([length, time])
            #self.data_handler.write_tautology([length, form.convert_to_string()])
            self.tweeter.tweet_tautology(form)

        #print(peak)

        #tracemalloc.stop()

        self.reset()


if __name__ == "__main__":
    # valid:
    #test = disjunction.Disjunction(negation.Negation(formula.Formula(None, "A", None, True, False)), formula.Formula(None, "A", None, True, False))
    #test = implication.Implication(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    #test = implication.Implication(box.Box(formula.Formula(None, "A", None, True, False)), box.Box(box.Box(formula.Formula(None, "A", None, True, False))))
    #test = negation.Negation(formula.Formula(None, "#", None, True, False, None, '\u22A5'))
    #test = disjunction.Disjunction(conjunction.Conjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "B", None, True, False)), disjunction.Disjunction(negation.Negation(formula.Formula(None, "A", None, True, False)), negation.Negation(formula.Formula(None, "B", None, True, False))))
    #test = implication.Implication(box.Box(implication.Implication(box.Box(formula.Formula(None, "A", None, True, False)), formula.Formula(None, "A", None, True, False))), box.Box(formula.Formula(None, "A", None, True, False)))
    #test = implication.Implication(diamond.Diamond(formula.Formula(None, "A", None, True, False)), negation.Negation(formula.Formula(None, "#", None, True, False, None, '\u22A5')))
    #test = box.Box(implication.Implication(diamond.Diamond(formula.Formula(None, "#", None, True, False, None, '\u22A5')), conjunction.Conjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))))
    #test = box.Box(disjunction.Disjunction(bi_implication.BiImplication(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False)), box.Box(formula.Formula(None, "A", None, True, False))))
    #test = box.Box(disjunction.Disjunction(bi_implication.BiImplication(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False)), negation.Negation(formula.Formula(None, "B", None, True, False))))

    # invalid:
    #test = conjunction.Conjunction(formula.Formula(None, "A", None, True, False), negation.Negation(formula.Formula(None, "A", None, True, False)))
    #test = disjunction.Disjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))
    #test = box.Box(box.Box(formula.Formula(None, "A", None, True, False)))
    #test = conjunction.Conjunction(disjunction.Disjunction(formula.Formula(None, 'A', None, True, False, None), negation.Negation(formula.Formula(None, 'A', None, True, False, None))), conjunction.Conjunction(conjunction.Conjunction(negation.Negation(formula.Formula(None, "#", None, True, False, None, '\u22A5')),negation.Negation(formula.Formula(None, "#", None, True, False, None, '\u22A5'))), formula.Formula(None, 'A', None, True, False, None)))
    #test = disjunction.Disjunction(conjunction.Conjunction(formula.Formula(None, "#", None, True, False, None, '\u22A5'), formula.Formula(None, "#", None, True, False, None, '\u22A5')), bi_implication.BiImplication(disjunction.Disjunction(formula.Formula(None, 'A', None, True, False, None), formula.Formula(None, 'A', None, True, False, None)), disjunction.Disjunction(formula.Formula(None, "B", None, True, False), formula.Formula(None, "B", None, True, False))))
    #test = implication.Implication(diamond.Diamond(formula.Formula(None, "A", None, True, False)), negation.Negation(formula.Formula(None, 'B', None, True, False, None)))
    #test = conjunction.Conjunction(box.Box(box.Box(diamond.Diamond(bi_implication.BiImplication(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False))))), box.Box(box.Box(diamond.Diamond(box.Box(diamond.Diamond(conjunction.Conjunction(formula.Formula(None, "A", None, True, False), negation.Negation(formula.Formula(None, "A", None, True, False)))))))))

    #test = bi_implication.BiImplication(disjunction.Disjunction(formula.Formula(None, "A", None, True, False), formula.Formula(None, "A", None, True, False)), disjunction.Disjunction(formula.Formula(None, "#", None, True, False, None, '\u22A5'), formula.Formula(None, "A", None, True, False)))

    # TEST SET FROM VAN LOO
    '''
    #WORKS, invalid
    test = negation.Negation(
        bi_implication.BiImplication(
            formula.Formula(None, "A", None, True, False),
            formula.Formula(None, "B", None, True, False)
        )
    )
    '''

    '''
    #WORKS, valid
    test = negation.Negation(
        conjunction.Conjunction(
            box.Box(
                formula.Formula(None, "A", None, True, False)
            ),
            diamond.Diamond(
                negation.Negation(
                    formula.Formula(None, "A", None, True, False)
                )
            )
        )
    )
    '''

    '''
    #WORKS, valid
    test = negation.Negation(
        bi_implication.BiImplication(
            box.Box(
                formula.Formula(None, "A", None, True, False)
            ),
            diamond.Diamond(
                negation.Negation(
                    formula.Formula(None, "A", None, True, False)
                )
            )
        )
    )
    '''

    '''
    #WORKS, invalid
    test = bi_implication.BiImplication(
        box.Box(
            formula.Formula(None, "A", None, True, False)
        ),
        diamond.Diamond(
            negation.Negation(
                formula.Formula(None, "A", None, True, False)
            )
        )
    )
    '''

    '''
    #WORKS, invalid
    test = box.Box(
            bi_implication.BiImplication(
                formula.Formula(None, "A", None, True, False),
                implication.Implication(
                    box.Box(
                        box.Box(
                            box.Box(
                                formula.Formula(None, "#", None, True, False, None, '\u22A5')
                            )
                        )
                    ),
                    box.Box(
                        box.Box(
                            formula.Formula(None, "#", None, True, False, None, '\u22A5')
                        )
                    )
                )
            )
        )
    '''

    '''
    #WORKS, valid
    test = implication.Implication(
        box.Box(
            bi_implication.BiImplication(
                formula.Formula(None, "A", None, True, False),
                implication.Implication(
                    box.Box(
                        disjunction.Disjunction(
                            formula.Formula(None, "A", None, True, False),
                            box.Box(
                                formula.Formula(None, "#", None, True, False, None, '\u22A5')
                            )
                        )
                    ),
                    box.Box(
                        implication.Implication(
                            formula.Formula(None, "A", None, True, False),
                            box.Box(
                                formula.Formula(None, "#", None, True, False, None, '\u22A5')
                            )
                        )
                    )
                )
            )
        ),
        box.Box(
            bi_implication.BiImplication(
                formula.Formula(None, "A", None, True, False),
                implication.Implication(
                    box.Box(
                        box.Box(
                            box.Box(
                                formula.Formula(None, "#", None, True, False, None, '\u22A5')
                            )
                        )
                    ),
                    box.Box(
                        box.Box(
                            formula.Formula(None, "#", None, True, False, None, '\u22A5')
                        )
                    )
                )
            )
        )
    )
    '''

    '''
    #WORKS, INVALID
    test = implication.Implication(
            box.Box(
                box.Box(
                    box.Box(
                        formula.Formula(None, "#", None, True, False, None, '\u22A5')
                    )
                )
            ),
            box.Box(
                box.Box(
                    formula.Formula(None, "#", None, True, False, None, '\u22A5')
                )
            )
        )
    '''

    '''
    #WORKS, valid
    test = disjunction.Disjunction(
        disjunction.Disjunction(
            disjunction.Disjunction(
                disjunction.Disjunction(
                    disjunction.Disjunction(
                        disjunction.Disjunction(
                            box.Box(
                                disjunction.Disjunction(
                                    box.Box(
                                        formula.Formula(None, "A", None, True, False)
                                    ),
                                    box.Box(
                                        diamond.Diamond(
                                            negation.Negation(
                                                formula.Formula(None, "A", None, True, False)
                                            )
                                        )
                                    )
                                )
                            ),
                            diamond.Diamond(
                                box.Box(
                                    formula.Formula(None, "#", None, True, False, None, '\u22A5')
                                )
                            )
                        ),
                        diamond.Diamond(
                            conjunction.Conjunction(
                                box.Box(
                                    formula.Formula(None, "A", None, True, False)
                                ),
                                diamond.Diamond(
                                    diamond.Diamond(
                                        negation.Negation(
                                            formula.Formula(None, "A", None, True, False)
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    diamond.Diamond(
                        conjunction.Conjunction(
                            box.Box(
                                diamond.Diamond(
                                    formula.Formula(None, "A", None, True, False)
                                )
                            ),
                            diamond.Diamond(
                                diamond.Diamond(
                                    box.Box(
                                        negation.Negation(
                                            formula.Formula(None, "A", None, True, False)
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                diamond.Diamond(
                    conjunction.Conjunction(
                        box.Box(
                            formula.Formula(None, "A", None, True, False)
                        ),
                        box.Box(
                            negation.Negation(
                                formula.Formula(None, "A", None, True, False)
                            )
                        )
                    )
                )
            ),
            diamond.Diamond(
                conjunction.Conjunction(
                    box.Box(
                        disjunction.Disjunction(
                            box.Box(
                                negation.Negation(
                                    formula.Formula(None, "A", None, True, False)
                                )
                            ),
                            formula.Formula(None, "A", None, True, False)
                        )
                    ),
                    diamond.Diamond(
                        diamond.Diamond(
                            conjunction.Conjunction(
                                diamond.Diamond(
                                    formula.Formula(None, "A", None, True, False)
                                ),
                                negation.Negation(
                                    formula.Formula(None, "A", None, True, False)
                                )
                            )
                        )
                    )
                )
            )
        ),
        diamond.Diamond(
            conjunction.Conjunction(
                box.Box(
                    disjunction.Disjunction(
                        diamond.Diamond(
                            negation.Negation(
                                formula.Formula(None, "A", None, True, False)
                            )
                        ),
                        formula.Formula(None, "A", None, True, False)
                    )
                ),
                diamond.Diamond(
                    diamond.Diamond(
                        conjunction.Conjunction(
                            box.Box(
                                formula.Formula(None, "A", None, True, False)
                            ),
                            negation.Negation(
                                formula.Formula(None, "A", None, True, False)
                            )
                        )
                    )
                )
            )
        )
    )
    '''


    #DOES NOT PRODUCE AN ANSWER IN REASONABLE TIME
    test = disjunction.Disjunction(
        disjunction.Disjunction(
            conjunction.Conjunction(
                disjunction.Disjunction(
                    conjunction.Conjunction(
                        disjunction.Disjunction(
                            disjunction.Disjunction(
                                box.Box(
                                    disjunction.Disjunction(
                                        box.Box(
                                            formula.Formula(None, "A", None, True, False)
                                        ),
                                        box.Box(
                                            diamond.Diamond(
                                                negation.Negation(
                                                    formula.Formula(None, "A", None, True, False)
                                                )
                                            )
                                        )
                                    )
                                ),
                                diamond.Diamond(
                                    box.Box(
                                        formula.Formula(None, "#", None, True, False, None, '\u22A5')
                                    )
                                )
                            ),
                            diamond.Diamond(
                                conjunction.Conjunction(
                                    box.Box(
                                        formula.Formula(None, "A", None, True, False)
                                    ),
                                    diamond.Diamond(
                                        diamond.Diamond(
                                            negation.Negation(
                                                formula.Formula(None, "A", None, True, False)
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        diamond.Diamond(
                            conjunction.Conjunction(
                                box.Box(
                                    diamond.Diamond(
                                        formula.Formula(None, "A", None, True, False)
                                    )
                                ),
                                diamond.Diamond(
                                    diamond.Diamond(
                                        box.Box(
                                            negation.Negation(
                                                formula.Formula(None, "A", None, True, False)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    diamond.Diamond(
                        conjunction.Conjunction(
                            box.Box(
                                formula.Formula(None, "A", None, True, False)
                            ),
                            box.Box(
                                negation.Negation(
                                    formula.Formula(None, "A", None, True, False)
                                )
                            )
                        )
                    )
                ),
                diamond.Diamond(
                    conjunction.Conjunction(
                        box.Box(
                            disjunction.Disjunction(
                                box.Box(
                                    negation.Negation(
                                        formula.Formula(None, "A", None, True, False)
                                    )
                                ),
                                formula.Formula(None, "A", None, True, False)
                            )
                        ),
                        diamond.Diamond(
                            diamond.Diamond(
                                conjunction.Conjunction(
                                    diamond.Diamond(
                                        formula.Formula(None, "A", None, True, False)
                                    ),
                                    negation.Negation(
                                        formula.Formula(None, "A", None, True, False)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            diamond.Diamond(
                conjunction.Conjunction(
                    box.Box(
                        disjunction.Disjunction(
                            diamond.Diamond(
                                negation.Negation(
                                    formula.Formula(None, "A", None, True, False)
                                )
                            ),
                            formula.Formula(None, "A", None, True, False)
                        )
                    ),
                    diamond.Diamond(
                        diamond.Diamond(
                            conjunction.Conjunction(
                                box.Box(
                                    formula.Formula(None, "A", None, True, False)
                                ),
                                negation.Negation(
                                    formula.Formula(None, "A", None, True, False)
                                )
                            )
                        )
                    )
                )
            )
        ),
        negation.Negation(
            implication.Implication(
                box.Box(
                    bi_implication.BiImplication(
                        formula.Formula(None, "A", None, True, False),
                        implication.Implication(
                            box.Box(
                                disjunction.Disjunction(
                                    formula.Formula(None, "A", None, True, False),
                                    box.Box(
                                        formula.Formula(None, "#", None, True, False, None, '\u22A5')
                                    )
                                )
                            ),
                            box.Box(
                                implication.Implication(
                                    formula.Formula(None, "A", None, True, False),
                                    box.Box(
                                        formula.Formula(None, "#", None, True, False, None, '\u22A5')
                                    )
                                )
                            )
                        )
                    )
                ),
                box.Box(
                    bi_implication.BiImplication(
                        formula.Formula(None, "A", None, True, False),
                        implication.Implication(
                            box.Box(
                                box.Box(
                                    box.Box(
                                        formula.Formula(None, "#", None, True, False, None, '\u22A5')
                                    )
                                )
                            ),
                            box.Box(
                                box.Box(
                                    formula.Formula(None, "#", None, True, False, None, '\u22A5')
                                )
                            )
                        )
                    )
                )
            )
        )
    )


    solver = Solver()
    solver.solve_formula(test)
