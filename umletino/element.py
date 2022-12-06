px = py = 10
maxh = 0


class UmletinoElement:
    def __init__(self, phpc=None, e_id='UMLClass', w=160, h=50, x=0, y=0,
                 panel_attributes=None, additional_attributes=None):
        global px, py, maxh
        if phpc is not None:
            self.id = 'UMLClass'
            self.w = w
            self.h = h
            self.panel_attributes = phpc.getUMLString()
            self.additional_attributes = ''
            phpc.umletinoEntity = self
            self.x = px
            self.y = py
            if self.h > maxh:
                maxh = self.h
            if px + self.w > 1000:
                px = 10
                py += maxh + 30
            else:
                px += self.w + 30
        else:
            self.id = e_id
            self.w = w
            self.h = h
            self.x = x
            self.y = y
            self.panel_attributes = panel_attributes
            self.additional_attributes = additional_attributes

    def __str__(self):
        return f"<element>" \
               f"<id>{self.id}</id>" \
               f"<coordinates><x>{self.x}</x><y>{self.y}</y><w>{self.w}</w><h>{self.h}</h></coordinates>" \
               f"<panel_attributes>{self.panel_attributes}</panel_attributes>" \
               f"<additional_attributes>{self.additional_attributes}</additional_attributes>" \
               f"</element>"
