import numpy as np
from models import NanogramSolution
from data import CLUES
from nanogram import NanogramGA
from tqdm import tqdm
import editdistance

def fitness1(chromosome, clues):
    nanogram_solution = NanogramSolution(clues, chromosome)
    return np.sum(nanogram_solution.row_correctness) + np.sum(nanogram_solution.column_correctness)

def fitness2(chromosome, clues):
    ns = NanogramSolution(clues, chromosome)
    a = [editdistance.eval(x, y) for x, y in zip(ns.solution_clues.rows, clues.rows)]
    b = [editdistance.eval(x, y) for x, y in zip(ns.solution_clues.columns, clues.columns)]
    return -(sum(a)+sum(b))

def main():
    generations = 300
    nga = NanogramGA(
        CLUES,
        fitness2,
        population_size=1000,
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
