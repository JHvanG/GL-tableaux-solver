from util import negation, conjunction
from util import formula
from util import connective_enum
from pathlib import Path
import pickle, os


class Generator(object):
    def __init__(self):
        self.total_length = 1
        self.position = 0
        self.generator_on = False
        self.formula_complexity = 0
        self.storage_path = os.path.join(Path(__file__).parents[1], "storage")

    def set_generator_on(self, value):
        self.generator_on = value

    def get_total_length(self):
        return self.total_length

    def set_total_length(self, new_length):
        self.total_length = new_length

    # this method is responsible for keeping the resulting formula up to date
    def update_resulting_formula(self, filler):
        if self.resulting_formula is None:
            self.resulting_formula = filler
        else:
            self.resulting_formula.fill_in(filler)

    # this method checks whether a complete formula is produced and prints if that is the case
    def check_complete(self):
        if self.position == self.total_length:
            print(self.resulting_formula.convert_to_string())
            # TODO: remove the last formula, either through a method or by setting a boolean
            """
            for this a method needs to be designed that removes the deepest nested connective
                for binary connectives this should go right unless this is none, then left should be investigated
                if both are None, remove the connective itself and return
                for unary connectives this should only remove itself if its formula is None
            """

    # This method is responsible for saving the formulas a .form file using pickle
    def save_to_file(self, formula_list):
        filepath = os.path.join(self.storage_path, "formula_set_" + str(self.formula_complexity) + ".form")
        with open(filepath, 'wb') as file:
            for form in formula_list:
                pickle.dump(form, file, pickle.HIGHEST_PROTOCOL)

    def read_from_file(self):
        filepath = os.path.join(self.storage_path, "formula_set_" + str(self.formula_complexity) + ".form")
        with open(filepath, 'rb') as file:
            while True:
                try:
                    print(pickle.load(file))
                except EOFError:
                    break

    # This method will produce and save the two atoms A and B
    def generate_atoms(self):
        atom_one = formula.Formula(None, "A", None, True, False)
        atom_two = formula.Formula(None, "B", None, True, False)
        formula_list = [atom_one, atom_two]
        self.save_to_file(formula_list)

    # This method will produce and save combinations of the previously saved formulas
    def generate_combinations(self):
        if self.formula_complexity == 1:
            ''' 
        Complexity 1:
            - Unary connectives ~, [] and <> on complexity 0
        Complexity 2:
            - Binary connectives &, |, -> and <-> on complexity 0
            - Unary connectives ~, [] and <> on complexity 1
        Complexity 3:
            - Binary connectives on complexity combination of 0 with 2 and combination of 1 with 1
            - Unary connectives on binary connectives and single unary connectives of complexity 2        
        '''

    # TODO: Fix method to procedurally generate increasing combinations of past formulae.
    #       Using pickle save past formulae
    def create_formula(self):
        self.generate_atoms()
        self.read_from_file()
        #while self.generator_on:
        #    if self.formula_complexity == 0:
        #        self.generate_atoms()
        #    else:
        #        self.generate_combinations()

            #self.formula_complexity += 1


if __name__ == "__main__":
    generator = Generator()
    generator.set_generator_on(True)
    generator.create_formula()
