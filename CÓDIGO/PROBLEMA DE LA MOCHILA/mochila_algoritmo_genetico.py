from elitism import eaSimpleWithElitism
from read_knapsack_files import read_knapsack
from greedy_knapsack_individual import knapsack_greedy

import pandas as pd
import random, numpy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import time

def main(greedy, elitism, n_pop, n_gen, mat_prob, mut_prob, tournsize, nreps, filename, out1, out_filename):
    
    
    """
    Algoritmo genético para el problema de la mochila
    
    input:
        greedy:: Bool, indica si se añade un individuo representante de la solución obtenida por el algoritmo voraz
        elitism:: Bool, inidica si se aplica elitismo
        n_pop:: Int, tamaño de la población
        n_gen:: Int, número de generaciones
        mat_prob:: Float, probabilidad de cruce, entre 0 y 1
        mut_prob:: Float, probabilidad de mutación, entre 0 y 1
        tournsize:: Int, tamaño de torneo
        nreps:: Int, número de ejecuciones
        filename:: Str, nombre del fichero en el que se encuentra la instancia
        out1:: Str, path a la carpeta para guardar los resultados
        out_filename:: Str, nombre del fichero de salida en el que se guardan los resultados
    """
    
    start = time.time()
    N, MAX_WEIGHT, items = read_knapsack(filename)
 


    #maximiza el valor
    creator.create("Fitness", base.Fitness, weights=(1.0,))


    #representamos los individuos en un cjto
    creator.create("Individual", set, fitness=creator.Fitness)

    
    toolbox = base.Toolbox()
    toolbox.register("knapsack_greedy", knapsack_greedy, filename)
    toolbox.register("attr_item", random.randrange, N)  ## N = NBR_ITEMS
    toolbox.register("individual1", tools.initRepeat, creator.Individual, 
        toolbox.attr_item, N) ## N = IND_INIT_SIZE
    toolbox.register("individual2", tools.initIterate, creator.Individual, toolbox.knapsack_greedy)
    toolbox.register("population", tools.initRepeat, list)


    def evalKnapsack(individual):
        weight = 0.0
        value = 0.0
        for item in individual:
            value += items[item][0]
            weight += items[item][1]
        if weight > MAX_WEIGHT:
            return 0, 10000             # Ensure overweighted bags are dominated
        return value, weight

    #crossover in sets: producing two children from two parents, could be that the first
    #child is the intersection of the two sets and the second child their absolute difference
    def cxSet(ind1, ind2):
        """Apply a crossover operation on input sets. The first child is the
        intersection of the two sets, the second child is the difference of the
        two sets.
        """
        temp = set(ind1)                # Used in order to keep type
        ind1 &= ind2                    # Intersection (inplace)
        ind2 ^= temp                    # Symmetric Difference (inplace)
        return ind1, ind2

    #mutation operator could randomly add or remove an element from the set input individual
    def mutSet(individual):
        """Mutation that pops or add an element."""
        if random.random() < 0.5:
            if len(individual) > 0:     # We cannot pop from an empty set
                individual.remove(random.choice(sorted(tuple(individual))))
        else:
            individual.add(random.randrange(N)) ## N = IND_INIT_SIZE
        return individual,


    dict_result = dict()
    dict_time = dict()
    dict_all_gen = dict()
    for i in range(nreps):

        #register these operators in the toolbox
        toolbox.register("evaluate", evalKnapsack)
        toolbox.register("mate", cxSet)
        toolbox.register("mutate", mutSet)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
        
        if greedy:
            pop1 = toolbox.population(toolbox.individual1, n=n_pop)
            pop2 = toolbox.population(toolbox.individual2, n=1)
            pop = pop1 + pop2
        else:
            pop = toolbox.population(toolbox.individual1, n=n_pop) 
        
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, logbook = eaSimpleWithElitism(pop, toolbox, mat_prob, mut_prob, n_gen, stats,
                              halloffame=hof)
        #pop, logbook = algorithms.eaSimple(pop, toolbox, mat_prob, mut_prob, n_gen, stats,
        #                         halloffame=hof)
    
        result_list = logbook
        end = time.time()
        dict_all_gen[i] = list(result_list)
        dict_result[i] = result_list[-1]
        dict_time[i] = {'time': end-start}

    dfa = pd.DataFrame.from_dict(dict_all_gen, orient = 'index')
    dfa.to_csv('Data_KNAPSACK/' + out1 + out_filename + 'all_gen.csv', sep=';', header=True, index=True)
    df1 = pd.DataFrame.from_dict(dict_result, orient = 'index')
    df2 = pd.DataFrame.from_dict(dict_time, orient = 'index')
    df = pd.concat([df1,df2], axis=1, sort=False)
    df.to_csv('Data_KNAPSACK/' + out1 + out_filename + 'complete.csv', sep=';', header=True, index=True)
    df = df.describe()
    df.to_csv('Data_KNAPSACK/' + out1 + out_filename + '.csv', sep=';', header=True, index=True)