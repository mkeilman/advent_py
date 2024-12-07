from utils.debug import debug

def indices(sub_txt, txt):
    done = False
    s = []
    p = 0
    while not done:
        try:
            p = txt.index(sub_txt, p)
            s.append(p)
            p += 1
        except ValueError:
            done = True
    return s

def re_indices(r, txt):
    import re

    s = []
    q = 0
    t = txt
    m = re.search(r, t)
    while m:
        p = m.span()[0]
        q += p
        s.append(q)
        t = t[p + 1:]
        q += 1
        m = re.search(r, t)
    return s

