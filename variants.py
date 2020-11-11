from nonogram import NonogramGA
from abc import abstractstaticmethod, ABC
from models import NonogramSolution
import editdistance
import random
import numpy as np

class IVariant(ABC):
    def modify(self, ga):
        pass

class BasicVariant(IVariant):
    @classmethod
    def modify(cls, ga):
        ga.fitness_function = cls.fitness
        ga.create_individual = cls.create_individual

    @classmethod
    def fitness(cls, chromosome, clues):
        ns = NonogramSolution(clues, chromosome)
        def one_orientation(expected, actual):
            return sum(cls.fitness_one_line(x, y) for x, y in zip(expected, actual))
        return one_orientation(clues.rows, ns.solution_clues.rows) + one_orientation(clues.columns, ns.solution_clues.columns)

    @abstractstaticmethod
    def fitness_one_line(expected, actual):
        pass

    @staticmethod
    def create_individual(clues):
        cells_count = len(clues.columns) * len(clues.rows)
        return [random.randint(0, 1) for _ in range(cells_count)]

class BasicWholeLineVariant(BasicVariant):
    @staticmethod
    def fitness_one_line(expected, actual):
        return 1 if expected == actual else 0

class BasicEditDistanceVariant(BasicVariant):
    @staticmethod
    def fitness_one_line(expected, actual):
        return -editdistance.eval(expected, actual)

class BasicDiffsVariant(BasicVariant):
    @staticmethod
    def fitness_one_line(expected, actual):
        min_len = min(len(expected), len(actual))
        value_diff = np.sum(np.abs(np.array(expected[:min_len]) - np.array(actual[:min_len])))
        len_diff = abs(len(expected)-len(actual))
        return -(value_diff + len_diff)
