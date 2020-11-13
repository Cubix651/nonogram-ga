from pyeasyga import pyeasyga
from collections import namedtuple
import random
import numpy as np
from visualize import NonogramSolutionVisualizer
from models import NonogramSolution
import matplotlib.pyplot as plt

Iteration = namedtuple('Iteration', 'number average_fitness best_fitness best_individual')

class NonogramGA:
    def __init__(self, clues, variant, **pyeasyga_parameters):
        self.__clues = clues
        self.__variant = variant
        self.__iterations = []
        self.__pyeasyga_parameters = pyeasyga_parameters

    def run(self):
        ga = pyeasyga.GeneticAlgorithm(
            self.__clues,
            **self.__pyeasyga_parameters
        )
        self.__variant.modify(ga)

        ga.create_first_generation()
        for generation_number in range(ga.generations):
            ga.create_next_generation()
            average_fitness = np.average([individual[0] for individual in ga.last_generation()])
            best_individual = self.__variant.convert_individual(self.__clues, ga.best_individual()[-1])
            iteration = Iteration(generation_number, average_fitness, ga.best_individual()[0], best_individual)
            self.__iterations.append(iteration)
            yield iteration

    def get_best_solution(self):
        last_iteration = self.__iterations[-1]
        return last_iteration.best_individual

    def get_best_fitness(self):
        last_iteration = self.__iterations[-1]
        return last_iteration.best_fitness
    
    def get_bests(self):
        return [iteration.best_fitness for iteration in self.__iterations]

    def show_best_solution(self):
        visualizer = NonogramSolutionVisualizer()
        last_iteration = self.__iterations[-1]
        solution = NonogramSolution(self.__clues, last_iteration.best_individual)
        visualizer.set_nonogram_solution(solution)
        visualizer.show()
    
    def show_statistics(self):
        averages = [iteration.average_fitness for iteration in self.__iterations]
        bests = self.get_bests()
        plt.plot(averages, 'b', label='średnie')
        plt.plot(bests, 'r', label='maksymalne')
        plt.legend()
        plt.title('Działanie Alg. Genetycznego')
        plt.xlabel('pokolenie')
        plt.ylabel('fitness (ocena)')
        plt.show()