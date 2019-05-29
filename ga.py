from abc import ABC, abstractmethod
from random import random, uniform

def flip(p):
    if random() < p:
        return True
    return False

class Parameters:
    def __init__(self, popsize, numgen, pcrossover, pmutation, elitism=True, minmax='max'):
        self.popsize = popsize
        self.numgen = numgen
        self.pcrossover = pcrossover
        self.pmutation = pmutation
        self.elitism = elitism
        self.minmax = minmax

class GABase(ABC):
    def __init__(self, params):
        self.params = params
        self.population = []
        self.objs = []
        self.fitnesses = []

    def best(self, otherobjs=None):
        if self.params.minmax == 'max':
            if otherobjs == None:
                bestobj = max(self.objs)
            else:
                bestobj = max(otherobjs)
        else:
            if otherobjs == None:
                bestobj = min(self.objs)
            else:
                bestobj = min(otherobjs)
        return bestobj, self.objs.index(bestobj) if otherobjs==None else otherobjs.index(bestobj)

    def worst(self, otherobjs=None):
        if self.params.minmax == 'max':
            if otherobjs == None:
                worstobj = min(self.objs)
            else:
                worstobj = min(otherobjs)
        else:
            if otherobjs == None:
                worstobj = max(self.objs)
            else:
                worstobj = max(otherobjs)
        return worstobj, self.objs.index(worstobj) if otherobjs==None else otherobjs.index(worstobj)

    # user provides a decode method
    def decode(self, s):
        return s
        
    def evaluation(self):
        self.objs = [self.obj(self.decode(s)) for s in self.population]
        self.fitnesses = self.obj2fitness()

    #
    # abstract methods
    #
    @abstractmethod
    def obj(self, s):
        return
    @abstractmethod
    def initialization(self):
        return
    @abstractmethod
    def obj2fitness(self):
        return
    @abstractmethod
    def crossover(self, s1, s2):
        return
    @abstractmethod
    def mutation(self, s):
        return

    def select(self):
        total = sum(self.fitnesses)
        r = uniform(0, total)
        acc = 0
        for i in range(len(self.fitnesses)):
            acc += self.fitnesses[i]
            if acc >= r:
                return i

    def generation(self):
        oldbest, ibest = self.best()
        newpop = []
        while len(newpop) < len(self.population):
            p1 = self.population[self.select()]
            p2 = self.population[self.select()]
            offspring = self.crossover(p1, p2)
            for s in offspring:
                c = self.mutation(s)
                if len(newpop) < len(self.population):
                    newpop.append(c)
                else:
                    break
        newobjs = [self.obj(self.decode(s)) for s in newpop]
        if self.params.elitism:
            newbest, _ = self.best(newobjs)
            _, inewworst = self.worst(newobjs)
            if self.better(oldbest, newbest): # if old is better than new
                newpop[inewworst] = self.population[ibest]
                newobjs[inewworst] = oldbest
        self.population = newpop
        self.objs = newobjs
        self.fitnesses = self.obj2fitness()

    # if a is better than b?
    def better(self, a, b):
        if self.params.minmax == 'min':
            return a < b
        else:
            return a > b

    def run(self):
        self.initialization()
        for i in range(self.params.numgen):
            self.generation()
        return self.best()[0], sum(self.objs)/self.params.popsize
