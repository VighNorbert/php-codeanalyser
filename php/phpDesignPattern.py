design_patterns = []


class PHPDesignPattern:
    def __init__(self, name):
        self.classMap = {}
        self.name = name
        design_patterns.append(self)

    def add(self, phpClass, name):
        self.classMap[name] = phpClass

    def __str__(self):
        s = f"Design pattern ({self.name}) represented by classes:\n"
        s += '\n'.join([f"\t{k}: {v.get_full_name()}" for k, v in self.classMap.items()])
        return s
