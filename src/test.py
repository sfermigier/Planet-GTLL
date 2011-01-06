class A:
    def __repr__(self):
        return "<A %s>" % getattr(self, "a", None)

def t():
    l = [A(), A(), A()]
    d = {}
    for x in l:
        d[0] = d.get(0, ()) + (x,)

    l1 = d.items()
    l1.sort(lambda x, y: -cmp(x[0], y[0]))
    for date, e1 in l1:
        e1[0].a = date

    print l
    return l

def q():
    l = t()
    print l
    print l[0].a

q()
