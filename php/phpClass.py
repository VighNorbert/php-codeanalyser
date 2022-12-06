from php.phpMethod import PHPMethod
from php.phpNamespace import PHPNamespace
from php.phpProperty import PHPProperty
from php.phpRelationship import PHPRelationship


def get_next_word(split_line, word):
    return split_line[split_line.index(word) + 1]


def find_common_superclass(class1, class2):
    if class1 is None or class2 is None:
        return None
    if class1 == class2:
        return class1
    if class1.is_extending(class2):
        return class2
    if class2.is_extending(class1):
        return class1
    return find_common_superclass(class1.extends, class2)


base_namespace = PHPNamespace('', None)


class PHPClass:
    def __init__(self, filename, parse=True):
        self.filename = filename
        self.name = None
        self.type = None
        self.namespace = None
        self.extends = None
        self.children = []
        self.implements = []
        self.methods = []
        self.properties = []
        self.imports = []
        self.otherClassesInFile = []
        self.associations = []
        self.aggregations = []
        self.compositions = []
        self.umletinoEntity = None
        self.activeClass: PHPClass = self
        if parse:
            self.parse()
            if self.name is not None:
                base_namespace.get_namespace(self.namespace).add_class(self)
                for sc in self.otherClassesInFile:
                    base_namespace.get_namespace(sc.namespace).add_class(sc)

    def is_extending(self, c):
        if self.extends is None:
            return False
        if self.extends == c:
            return True
        return self.extends.is_extending(c)

    def get_full_name(self):
        return f"{self.namespace.get_full_namespace_string()}\\{self.name}"

    def getUMLString(self):
        s = ''
        if self.type == 'interface':
            s += f'&lt;&lt;Interface&gt;&gt;\n'
        elif self.type == 'abstract':
            s += f'&lt;&lt;Abstract&gt;&gt;\n'
        elif self.type == 'final':
            s += f'&lt;&lt;Final&gt;&gt;\n'
        s += f'{self.name}'
        return s

    def __str__(self):
        s = f"Class" if self.type == 'class' else f"Interface" if self.type == 'interface' else f"Abstract class" \
            if self.type == 'abstract' else 'Final class'
        s += f": {self.namespace.get_full_namespace_string()}\\{self.name}\n"
        try:
            s += f"Extends: {self.extends.namespace.get_full_namespace_string()}\\{self.extends.name}\n"
        except AttributeError:
            s += f"Extends: {self.extends}\n"
        s += f"Implements: {self.implements}\n" \
             f"Methods:\n"
        for m in self.methods:
            s += f"{m}\n"
        s += f"Properties:\n"
        for p in self.properties:
            s += f"\t{p}\n"
        s += f"Associations:\n"
        for a in self.associations:
            s += f"\t{a}\n"
        s += f"Aggregations:\n"
        for a in self.aggregations:
            s += f"\t{a}\n"
        s += f"Compositions:\n"
        for c in self.compositions:
            s += f"\t{c}\n"
        s += f"Imports: {self.imports}\n"
        return s

    def read(self):
        try:
            with open(self.filename, 'r', encoding="utf8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def parse(self):
        lines = self.read().splitlines()
        prev_line = None
        for line in lines:
            if prev_line is not None:
                line = prev_line + ' ' + line
            line = line.strip()
            split_line = line.split(' ')
            prev_line = None
            if line.startswith('*') or line.startswith('//') or line.startswith('#') or line.startswith('/*'):
                continue
            try:
                if 'namespace' in split_line:
                    self.activeClass.namespace = get_next_word(split_line, 'namespace').strip(';')
                if line.startswith('class ') or line.startswith('abstract class ') or line.startswith('final class '):
                    if self.activeClass.name is not None:
                        self.activeClass = PHPClass(self.filename, False)
                        self.activeClass.namespace = self.namespace
                        self.activeClass.imports = self.imports
                        self.otherClassesInFile.append(self.activeClass)
                    self.activeClass.name = get_next_word(split_line, 'class')
                    self.activeClass.type = line.split(' ')[0]
                elif line.startswith('interface '):
                    if self.activeClass.name is not None:
                        self.activeClass = PHPClass(self.filename, False)
                        self.activeClass.namespace = self.namespace
                        self.activeClass.imports = self.imports
                        self.otherClassesInFile.append(self.activeClass)
                    self.activeClass.name = get_next_word(split_line, 'interface')
                    self.activeClass.type = 'interface'
                if 'use' in split_line and self.activeClass.name is None:
                    self.activeClass.imports.append(get_next_word(split_line, 'use').strip(';'))
                if 'implements' in split_line:
                    for w in split_line[split_line.index('implements') + 1:]:
                        if '{' in w:
                            break
                        self.activeClass.implements.append(w.strip(','))
                if 'extends' in split_line:
                    self.activeClass.extends = get_next_word(split_line, 'extends')

                if 'function' in split_line:
                    if '{' not in line and ';' not in line:
                        prev_line = line
                    elif '{' in line:
                        m = PHPMethod(get_next_word(split_line, 'function').split('(')[0], line[:line.index('{')])
                        self.activeClass.methods.append(m)
                    else:
                        m = PHPMethod(get_next_word(split_line, 'function').split('(')[0], line[:line.index(';')])
                        self.activeClass.methods.append(m)
                elif line.startswith('public') or line.startswith('private') or line.startswith('protected'):
                    self.activeClass.properties.append(line[line.index(' ') + 1:].split('=')[0].strip(';'))
            except IndexError:
                prev_line = line

    def identify_classes(self):
        if self.extends is not None:
            self.extends = base_namespace.get_class(self.__get_full_name_of_class(self.extends))
            if self.extends is not None:
                self.extends.children.append(self)

    def advanced_parsing(self):
        interfaces = []
        for i in self.implements:
            i = base_namespace.get_class(self.__get_full_name_of_class(i))
            if i is not None:
                interfaces.append(i)
        self.implements = interfaces
        properties = []
        for p in self.properties:
            properties.append(PHPProperty(p, self))
        self.properties = properties

    def identify_class(self, className):
        return base_namespace.get_class(self.__get_full_name_of_class(className))

    def __get_full_name_of_class(self, name):

        for imp in self.imports:
            if name == imp.split('\\')[-1]:
                return imp
            if name.split('\\')[0] == imp.split('\\')[-1]:
                return imp + '\\' + '\\'.join(name.split('\\')[1:])
        if '\\' in name:
            return name
        return self.namespace.get_full_namespace_string() + '\\' + name

    def add_association(self, association: PHPRelationship):
        if association is None:
            return
        if association.type == 'association':
            self.associations.append(association)
        elif association.type == 'aggregation':
            self.aggregations.append(association)
        elif association.type == 'composition':
            self.compositions.append(association)

    def identify_aggregation_type(self, rel_name: str):
        lines = self.read().splitlines()
        s1 = "$this->" + rel_name + '['
        possible_type = 'composition'
        included_classes = []
        for i, line in enumerate(lines):
            if s1 in line and '=' in line and ';' in line:
                contents = line[line.index('=') + 1:line.index(';')].strip()
                if contents.startswith('new '):
                    c = self.identify_class(contents[4:contents.index('(')])
                    included_classes.append(c)
                elif contents.startswith('$'):
                    a = self.identify_type_of_variable(contents.split(' ')[0], i)
                    if a is not None:
                        included_classes.append(a.phpClass)
                        if possible_type == 'composition' and a.type == 'aggregation':
                            possible_type = a.type
        if len(included_classes) == 0:
            return None
        while len(included_classes) > 1:
            if included_classes[0] == included_classes[1]:
                included_classes.pop(0)
                continue
            c0 = included_classes.pop(0)
            c1 = included_classes.pop(0)
            common = find_common_superclass(c0, c1)
            if common is None:
                return None
            included_classes.append(common)

        return PHPRelationship(included_classes[0], rel_name, possible_type)

    def identify_type_of_variable(self, varname, line_index):
        lines = self.read().splitlines()[line_index - 1:0:-1]
        for line in lines:
            if varname in line:
                line_substr = line[line.index(varname) + len(varname):].strip()
                if line_substr.startswith('= '):
                    line_substr = line_substr[2:].strip()
                    if line_substr.startswith('new '):
                        c = self.identify_class(line_substr[4:line_substr.index('(')])
                        return PHPRelationship(c, varname, 'composition')
                    else:
                        return None
                elif 'function' in line:
                    c_name = line[0:line.index(varname)].strip(' ').split(' ')[-1].strip()
                    if '(' in c_name:
                        c_name = c_name[c_name.index('(') + 1:]
                    if 'function' in line and len(c_name) and c_name[-1] != ',':
                        return PHPRelationship(self.identify_class(c_name), varname, 'aggregation')
        return None
