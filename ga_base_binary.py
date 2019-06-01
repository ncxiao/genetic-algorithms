from ga import *
from random import randint

class GABin(GABase):
    def __init__(self, params):
        super().__init__(params)

    def decode(self, s):
        def _decode(s):
            num = 0
            n = len(s)
            for i in range(n):
                c = s[n-i-1]
                num += int(c) * 2 ** i
            return num
        return _decode(s[:3]), _decode(s[3:6]), _decode(s[6:])

    def obj(self, x):
        return x[0] ** 2 - x[1] - x[2] + 1

    def obj2fitness(self):
        low = self.worst()[0]
        minimal = (self.best()[0] - low) * 0.1
        fitnesses = [val - low + minimal for val in self.objs]
        return fitnesses

    def initialization(self):
        self.population = []
        for i in range(self.params.popsize):
            sol = ''.join(['1' if flip(0.5) else '0' for i in range(9)])
            self.population.append(sol)
        self.evaluation()

    def crossover(self, s1, s2):
        if not flip(self.params.pcrossover):
            return [s1, s2]
        n = len(s1)
        x = randint(0, n-1)
        s1x = s1[:x] + s2[x:]
        s2x = s2[:x] + s1[x:]
        return [s1x, s2x]

    def mutation(self, s):
        mutated = ''
        mutate = lambda i: '1' if i=='0' else '0'
        for c in s:
            if flip(self.params.pmutation):
                mutated += mutate(c)
            else:
                mutated += c
        return mutated

if __name__ == '__main__':
    params = Parameters(
        popsize = 10,
        numgen = 10,
        pcrossover = 0.9,
        pmutation = 0.1,
        elitism = True)
        
    myga = GABin(params)
    res = myga.run()
    print(res)

    print([myga.run()[0] for _ in range(10)])
