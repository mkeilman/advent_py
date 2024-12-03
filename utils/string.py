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
