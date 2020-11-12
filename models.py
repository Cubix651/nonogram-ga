import numpy as np

class NonogramClues:
    def __init__(self, columns, rows):
        self.columns = np.array(columns, dtype=object)
        self.rows = np.array(rows, dtype=object)

class NonogramSolution:
    def __init__(self, clues, solution):
        self.clues = clues
        self.solution = np.array(solution).reshape(len(clues.rows), len(clues.columns))
        self.solution_clues = self.__get_clues(self.solution)
        self.row_correctness = (self.clues.rows == self.solution_clues.rows)
        self.column_correctness = (self.clues.columns == self.solution_clues.columns)

    def __get_clues(self, solution):
        return NonogramClues(
            columns = self.__get_clues_for_one_orientation(self.solution.T),
            rows = self.__get_clues_for_one_orientation(self.solution)
        )

    def __get_clues_for_one_orientation(self, solution):
        return np.array([self.__convert_line(row) for row in solution], dtype=object)

    def __convert_line(self, line):
        result = []
        for prev, cur in zip([0, *line[:-1]], line):
            if prev == 0 and cur == 1:
                result.append(1)
            if prev == 1 and cur == 1:
                result[-1] = result[-1]+1
        return result