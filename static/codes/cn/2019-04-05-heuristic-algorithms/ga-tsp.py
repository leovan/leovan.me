#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import random
import numpy as np
import pandas as pd

from geopy.distance import geodesic
from deap import algorithms, base, creator, tools

# 读取数据
city_coordinate = pd.read_csv('city-coordinate.tsv', header=0, sep='\t')

# 构建距离矩阵
def distance_tsp(latitude1, longitude1, latitude2, longitude2):
    return geodesic((latitude1, longitude1), (latitude2, longitude2)).meters

city_distance_matrix = np.zeros([len(city_coordinate), len(city_coordinate)], dtype=np.float64)

for i in range(len(city_coordinate)):
    for j in range(len(city_coordinate)):
        city_distance_matrix[i, j] = distance_tsp(city_coordinate.iloc[i, 2], city_coordinate.iloc[i, 1],
                                                  city_coordinate.iloc[j, 2], city_coordinate.iloc[j, 1])

# 染色体位数
IND_SIZE = len(city_coordinate)

# 种群数量
POPULATION = 100

# 交叉率
CXPB = 0.7

# 个体变异率
MUTPB = 0.2

# 基因变异率
INDPB = 0.05

# 迭代次数
NGEN = 1000

# 设置 TSP 问题的 Fitness
creator.create('FitnessMin', base.Fitness, weights=(-1.0, ))

# 设置个体
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate_tsp(individual):
    distance = city_distance_matrix[individual[-1]][individual[0]]
    for gene1, gene2 in zip(individual[0:-1], individual[1:]):
        distance += city_distance_matrix[gene1][gene2]
    return distance,

toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=INDPB)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate_tsp)

def main():
    with open('city-path.tsv', 'w') as f:
        f_writer = csv.DictWriter(f, ['path', 'fitness'], delimiter='\t')
        f_writer.writeheader()

        random.seed(112358)
        pop = toolbox.population(n=POPULATION)

        print('Start of evolution')

        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for iter in range(NGEN):
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)

                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)

                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            print("Iter: {iter}, Evaluated {counts} individuals".format(iter=iter, counts=len(invalid_ind)))

            pop[:] = offspring

            best_ind = tools.selBest(pop, 1)[0]

            path = ','.join(map(str, list(best_ind)))
            fitness, = best_ind.fitness.values

            f_writer.writerow({'path': path, 'fitness': fitness})


if __name__ == '__main__':
    main()
