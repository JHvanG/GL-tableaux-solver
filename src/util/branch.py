from . import formula, negation


class Box(object):
    def __init__(self, higher_branch, form):
        self.higher_branch = higher_branch
        self.left = None
        self.right = None
        self.active_list = [form]
        self.applied_list = []

    # this function checks whether a formula already exists in the branch
    def check_duplicate(self, form):
        for item in self.active_list:
            if item.equals(form):
                return True
        for item in self.applied_list:
            if item.equals(form):
                return True

        if self.higher_branch:
            return self.higher_branch.check_duplicate(form)
        else:
            return False
        pass

    # this function checks whether a formula causes a contradiction, resulting in the closing of a branch
    def check_contradiction(self, form):
        for item in self.active_list:
            if form.equals(negation.Negation(item, world=item.world)) or item.equals(negation.Negation(form, world=form.world)):
                return True
        for item in self.applied_list:
            if form.equals(negation.Negation(item, world=item.world)) or item.equals(negation.Negation(form, world=form.world)):
                return True

        if self.higher_branch:
            return self.higher_branch.check_contradiction(form)
        else:
            return False
