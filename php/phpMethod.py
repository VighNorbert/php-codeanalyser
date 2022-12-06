class PHPMethod:
    def __init__(self, name, definition):
        self.name = name
        self.definition = definition
        self.params = self.__get_params()

    def __str__(self):
        return f"\tMethod: {self.name}\n" \
               f"\tParameters: {self.params}\n"

    def __get_params(self):
        params = []
        if self.definition.find('(') > -1:
            params = list(map(
                lambda x: x.strip(),
                self.definition[self.definition.find('(') + 1:self.definition.find(')')].split(',')
            ))
        if len(params) == 1 and params[0] == '':
            return []
        return params
