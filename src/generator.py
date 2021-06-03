from src.solver import Solver
from util import formula, negation, box, diamond, disjunction, conjunction, implication, bi_implication
from util.connective_enum import ConnectiveType
from pathlib import Path
import pickle, os


class Generator(object):
    def __init__(self):
        self.within_length = False
        self.position = 0
        self.generator_on = False
        self.formula_complexity = 0
        self.storage_path = os.path.join(Path(__file__).parents[1], "storage")
        self.solver = Solver()

    # This method is responsible for saving the formulas a .form file using pickle
    def save_to_file(self, formula_list):
        filepath = os.path.join(self.storage_path, "formula_set_" + str(self.formula_complexity) + ".form")
        with open(filepath, 'wb') as file:
            for form in formula_list:
                print(form.convert_to_string())
                pickle.dump(form, file, pickle.HIGHEST_PROTOCOL)

    def read_from_file(self, filepath):
        formulas = []
        with open(filepath, 'rb') as file:
            while True:
                try:
                    temp = pickle.load(file)
                    if isinstance(temp, formula.Formula):
                        formulas.append(temp)
                except EOFError:
                    return formulas

    # This method returns a list of all unary connectives based on the formulas of the previous complexity
    def create_unary_connectives(self, n):
        connectives = [ConnectiveType.NEGATION, ConnectiveType.BOX, ConnectiveType.DIAMOND]

        filepath = os.path.join(self.storage_path, "formula_set_" + str(n) + ".form")
        previous_formulas = self.read_from_file(filepath)

        formula_list = []
        for connective in connectives:
            for form in previous_formulas:
                new_form = None
                if connective == ConnectiveType.NEGATION:
                    new_form = negation.Negation(form)
                elif connective == ConnectiveType.BOX:
                    new_form = box.Box(form)
                elif connective == ConnectiveType.DIAMOND:
                    new_form = diamond.Diamond(form)

                # solve each new formula right away
                self.solver.solve_formula(new_form)
                formula_list.append(new_form)

        return formula_list

    # This method returns a list of all binary connectives based on the formulas of the previous complexity
    def create_binary_connectives(self, min, max):
        binary_connectives = [ConnectiveType.CONJUNCTION, ConnectiveType.DISJUNCTION,
                              ConnectiveType.IMPLICATION, ConnectiveType.BIIMPLICATION]
        filepath_min = os.path.join(self.storage_path, "formula_set_" + str(min) + ".form")
        filepath_max = os.path.join(self.storage_path, "formula_set_" + str(max) + ".form")

        previous_formulas_min = self.read_from_file(filepath_min)
        previous_formulas_max = self.read_from_file(filepath_max)

        formula_list = []

        for connective in binary_connectives:
            for form_a in previous_formulas_min:
                index_a = previous_formulas_min.index(form_a)
                for form_b in previous_formulas_max:
                    index_b = previous_formulas_max.index(form_b)
                    if index_a > index_b:
                        if connective == ConnectiveType.IMPLICATION:
                            formula_list.append(implication.Implication(form_a, form_b))
                    else:
                        if connective == ConnectiveType.CONJUNCTION:
                            formula_list.append(conjunction.Conjunction(form_a, form_b))
                        elif connective == ConnectiveType.DISJUNCTION:
                            formula_list.append(disjunction.Disjunction(form_a, form_b))
                        elif connective == ConnectiveType.IMPLICATION:
                            formula_list.append(implication.Implication(form_a, form_b))
                        elif connective == ConnectiveType.BIIMPLICATION:
                            formula_list.append(bi_implication.BiImplication(form_a, form_b))

                    # solve each new formula right away
                    self.solver.solve_formula(formula_list[len(formula_list) - 1])

        return formula_list

    # This method will produce and save the two atoms A and B
    def generate_atoms(self):
        # TODO: include contradiction as well!

        atom_one = formula.Formula(None, "A", None, True, False)
        atom_two = formula.Formula(None, "B", None, True, False)
        atom_three = formula.Formula(None, "#", None, True, False)
        formula_list = [atom_one, atom_two, atom_three]
        self.save_to_file(formula_list)

    # This method will produce and save combinations of the previously saved formulas
    def generate_combinations(self):
        """
        unary: ~, [], <>
        binary: &, |, ->, <->
        Complexity 1: unary on {0} and binary on {0,0}
        Complexity 2: unary on {1} and binary on {0,1} and {1,1}
        Complexity 3: unary on {2} and binary on {0,2}, {1,2} and {2,2}
        """

        min = 0
        max = self.formula_complexity - 1

        new_formulas = self.create_unary_connectives(max)

        while min <= max:
            new_formulas += self.create_binary_connectives(min, max)
            min += 1

        for form in new_formulas:
            self.solver.solve_formula(form)

        self.save_to_file(new_formulas)

    def check_length(self, form):
        # TODO: have all elements be one character in the string representation
        if len(form.convert_to_string()) <= 280:
            self.within_length = True

    def create_formula(self):
        while self.generator_on:
            if self.formula_complexity == 0:
                self.generate_atoms()
            else:
                self.generate_combinations()

            self.formula_complexity += 1


if __name__ == "__main__":
    generator = Generator()
    generator.generator_on = True
    generator.create_formula()
