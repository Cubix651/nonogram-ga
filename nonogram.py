from pyeasyga import pyeasyga
from collections import namedtuple
import random
import numpy as np
from visualize import NonogramSolutionVisualizer
from models import NonogramSolution
import matplotlib.pyplot as plt

Iteration = namedtuple('Iteration', 'number average_fitness best_fitness best_individual')

class NonogramGA:
    def __init__(self, clues, fitness_function, **pyeasyga_parameters):
        self.__clues = clues
        self.__fitness_function = fitness_function
        self.__iterations = []
        self.__pyeasyga_parameters = pyeasyga_parameters
    
    def run(self):
        ga = pyeasyga.GeneticAlgorithm(
            self.__clues,
            **self.__pyeasyga_parameters
        )
        ga.fitness_function = self.__fitness_function

        def create_individual(clues):
            cells_count = len(clues.columns) * len(clues.rows)
            return [random.randint(0, 1) for _ in range(cells_count)]
        ga.create_individual = create_individual

        ga.create_first_generation()
        for generation_number in range(ga.generations):
            ga.create_next_generation()
            average_fitness = np.average([individual[0] for individual in ga.last_generation()])
            best_individual = np.array(ga.best_individual()[-1]).reshape(len(self.__clues.rows), len(self.__clues.columns))
            iteration = Iteration(generation_number, average_fitness, ga.best_individual()[0], best_individual)
            self.__iterations.append(iteration)
            yield iteration

    def show_best_solution(self):
        visualizer = NonogramSolutionVisualizer()
        last_iteration = self.__iterations[-1]
        solution = NonogramSolution(self.__clues, last_iteration.best_individual)
        visualizer.set_nonogram_solution(solution)
        visualizer.show()
    
    def show_statistics(self):
        averages = [iteration.average_fitness for iteration in self.__iterations]
        bests = [iteration.best_fitness for iteration in self.__iterations]
        plt.plot(averages, 'b', label='średnie')
        plt.plot(bests, 'r', label='maksymalne')
        plt.legend()
        plt.title('Działanie Alg. Genetycznego')
        plt.xlabel('pokolenie')
        plt.ylabel('fitness (ocena)')
        plt.show()