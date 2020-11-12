from nonogram import NonogramGA
from tqdm import tqdm
from variants import *
from visualize import NonogramSolutionVisualizer
from reader import NonReader

def main():
    path = 'projekt/butterfly.non'
    nr = NonReader(path)
    ns = nr.read()
    visualizer = NonogramSolutionVisualizer()
    visualizer.set_nonogram_solution(ns)
    visualizer.show()
    
    parameters = {
        'generations': 20,
        'population_size': 200,
        'mutation_probability': 1,
        'elitism': True,
        'variant': ExtendedDiffVariant
    }
    print(parameters)
    nga = NonogramGA(ns.clues, **parameters)
    pbar = tqdm(nga.run(), total=parameters['generations'])
    for iteration in pbar:
        pbar.set_description(f'Current best: {iteration.best_fitness}, average: {iteration.average_fitness}')
    nga.show_best_solution()
    nga.show_statistics()

if __name__ == '__main__':
    main()
