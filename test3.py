if __name__ == '__main__':

    # l = [5, 3, 0]
    # scores = set()
    # for a in l:
    #     for b in l:
    #         for c in l:
    #             for d in l:
    #                 for e in l:
    #                     for f in l:
    #                         for g in l:
    #                             for h in l:
    #                                 for i in l:
    #                                     for j in l:
    #                                         scores.add(sum([a, b, c, d, e, f, g, h, i, j]))
    # print(scores)
    # print(len(scores))

    scores = set()
    for n in range(0, 11):
        for m in range(0, 11-n):
            scores.add(3*n + 5*m)
    print(scores)
    print(len(scores))

