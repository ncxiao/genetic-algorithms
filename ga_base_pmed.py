from ga import *
from random import randint, sample

class GAPMed(GABase):
    def __init__(self, params, owndata):
        super().__init__(params)
        self.n = owndata['n']
        self.distmatrix = owndata['distmatrix']
        self.p = owndata['p']

    def obj(self, s):
        n = len(self.distmatrix)
        d_total = 0
        for i in range(self.n):
            d_min = float('inf')
            for j in s:
                if self.distmatrix[i][j] < d_min:
                    d_min = self.distmatrix[i][j]
            d_total += d_min
        return d_total

    def obj2fitness(self):
        return [1/val for val in self.objs]

    def initialization(self):
        self.population = []
        for i in range(self.params.popsize):
            sol = sample(range(self.n), self.p)
            self.population.append(sol)
        self.evaluation()

    def crossover(self, s1, s2):
        if not flip(self.params.pcrossover):
            return [s1]
        child = list(set(s1 + s2))
        while len(child) > self.p:
            d = float('inf')
            to_remove = -1
            for i in child:
                c1 = [j for j in child if j != i]
                d1 = self.obj(c1)
                if d1 < d:
                    d = d1
                    to_remove = i
            child = [j for j in child if j != to_remove]
        return [child]

    def mutation(self, s):
        for i in range(len(s)):
            if not flip(self.params.pmutation):
                continue
            while True:
                j = randint(0, self.n-1)
                if not j in s:
                    s[i] = j
                    break
        return s

if __name__ == '__main__':
    owndata = {
        'n': 8,
        'distmatrix': [
            [0, 3, 13, 5, 12, 16, 17, 20],
            [3, 0, 10, 8, 9, 13, 14, 23],
            [13, 10, 0, 8, 9, 3, 14, 15],
            [5, 8, 8, 0, 17, 11, 22, 15],
            [12, 9, 9, 17, 0, 6, 5, 16],
            [16, 13, 3, 11, 6, 0, 11, 12],
            [17, 14, 14, 22, 5, 11, 0, 11],
            [20, 23, 15, 15, 16, 12, 11, 0]],
        'p': 2
    }

    params = Parameters(
        popsize = 4,
        numgen = 10,
        pcrossover = 0.9,
        pmutation = 0.1,
        elitism = False,
        minmax = 'min')

    myga = GAPMed(params, owndata)
    res = myga.run()
    print(res)

    # test mutation rates
    pmutate = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    paramx = [Parameters(4, 10, 0.9, pm, True, 'min') for pm in pmutate]

    def multirun(prog, n, best):
        all_best = []
        for _ in range(n):
            res = prog.run()
            all_best.append(res[0])
        return sum([1 if res==best else 0 for res in all_best])

    res = [multirun(myga, 100, 40) for myga in [GAPMed(par, owndata) for par in paramx]]

    print('{:15} {}'.format('mutation', 'obj'))
    for i in range(len(res)):
        print('{:15} {}'.format(pmutate[i], res[i]))

    def test():
        pcross = [0, 0.1, 0.3, 0.5, 0.7, 0.9]
        pmutate = [0, 0.1, 0.3, 0.5, 0.7, 0.9]
        for pc in pcross:
            for pm in pmutate:
                paramx = Parameters(4, 10, pc, pm, True, 'min')
                myga = GAMed(paramx, owndata)
                
                all_best = []
                for _ in range(1000):
                    res = myga.run()
                    all_best.append(res[0])
                print(pc, pm, sum([1 if res==40 else 0 for res in all_best]))

    # test()
