class PHPNamespace:
    def __init__(self, name, baseNameSpace, parentNamespace=None):
        self.parentNamespace = parentNamespace
        if parentNamespace is None or parentNamespace == '':
            self.name = name[:name.find('\\')] if name.find('\\') > -1 else name
        else:
            name = name[name.find(parentNamespace) + len(parentNamespace) + 1:]
            self.name = name[:name.find('\\')] if name.find('\\') > -1 else name
        if baseNameSpace is None:
            self.baseNameSpace = self
        else:
            self.baseNameSpace = baseNameSpace
        self.classes = []
        self.subNamespaces = []

    def get_full_namespace_string(self) -> str:
        return self.parentNamespace + '\\' + self.name \
            if self.parentNamespace is not None and self.parentNamespace != '' \
            else self.name

    def __str__(self):
        s = f"\nNamespace: '{self.get_full_namespace_string()}'"
        if len(self.subNamespaces):
            s += f"\nSubnamespaces: "
            for sns in self.subNamespaces:
                s += "'" + sns.get_full_namespace_string() + "', "
        s += "\n"
        if len(self.classes):
            s += f"NS Classes: {self.classes}\n"
        for sns in self.subNamespaces:
            s += sns.__str__()
        return s

    def get_namespace(self, name):
        if name is not None and name.startswith('\\'):
            name = name[1:]
        if name is None or name == self.get_full_namespace_string():
            return self
        for sns in self.subNamespaces:
            if name.startswith(sns.get_full_namespace_string() + "\\") or name == sns.get_full_namespace_string():
                ns = sns.get_namespace(name)
                if ns is not None:
                    return ns
        ns = PHPNamespace(name, self.baseNameSpace, self.get_full_namespace_string())
        self.subNamespaces.append(ns)
        return ns.get_namespace(name)

    def add_class(self, c):
        self.classes.append(c)
        c.namespace = self

    def get_class(self, full_class_name):
        if '\\' in full_class_name:
            ns = self.get_namespace(full_class_name[:full_class_name.rfind('\\')])
            return ns.get_class(full_class_name[full_class_name.rfind('\\') + 1:])
        for c in self.classes:
            if c.name == full_class_name:
                return c
        return None
