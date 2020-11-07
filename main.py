import numpy as np
from models import NonogramSolution
from data import CLUES
from nonogram import NonogramGA
from tqdm import tqdm
import editdistance

def nonogram_fitness(one_line):
    def helper(chromosome, clues):
        ns = NonogramSolution(clues, chromosome)
        def one_orientation(expected, actual):
            return sum(one_line(x, y) for x, y in zip(expected, actual))
        return one_orientation(clues.rows, ns.solution_clues.rows) + one_orientation(clues.columns, ns.solution_clues.columns)
    return helper

@nonogram_fitness
def fitness1(expected, actual):
    return 1 if expected == actual else 0

@nonogram_fitness
def fitness2(expected, actual):
    return -editdistance.eval(expected, actual)

@nonogram_fitness
def fitness3(expected, actual):
    min_len = min(len(expected), len(actual))
    value_diff = np.sum(np.abs(np.array(expected[:min_len]) - np.array(actual[:min_len])))
    len_diff = abs(len(expected)-len(actual))
    return -(value_diff + len_diff)

def main():
    generations = 150
    nga = NonogramGA(
        CLUES,
        fitness3,
        population_size=500,
        generations=generations,
        mutation_probability=0.05,
        elitism=True
    )
    pbar = tqdm(nga.run(), total=generations)
    for iteration in pbar:
        pbar.set_description(f'Current best: {iteration.best_fitness}, average: {iteration.average_fitness}')
    nga.show_best_solution()
    nga.show_statistics()

if __name__ == '__main__':
    main()
