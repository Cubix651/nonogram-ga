import sys
import os
from nonogram import NonogramGA
from tqdm import tqdm
from variants import *
from visualize import NonogramSolutionVisualizer
from reader import NonReader
import matplotlib.pyplot as plt

def single_run(path):
    nr = NonReader(path)
    ns = nr.read()
    visualizer = NonogramSolutionVisualizer()
    visualizer.set_nonogram_solution(ns)
    visualizer.show()
    
    parameters = {
        'generations': 50,
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
    print(nga.get_best_solution())
    nga.show_best_solution()
    nga.show_statistics()

GENERATIONS1 = 30
COMPETITORS1 = [
    ('Ex-Diff', {
        'generations': GENERATIONS1,
        'population_size': 200,
        'mutation_probability': 1,
        'elitism': True,
        'variant': ExtendedDiffVariant
    }),
    ('Ex-WholeLine', {
        'generations': GENERATIONS1,
        'population_size': 200,
        'mutation_probability': 1,
        'elitism': True,
        'variant': ExtendedWholeLineVariant
    }),
    ('B-Diff', {
        'generations': GENERATIONS1,
        'population_size': 200,
        'mutation_probability': 0.05,
        'elitism': True,
        'variant': BasicDiffsVariant
    }),
    ('B-EditDist', {
        'generations': GENERATIONS1,
        'population_size': 200,
        'mutation_probability': 0.05,
        'elitism': True,
        'variant': BasicEditDistanceVariant
    }),
    ('B-WholeLine', {
        'generations': GENERATIONS1,
        'population_size': 200,
        'mutation_probability': 0.05,
        'elitism': True,
        'variant': BasicWholeLineVariant
    })
]

GENERATIONS2 = 50
COMPETITORS2 = [
    ('Ex-Diff', {
        'generations': GENERATIONS2,
        'population_size': 200,
        'mutation_probability': 1,
        'elitism': True,
        'variant': ExtendedDiffVariant
    }),
    ('Ex-WholeLine', {
        'generations': GENERATIONS2,
        'population_size': 200,
        'mutation_probability': 1,
        'elitism': True,
        'variant': ExtendedWholeLineVariant
    }),
    ('B-Diff', {
        'generations': GENERATIONS2,
        'population_size': 200,
        'mutation_probability': 0.05,
        'elitism': True,
        'variant': BasicDiffsVariant
    }),
    ('B-EditDist', {
        'generations': GENERATIONS2,
        'population_size': 200,
        'mutation_probability': 0.05,
        'elitism': True,
        'variant': BasicEditDistanceVariant
    }),
    ('B-WholeLine', {
        'generations': GENERATIONS2,
        'population_size': 200,
        'mutation_probability': 0.05,
        'elitism': True,
        'variant': BasicWholeLineVariant
    })
]

CATEGORIES = {
    '5x5': COMPETITORS1,
    '5x10': COMPETITORS2,
    '10x5': COMPETITORS2,
    '10x10': COMPETITORS2,
    # '15x15',
    # '20x20',
    # '25x25',
}

def compare_single(category, competitors, name, path):
    nr = NonReader(path)
    ns = nr.read()
    output_prefix = os.path.join('results', category, name)
    
    plt.figure()
    results = {}
    
    for competitor in competitors:
        competitor_name = competitor[0]
        nga = NonogramGA(ns.clues, **competitor[1])
        with open(f'{output_prefix}_{competitor_name}.csv', 'w+') as f:
            for iteration in nga.run():
                f.write(f'{category};{name};{iteration.number};{iteration.best_fitness}\n')
        plt.plot(nga.get_bests(), label=competitor[0])
        results[competitor_name] = nga.get_bests()[-1]

    plt.legend()
    plt.title(path)
    plt.xlabel('pokolenie')
    plt.ylabel('fitness (ocena)')
    plt.savefig(output_prefix + '.png')
    plt.close()
    return results

def compare():
    with open('results/summary.csv', 'w+') as f:
        for category in tqdm(CATEGORIES):
            for filename in tqdm(os.listdir(f'db/{category}')):
                path = os.path.join('db', category, filename)
                name = filename[:-4]
                results = compare_single(category, CATEGORIES[category], name, path)
                for competitor, result in results.items():
                    f.write(f'{category};{name};{competitor};{result}\n')
                f.flush()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        single_run(sys.argv[1])
    else:
        compare()
