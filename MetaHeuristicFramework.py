

MaxSearches = 10000


def IteratedLocalSearch(f, N, L, S):
    s = GenerateInitialSolution()
    s_star = s
    for k in MaxSearches:
        s = LocalSearch(f, N, L, S, s)
        if f(s) < f(s_star):
            s_star = s
        s = GenerateNewSolution(s)
    return s_star