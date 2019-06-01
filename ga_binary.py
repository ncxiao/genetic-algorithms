from random import random, randint, sample, uniform

def flip(p):
    if random() < p:
        return True
    return False
    
def crossover(s1, s2, prob):
    if not flip(prob):
        return [s1, s2], 0
    n = len(s1)
    x = randint(0, n-1)
    s1x = s1[:x] + s2[x:]
    s2x = s2[:x] + s1[x:]
    return [s1x, s2x], x

def mutation(s, prob):
    mutated = ''
    mutate = lambda i: '1' if i=='0' else '0'
    for c in s:
        if flip(prob):
            mutated += mutate(c)
        else:
            mutated += c
    return mutated
    
def decode(s):
    def _decode(s):
        num = 0
        n = len(s)
        for i in range(n):
            c = s[n-i-1]
            num += int(c) * 2 ** i
        return num
    return _decode(s[:3]), _decode(s[3:6]), _decode(s[6:])

def obj(x):
    return x[0] ** 2 - x[1] - x[2] + 1

def obj2fitness(objs):
    low = min(objs)
    minimal = (max(objs) - low) * 0.1
    fitnesses = [val - low + minimal for val in objs]
    return fitnesses

def evaluation(population):
    objs = [obj(decode(s)) for s in population]
    return objs

def select(fitnesses):
    total = sum(fitnesses)
    r = uniform(0, total)
    acc = 0
    for i in range(len(fitnesses)):
        acc += fitnesses[i]
        if acc >= r:
            return i

def generation(population, objs, fitnesses, pcrossover, pmutation, elitism=True):
    oldbest = max(objs)
    ibest = objs.index(oldbest)
    newpop = []
    while len(newpop) < len(population):
        p1 = population[select(fitnesses)]
        p2 = population[select(fitnesses)]
        offspring = crossover(p1, p2, pcrossover)[0]
        for s in offspring:
            c = mutation(s, pmutation)
            if len(newpop) < len(population):
                newpop.append(c)
            else:
                break
    newobjs = [obj(decode(s)) for s in newpop]
    if elitism:
        newbest = max(newobjs)
        inewworst = newobjs.index(min(newobjs))
        if oldbest > newbest:
            newpop[inewworst] = population[ibest]
            newobjs[inewworst] = oldbest
    population = newpop
    objs = newobjs
    newfitnesses = obj2fitness(newobjs)
    return newpop, newobjs, newfitnesses

def initialization(popsize):
    population = []
    for i in range(popsize):
        sol = ''.join(['1' if flip(0.5) else '0' 
                       for i in range(9)])
        population.append(sol)
    objs = [obj(decode(s)) for s in population]
    fitnesses = obj2fitness(objs)
    return population, objs, fitnesses
        
def GA(param):
    population, objs, fitnesses = initialization(param.popsize)
    for i in range(param.numgen):
        population, objs, fitnesses = generation(
            population, objs, fitnesses, param.pcrossover, param.pmutation, param.elitism)
    return max(objs), sum(objs)/param.popsize, population


class Parameters:
    def __init__(self, popsize, numgen, pcrossover, pmutation, elitism):
        self.popsize = popsize
        self.numgen = numgen
        self.pcrossover = pcrossover
        self.pmutation = pmutation
        self.elitism = elitism
    
# returns the median objective function value 
def run_many_GAs(n, param):
    all_best = []
    for i in range(n):
        res = GA(param)
        all_best.append(res[0])
    all_best.sort()
    return(all_best[n//2], all_best[0]) # return median and worst

def test():
    psizes = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    nruns = [5, 10, 15, 20, 25, 30]
    pcross = [0, 0.1, 0.3, 0.5, 0.7, 0.9]
    pmutate = [0, 0.1, 0.3, 0.5, 0.7, 0.9]
    elitisms = [True, False]

    for n in psizes:
        for nr in nruns:
            for pc in pcross:
                for pm in pmutate:
                    for e in elitisms:
                        paramx = Parameters(n, nr, pc, pm, e)
                        res = run_many_GAs(10, paramx)
                        print(n, nr, pc, pm, e, res[0], res[1])

# test()

param = Parameters(
    popsize = 10,
    numgen = 10,
    pcrossover = 0.8,
    pmutation = 0.1,
    elitism = True)

result = GA(param)
print(result[:2])

all_result = []
for _ in range(10):
    population, objs, fitnesses = initialization(10)
    for i in range(10):
        population, objs, fitnesses = generation(population, objs, fitnesses, 0.9, 0.1, False)
    all_result.append(max(objs))

print('no elitism  :', all_result)
print('with elitism:', [GA(param)[0] for _ in range(10)])
