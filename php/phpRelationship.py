class PHPRelationship:
    def __init__(self, phpClass, name, rel_type='association'):
        self.phpClass = phpClass
        self.name = name
        self.type = rel_type

    def __str__(self):
        return f"Relationship ({self.type}) with class {self.phpClass.get_full_name()} (name: {self.name})"
