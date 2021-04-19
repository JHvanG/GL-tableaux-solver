class Generator(object):
    def __init__(self):
        while True:
            self.create_formula()

    def create_formula(self):
        # this function will generate a new formula of same length as last unless all are already present
        # then it will increase in length and check for all connectives again
        # first only with 1 letter

if __name__ == "__main__":
    generator = Generator()