import numpy as np
from models import NanogramSolution
from data import CLUES
from nanogram import NanogramGA
from tqdm import tqdm
import editdistance

def nanogram_fitness(one_line):
    def helper(chromosome, clues):
        ns = NanogramSolution(clues, chromosome)
        def one_orientation(expected, actual):
            return sum(one_line(x, y) for x, y in zip(expected, actual))
        return one_orientation(clues.rows, ns.solution_clues.rows) + one_orientation(clues.columns, ns.solution_clues.columns)
    return helper

@nanogram_fitness
def fitness1(expected, actual):
    return 1 if expected == actual else 0

@nanogram_fitness
def fitness2(expected, actual):
    return -editdistance.eval(expected, actual)

def main():
    generations = 50
    nga = NanogramGA(
        CLUES,
        fitness1,
        population_size=200,
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
