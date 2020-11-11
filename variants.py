from nonogram import NonogramGA
from abc import abstractstaticmethod, ABC
from models import NonogramSolution
import editdistance
import random
import numpy as np
from converter import convertToSolution

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

    @staticmethod
    def convert_individual(clues, individual):
        np.array(individual).reshape(len(clues.rows), len(clues.columns))

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

class ExtendedVariant(IVariant):
    @classmethod
    def modify(cls, ga):
        ga.fitness_function = cls.fitness
        ga.create_individual = cls.create_individual
        ga.crossover_function = cls.crossover
        ga.mutate_function = cls.mutate

    @staticmethod
    def fitness(chromosome, clues):
        pass

    @staticmethod
    def create_row(clue, width):
        if not clue:
            return []
        c = np.array(clue)
        reserved = np.sum(c) + len(c) - 1
        left = width - reserved
        row = [0  for _ in range(len(c)+1)]
        for _ in range(left):
            chosen = random.randrange(0, len(row))
            row[chosen] += 1
        return row

    @classmethod
    def create_individual(cls, clues):
        width = len(clues.columns)
        return [cls.create_row(clue, width) for clue in clues.rows]

    @staticmethod
    def crossover(parent_1, parent_2):
        pass

    @staticmethod
    def mutate(individual):
        pass

    @staticmethod
    def convert_individual(clues, individual):
        ns = convertToSolution(clues, individual)
        return ns.solution