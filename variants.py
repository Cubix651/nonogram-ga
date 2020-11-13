from nonogram import NonogramGA
from abc import abstractstaticmethod, ABC
from models import NonogramSolution
import editdistance
import random
import numpy as np
from converter import NonogramConverter

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
        return 1 if expected == list(actual) else 0

    @classmethod
    def fitness(cls, chromosome, clues):
        ok = super().fitness(chromosome, clues)
        return ok - len(clues.rows) - len(clues.columns)

class BasicEditDistanceVariant(BasicVariant):
    @staticmethod
    def fitness_one_line(expected, actual):
        return -editdistance.eval(expected, actual)

class BasicDiffsVariant(BasicVariant):
    @staticmethod
    def fitness_one_line(expected, actual):
        min_len = min(len(expected), len(actual))
        value_diff = np.sum(np.abs(np.array(expected[:min_len]) - np.array(actual[:min_len])))
        missing_sum = sum(expected[min_len:])+sum(actual[min_len:])
        return -(value_diff + missing_sum)

class ExtendedVariant(IVariant):
    @classmethod
    def modify(cls, ga):
        ga.fitness_function = cls.fitness
        ga.create_individual = cls.create_individual
        ga.crossover_function = cls.crossover
        ga.mutate_function = cls.mutate

    @abstractstaticmethod
    def fitness_one_line(expected, actual):
        pass

    @classmethod
    def fitness(cls, chromosome, clues):
        ns = NonogramConverter.convert_to_solution(clues, chromosome)
        def one_orientation(expected, actual):
            return sum(cls.fitness_one_line(x, y) for x, y in zip(expected, actual))
        return one_orientation(clues.rows, ns.solution_clues.rows) + one_orientation(clues.columns, ns.solution_clues.columns)

    @staticmethod
    def create_repr(left, length):
        row = [random.randint(0, left) for _ in range(length)]
        row.sort()
        result = []
        for prev, cur in zip([0, *row], [*row, left]):
            result.append(cur - prev)
        return result
        
    @classmethod
    def create_row(cls, clue, width):
        if not clue:
            return []
        c = np.array(clue)
        reserved = np.sum(c) + len(c) - 1
        left = width - reserved
        return cls.create_repr(left, len(c)+1)

    @classmethod
    def create_individual(cls, clues):
        width = len(clues.columns)
        return [cls.create_row(clue, width) for clue in clues.rows]

    @staticmethod
    def crossover(parent_1, parent_2):
        child_1 = []
        child_2 = []
        for index in range(len(parent_1)):
            if random.randint(0,1) > 0:
                child_1, child_2 = child_2, child_1
            child_1.append(parent_1[index])
            child_2.append(parent_2[index])
        return child_1, child_2

    @classmethod
    def mutate(cls, individual):
        row_index = random.randrange(len(individual))
        old_repr = np.array(individual[row_index])
        individual[row_index] = cls.create_repr(np.sum(old_repr), len(old_repr))
        
    @staticmethod
    def convert_individual(clues, individual):
        ns = NonogramConverter.convert_to_solution(clues, individual)
        return ns.solution

class ExtendedDiffVariant(ExtendedVariant):
    @staticmethod
    def fitness_one_line(expected, actual):
        min_len = min(len(expected), len(actual))
        value_diff = np.sum(np.abs(np.array(expected[:min_len]) - np.array(actual[:min_len])))
        missing_sum = sum(expected[min_len:])+sum(actual[min_len:])
        return -(value_diff + missing_sum)

class ExtendedWholeLineVariant(ExtendedVariant):
    @staticmethod
    def fitness_one_line(expected, actual):
        return 1 if expected == list(actual) else 0
    
    @classmethod
    def fitness(cls, chromosome, clues):
        ok = super().fitness(chromosome, clues)
        return ok - len(clues.rows) - len(clues.columns)
