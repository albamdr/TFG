from elitism import eaSimpleWithElitism
from two_opt_individuo import two_OPT_individual
from algoritmo_voraz_individuo import greedy_tsp_individual as greedy_tsp
from read_tsp_file_euclidean import read_tsp
from read_tsp_file_euclidean import distance_matrix

import numpy as np
import array
import random

import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

def tsp_ga(greedy, opt, elitism, n_pop, n_gen, mat_prob, mut_prob, tournsize , nreps, filename, out1, out_filename):
    
    """
    Algoritmo genético para TSP
    
    input:
        greedy:: Bool, indica si se añade un individuo representante de la solución obtenida por el algoritmo voraz
        opt::  Bool, indica si se añade un individuo representante de la solución obtenida por el 2-OPT
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

    nodelist, N = read_tsp(filename)
    distanceMatrix = distance_matrix(nodelist, N) 

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) # minimizar distancias
    creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register("indices", random.sample, range(N), N)
    toolbox.register("greedy_tsp", greedy_tsp, distanceMatrix, N)
    toolbox.register("two_OPT_individual", two_OPT_individual, distanceMatrix, N)

    # Structure initializers
    toolbox.register("individual1", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("individual2", tools.initIterate, creator.Individual, toolbox.greedy_tsp)
    toolbox.register("individual3", tools.initIterate, creator.Individual, toolbox.two_OPT_individual)
    toolbox.register("population", tools.initRepeat, list)

    def evalTSP(individual):
        distance = distanceMatrix[individual[-1]][individual[0]]
        for gene1, gene2 in zip(individual[0:-1], individual[1:]):
            distance += distanceMatrix[gene1][gene2]
        return distance,
    
    dict_all_generation = dict()
    dict_result = dict()
    dict_time = dict()
    for i in range(nreps):
        
        start = time.time()
        
        toolbox.register("mate", tools.cxPartialyMatched)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
        toolbox.register("evaluate", evalTSP)
        
        if greedy:
            pop1 = toolbox.population(toolbox.individual1, n=n_pop)
            pop2 = toolbox.population(toolbox.individual2, n=1)
            pop = pop1 + pop2
        elif opt:
            pop1 = toolbox.population(toolbox.individual1, n=n_pop)
            pop2 = toolbox.population(toolbox.individual3, n=1)
            pop = pop1 + pop2
        else:
            pop = toolbox.population(toolbox.individual1, n=n_pop)

    
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
    
        if elitism:
            
            pop2, logbook = eaSimpleWithElitism(pop, toolbox, mat_prob, mut_prob, n_gen, stats=stats, 
                       halloffame=hof)
        else:
            
            pop2, logbook = algorithms.eaSimple(pop, toolbox, mat_prob, mut_prob, n_gen, stats=stats, 
                            halloffame=hof)
        
    
        result_list = logbook
        end = time.time()
        dict_all_generation[i] = list(result_list)
        dict_result[i] = result_list[-1]
        dict_time[i] = {'time': end-start}
        
    df = pd.DataFrame.from_dict(dict_all_generation, orient = 'index')
    df.to_csv(out1+'all_generation'+out_filename, sep=';',header=True,index=True)
    df1 = pd.DataFrame.from_dict(dict_result, orient = 'index')
    df2 = pd.DataFrame.from_dict(dict_time, orient = 'index')
    frames = [df1, df2]
    result = pd.concat(frames, axis=1, sort=False)
    result.to_csv(out1+'complete'+out_filename, sep=';',header=True,index=True)
    result = result.describe()
    result.to_csv(out1+out_filename, sep=';',header=True,index=True)