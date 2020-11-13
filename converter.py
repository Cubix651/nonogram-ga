from models import NonogramClues, NonogramSolution
import numpy as np

class NonogramConverter:
    @staticmethod
    def convert_to_solution(clues, short_repr):
        solution = []
        width = len(clues.columns)
        for r1, r2 in zip(short_repr, clues.rows):
            row = [0 for _ in range(width)]
            r = np.array(r1[:-1]) + 1
            r[0] -= 1
            idx = 0
            for x, y in zip(r, r2):
                idx += x
                for z in range(y):
                    row[idx+z] = 1
                idx += y
            solution.append(row)
        solution = np.array(solution)
        return NonogramSolution(clues, solution)

    @classmethod
    def convert_to_clues(cls, solution):
        return NonogramClues(
            columns = cls.__get_clues_for_one_orientation(solution.T),
            rows = cls.__get_clues_for_one_orientation(solution)
        )

    @classmethod
    def __get_clues_for_one_orientation(cls, solution):
        return np.array([cls.__convert_line(row) for row in solution], dtype=object)

    @classmethod
    def __convert_line(cls, line):
        result = []
        for prev, cur in zip([0, *line[:-1]], line):
            if prev == 0 and cur == 1:
                result.append(1)
            if prev == 1 and cur == 1:
                result[-1] = result[-1]+1
        return result
