import numpy as np
from models import NonogramSolution
from data import CLUES
from nonogram import NonogramGA
from tqdm import tqdm
from variants import *

def main():
    generations = 10
    nga = NonogramGA(
        CLUES,
        BasicDiffsVariant,
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
