class AssumptionManager:
    def __init__(self):
        self.assumptions = {}

    def add_assumption(self, assumption):
        self.assumptions[assumption.name] = assumption

    def get_assumption(self, name):
        return self.assumptions.get(name)

    def update_assumption(self, name, value):
        if name in self.assumptions:
            self.assumptions[name].value = value
            return True
        return False

    def remove_assumption(self, name):
        if name in self.assumptions:
            del self.assumptions[name]
            return True
        return False

    def validate_assumptions(self):
        for name, a in self.assumptions.items():
            if not name:
                raise ValueError("Invalid name")
        return True
