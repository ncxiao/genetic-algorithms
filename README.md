# Genetic Algorithms

This repository contains code and documents that demonstrate the essence of genetic algorithms (GAs) and how they can be used for optimization problems. 

We focus on single objective optimization here. For multiobjective optimization using GAs, please see another repo called nsga-ii at https://github.com/ncxiao/nsga-ii, or [this notebook](NSGA-II.ipynb).

## Example Notebooks

- `genetic algorithms.ipynb` introduction to genetic algorithms and how to implement them using Python.
- `GA Class.ipynb` a Python class called `GA` and how to use it for solving specific numerical and spatial optimization problems.

## Files

The following is a list of the source code:
	
- `README.md` this file
- `ga.py` a Python module for `GA` and `Parameters` classes
- `ga_base_binary.py` deriving theb`GA` class for a numerical problem using binary strings
- `ga_base_pmed.py` deriving theb`GA` class for a p-median problem
- `ga_binary.py` GA using binary strings (without using the `GA` class)
- `ga_pmed.py` GA for p-median problems (without using the `GA` class)

## Usage

From terminal:

```
$ python3 ga_base_binary.py 
(50, 44.9)
[50, 49, 50, 49, 49, 50, 50, 50, 48, 50]

$ python3 ga_base_pmed.py 
(40, 47.75)
mutation        obj
              0 38
            0.1 72
            0.2 79
            0.3 86
            0.4 91
            0.5 84
            0.6 90
            0.7 85
            0.8 87
            0.9 78
              1 80
```

From Python shell:

```
>>> from ga_base_pmed import *
>>> owndata = {
...     'n': 8,
...     'distmatrix': [
...         [0, 3, 13, 5, 12, 16, 17, 20],
...         [3, 0, 10, 8, 9, 13, 14, 23],
...         [13, 10, 0, 8, 9, 3, 14, 15],
...         [5, 8, 8, 0, 17, 11, 22, 15],
...         [12, 9, 9, 17, 0, 6, 5, 16],
...         [16, 13, 3, 11, 6, 0, 11, 12],
...         [17, 14, 14, 22, 5, 11, 0, 11],
...         [20, 23, 15, 15, 16, 12, 11, 0]],
...     'p': 2
... }
>>> 
>>> params = Parameters(
...     popsize = 4,
...     numgen = 10,
...     pcrossover = 0.9,
...     pmutation = 0.1,
...     elitism = False,
...     minmax = 'min')
>>> myga = GAPMed(params, owndata)
>>> res = myga.run()
>>> print(res)
(40, 42.75)

>>> from ga_base_binary import *
>>> params = Parameters(
...     popsize = 10,
...     numgen = 10,
...     pcrossover = 0.9,
...     pmutation = 0.1,
...     elitism = True)
>>> 
>>> myga = GABin(params)
>>> res = myga.run()
>>> print(res)
(50, 38.4)
>>> print([myga.run()[0] for _ in range(10)])
[49, 48, 50, 49, 49, 50, 50, 49, 50, 50]
```

## Contact

Ningchuan Xiao (ncxiao@gmail.com)
