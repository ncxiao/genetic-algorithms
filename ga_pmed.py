# GA for p-median

from random import random, randint, sample, uniform

n = 8

distmatrix = [
    [0, 3, 13, 5, 12, 16, 17, 20],
    [3, 0, 10, 8, 9, 13, 14, 23],
    [13, 10, 0, 8, 9, 3, 14, 15],
    [5, 8, 8, 0, 17, 11, 22, 15],
    [12, 9, 9, 17, 0, 6, 5, 16],
    [16, 13, 3, 11, 6, 0, 11, 12],
    [17, 14, 14, 22, 5, 11, 0, 11],
    [20, 23, 15, 15, 16, 12, 11, 0]]

p = 2

def flip(p):
    if random() < p:
        return True
    return False

def obj(s):
    n = len(distmatrix)
    d_total = 0
    for i in range(n):
        d_min = float('inf')
        for j in s:
            if distmatrix[i][j] < d_min:
                d_min = distmatrix[i][j]
        d_total += d_min
    return d_total

def obj2fitness(objs):
    fitnesses = [1/val for val in objs]
    return fitnesses
    
def initialization(popsize, n, p):
    population = []
    for i in range(popsize):
        sol = sample(range(n), p)
        population.append(sol)
    objs = [obj(s) for s in population]
    fitnesses = obj2fitness(objs)
    return population, objs, fitnesses
    
def crossover(s1, s2, prob):
    if not flip(prob):
        return s1
    p = len(s1)
    child = list(set(s1 + s2))
    while len(child) > p:
        d = float('inf')
        to_remove = -1
        for i in child:
            c1 = [j for j in child if j != i]
            d1 = obj(c1)
            if d1 < d:
                d = d1
                to_remove = i
        child = [j for j in child if j != to_remove]
    return child
    
def mutation(s, prob):
    for i in range(len(s)):
        if not flip(prob):
            continue
        while True:
            j = randint(0, n-1)
            # if j != s[i]:
            if not j in s:
                s[i] = j
                break
    return s
    
def select(fitnesses):
    total = sum(fitnesses)
    r = uniform(0, total)
    acc = 0
    for i in range(len(fitnesses)):
        acc += fitnesses[i]
        if acc >= r:
            return i
            
            
def generation(pop, objs, fitnesses, pcrossover, pmutation, elitism=True):
    oldbest = min(objs)
    ibest = objs.index(oldbest)
    newpop = []
    for i in range(len(pop)):
        p1 = pop[select(fitnesses)]
        p2 = pop[select(fitnesses)]
        child1 = crossover(p1, p2, pcrossover)
        child1 = mutation(child1, pmutation)
        newpop.append(child1)
    newobjs = [obj(c) for c in newpop]
    if elitism:
        newbest = min(newobjs)
        iworst = newobjs.index(max(newobjs))
        if oldbest < newbest: # old best is better
            newpop[iworst] = pop[ibest]
            newobjs[iworst] = oldbest
    newfitnesses = obj2fitness(newobjs)
    return newpop, newobjs, newfitnesses




class Parameters:
    def __init__(self, popsize, numgen, pcrossover, pmutation, elitism):
        self.popsize = popsize
        self.numgen = numgen
        self.pcrossover = pcrossover
        self.pmutation = pmutation
        self.elitism = elitism


def GA(param):
    population, objs, fitnesses = initialization(param.popsize, n, p)
    for i in range(param.numgen):
        population, objs, fitnesses = generation(
            population, objs, fitnesses, param.pcrossover, param.pmutation, param.elitism)
    return min(objs), sum(objs)/param.popsize, population


# returns the median objective function value 
def run_many_GAs(n, param):
    all_best = []
    for i in range(n):
        # res = GA(popsize, numgeneration, pcrossover, pmutation, elitism)
        res = GA(param)
        all_best.append(res[0])
    return sum([1 if res==40 else 0 for res in all_best])

def test():
    pcross = [0, 0.1, 0.3, 0.5, 0.7, 0.9]
    pmutate = [0, 0.1, 0.3, 0.5, 0.7, 0.9]
    for pc in pcross:
        for pm in pmutate:
            paramx = Parameters(4, 10, pc, pm, True)
            res = run_many_GAs(1000, paramx)
            print(pc, pm, res)

# test()

param = Parameters(
    popsize = 4,
    numgen = 10,
    pcrossover = 0.9,
    pmutation = 0.3,
    elitism = True)

print([GA(param)[0] for _ in range(10)])
