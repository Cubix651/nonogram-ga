import numpy as np
from models import NanogramSolution
from data import CLUES
from nanogram import NanogramGA
from tqdm import tqdm

def fitness(chromosome, clues):
    nanogram_solution = NanogramSolution(clues, chromosome)
    return np.sum(nanogram_solution.row_correctness) + np.sum(nanogram_solution.column_correctness)

def main():
    generations = 10
    nga = NanogramGA(
        CLUES,
        fitness,
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
