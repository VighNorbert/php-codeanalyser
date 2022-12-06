from php.phpDesignPattern import PHPDesignPattern
from php.phpRelationship import PHPRelationship


class PHPProperty:
    def __init__(self, definition, parentClass):
        split = definition.strip(' ').split(' ')
        if len(split) > 1:
            self.name = split[1]
            if 'a' <= split[0].strip('?')[0] <= 'z':
                self.type = split[0]
                if self.type == 'array':
                    a = parentClass.identify_aggregation_type(self.name.strip('$'))
                    if a is not None:
                        if parentClass.is_extending(a.phpClass) or parentClass == a.phpClass:
                            dp = PHPDesignPattern('Composite')
                            dp.add(parentClass, 'Composite')
                            if parentClass != a.phpClass:
                                dp.add(a.phpClass, 'Component')
                            for child in a.phpClass.children:
                                if child != parentClass:
                                    dp.add(child, 'Leaf')
                        parentClass.add_association(a)
            else:
                self.type = parentClass.identify_class(split[0].strip('?'))
                if self.type is not None:
                    parentClass.add_association(PHPRelationship(self.type, self.name.strip('$')))
        else:
            self.type = None
            self.name = split[0]

    def __str__(self):
        if self.type is None:
            return f"Property: {self.name}"
        if isinstance(self.type, str):
            return f"Property: {self.name} of type {self.type}"
        return f"Property: {self.name} of class {self.type.get_full_name()}"
