import pandas as pd
import random, numpy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import time

from elitism import eaSimpleWithElitism
from read_MIS_files import read_MIS
from algoritmo_voraz_individuo import greedy_mis

def mis(greedy, elitism, n_gen, mat_prob, mut_prob, tournsize, n_pop, nreps, filename, out1, out_filename):

    
    """
    Algoritmo genético para max independent set
    
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
    E, N, G = read_MIS(filename)
 


    #minimiza el peso y maximiza el valor
    creator.create("Fitness", base.Fitness, weights=(1.0,)) #quiero maximizar el número de vértices:
                                                           

    #representamos los individuos en una lista
    
    creator.create("Individual", list, fitness=creator.Fitness)

    
    toolbox = base.Toolbox()
    toolbox.register("greedy_mis", greedy_mis, filename)
    toolbox.register("attr_item", random.randint, 0, 1)  ## N = número de vértices
    toolbox.register("individual1", tools.initRepeat, creator.Individual, 
        toolbox.attr_item, N)
    toolbox.register("individual2", tools.initIterate, creator.Individual, toolbox.greedy_mis)
    toolbox.register("population", tools.initRepeat, list)


    def evalMIS(individual): #evalMIS

        for i in range(len(individual)): 
            if individual[i]==1:
                for j in range(i+1,len(individual)): #si los vértices i,j son adyacentes eliminamos j del conjunto
                    if individual[j]==1 and (i+1,j+1) in G[i]:
                        individual[j]=0
        v = sum(individual)
        return v,  

    def cxSet(ind1, ind2):
        
        set1=set()
        set2=set()
        
        for i in range(len(ind1)): #creo los conjuntos con los vértices que hay en cada individuo i.e (ind1={1,5,6,87,543})
            if ind1[i]==1:
                ind1[i]=0
                set1.add(i+1)
        for i in range(len(ind2)):
            if ind2[i]==1:
                ind2[i]=0
                set2.add(i+1)
                
        ind_set = set1.union(set2)
        ind_grades = [] #lista de tuplas (vértice,grado)
        for i in ind_set:
            grade = 0
            for edge in G:
                if i in edge:
                    grade+=1
            ind_grades.append((i,grade))
        ind_grades.sort(reverse=False, key=lambda x: x[1]) #ordenamos la lista por grado(ascendiente)
        
        for i in ind_grades: #añadimos vértices por grado de menor a mayor hasta que no podemos añadir más
            v = i[0]
            ind1[v-1]=1
            if evalMIS(ind1)==0:
                ind1[v-1]=0
                ind2 = ind1
        return ind1, ind2 #ahora ind1 = ind2

    #mutation operator could randomly add one vertex to the list changing a zero to a one
    def mut(individual):
        i =  random.randint(0,len(individual)-1)
        if individual[i]==1:
            mut(individual)
        else:
            individual[i] = 1
        return individual,


    dict_result = dict()
    dict_time = dict()
    dict_all_gen = dict()
    for i in range(nreps):
        
        #register these operators in the toolbox
        toolbox.register("evaluate", evalMIS)
        toolbox.register("mate", cxSet)
        toolbox.register("mutate", mut)
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
        #stats.register("min", numpy.min)
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
    df.to_csv(out1+ out_filename + '.csv', sep=';', header=True, index=True)