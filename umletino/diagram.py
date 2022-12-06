from umletino.element import UmletinoElement


def get_distance_reverse(a, b):
    e = a.umletinoEntity
    p = b.umletinoEntity
    return '0;0;' + str(int(p.x + p.w / 2) - int(e.x + e.w / 2)) \
        + ';' + str(int(p.y - p.h) - int(e.y))


def get_distance(a, b):
    e = a.umletinoEntity
    p = b.umletinoEntity
    return '0;0;' + str(int(p.x + p.w / 2) - int(e.x + e.w / 2)) \
        + ';' + str(int(p.y + p.h) - int(e.y))


class UmletinoDiagram:
    def __init__(self, classes):
        self.entities = []
        self.relations = []
        self.parse(classes)

    def parse(self, classes):
        for c in classes:
            self.entities.append(UmletinoElement(phpc=c))
        for c in classes:
            if c.extends is not None:
                self.relations.append(
                    UmletinoElement(
                        e_id='Relation', panel_attributes='lt=-&gt;&gt;', w=0, h=0,
                        x=int(c.umletinoEntity.x + c.umletinoEntity.w / 2), y=c.umletinoEntity.y,
                        additional_attributes=get_distance(c, c.extends)
                    ))
            for i in c.implements:
                self.relations.append(
                    UmletinoElement(
                        e_id='Relation', panel_attributes=f"lt=.&gt;&gt;", w=0, h=0,
                        x=int(c.umletinoEntity.x + c.umletinoEntity.w / 2), y=c.umletinoEntity.y,
                        additional_attributes=get_distance(c, i)
                    ))
            for a in c.associations:
                self.relations.append(
                    UmletinoElement(
                        e_id='Relation', panel_attributes=f"lt=-&gt;\n{a.name}", w=0, h=0,
                        x=int(c.umletinoEntity.x + c.umletinoEntity.w / 2), y=c.umletinoEntity.y,
                        additional_attributes=get_distance(c, a.phpClass)
                    ))
            for a in c.aggregations:
                self.relations.append(
                    UmletinoElement(
                        e_id='Relation', panel_attributes=f"lt=&lt;&lt;&lt;&lt;-\n{a.name}", w=0, h=0,
                        x=int(c.umletinoEntity.x + c.umletinoEntity.w / 2), y=c.umletinoEntity.y + c.umletinoEntity.h,
                        additional_attributes=get_distance_reverse(c, a.phpClass)
                    ))
            for a in c.compositions:
                self.relations.append(
                    UmletinoElement(
                        e_id='Relation', panel_attributes=f"lt=&lt;&lt;&lt;&lt;&lt;-\n{a.name}", w=0, h=0,
                        x=int(c.umletinoEntity.x + c.umletinoEntity.w / 2), y=c.umletinoEntity.y + c.umletinoEntity.h,
                        additional_attributes=get_distance_reverse(c, a.phpClass)
                    ))

    def __str__(self):
        s = f"<diagram program=\"umletino\" version=\"15.0.0\"><zoom_level>10</zoom_level>"
        for e in self.entities:
            s += e.__str__()
        for r in self.relations:
            s += r.__str__()
        s += "</diagram>"
        return s
