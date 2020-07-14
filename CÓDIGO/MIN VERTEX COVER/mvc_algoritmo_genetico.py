import pandas as pd
import random, numpy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import time

from algoritmo_voraz_individuo import greedy_mvc
from algoritmo_voraz_mejorado_individuo import greedy_mvc_mejorado
from read_MVC_files import read_MVC
from elitism import eaSimpleWithElitism

def mvc(greedy, greedy_mejorado, elitism, n_gen, mat_prob, mut_prob, tournsize, n_pop, nreps, filename, out1, out_filename):
    
    """
    Algoritmo genético para min vertex cover
    
    input:
        greedy:: Bool, indica si se añade un individuo representante de la solución obtenida por el algoritmo voraz
        greedy_mejorado:: Bool, indica si se añade un individuo representante de la solución obtenida por el 
                                algoritmo voraz mejorado
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
    E, N, G = read_MIS(filename)
 


    #minimiza el peso y maximiza el valor
    creator.create("Fitness", base.Fitness, weights=(-1.0,)) #quiero minimimzar el número de vértices:
                                                            

    #representamos los individuos en una lista
    creator.create("Individual", list, fitness=creator.Fitness)

    
    toolbox = base.Toolbox()
    toolbox.register("attr_item", random.randint, 0, 1)  ## N = número de vértices
    toolbox.register("greedy_mvc", greedy_mvc, filename)
    toolbox.register("greedy_mvc_mejorado", greedy_mvc_mejorado, E, N, G)
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
        toolbox.attr_item, N)
    toolbox.register("individual2", tools.initIterate, creator.Individual, 
        toolbox.greedy_mvc)
    toolbox.register("individual3", tools.initIterate, creator.Individual, 
        toolbox.greedy_mvc_mejorado)
    toolbox.register("population", tools.initRepeat, list)


    def evalMVC(individual): #corrige los individuos que no sean MVC cubriendo los vértices que dejan descubiertos
        
        uncovered_vertex = {i  for i in range(N) if individual[i]==0}
        vertex = set()
        for i in uncovered_vertex:
            for edge in G[i]:
                u,v = edge
                vertex.add(v-1)
                    
        for i in vertex:
            individual[i]=1
        
        v = sum(individual)
                
        return v,

    #mutation operator could randomly remove one vertex to the list changing a one to a zero
    def mut(individual):
        i =  random.randint(0,len(individual)-1)
        individual[i] = 0
        return individual,


    dict_result = dict()
    dict_time = dict()
    dict_all_gen = dict()
    for i in range(nreps):
        
        #register these operators in the toolbox
        toolbox.register("evaluate", evalMVC)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", mut)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
    
        if greedy:
            pop1 = toolbox.population(toolbox.individual, n=n_pop)
            pop2 = toolbox.population(toolbox.individual2, n=1)
            pop = pop1+pop2
        elif greedy_mejorado:
            pop1 = toolbox.population(toolbox.individual, n=n_pop)
            pop2 = toolbox.population(toolbox.individual3, n=1)
            pop = pop1+pop2
        else:
            pop = toolbox.population(toolbox.individual, n=n_pop)
        
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
        
        if elitism:
            pop, logbook = eaSimpleWithElitism(pop, toolbox, mat_prob, mut_prob, n_gen, stats,
                              halloffame=hof)
            
        else:
            pop, logbook = algorithms.eaSimple(pop, toolbox, mat_prob, mut_prob, n_gen, stats,
                              halloffame=hof)
        
    
        result_list = logbook
        end = time.time()
        dict_all_gen[i] = list(result_list)
        dict_result[i] = result_list[-1]
        dict_time[i] = {'time': end-start}

    dfa = pd.DataFrame.from_dict(dict_all_gen, orient = 'index')
    dfa.to_csv(out1 + out_filename + 'all_gen.csv', sep=';', header=True, index=True)
    df1 = pd.DataFrame.from_dict(dict_result, orient = 'index')
    df2 = pd.DataFrame.from_dict(dict_time, orient = 'index')
    df = pd.concat([df1,df2], axis=1, sort=False)
    df.to_csv(out1 + out_filename + 'complete.csv', sep=';', header=True, index=True)
    df = df.describe()
    df.to_csv(out1 + out_filename + '.csv', sep=';', header=True, index=True)