import numpy as np
import converter
class NonogramClues:
    def __init__(self, columns, rows):
        self.columns = np.array(columns, dtype=object)
        self.rows = np.array(rows, dtype=object)

class NonogramSolution:
    def __init__(self, clues, solution):
        self.clues = clues
        self.solution = np.array(solution).reshape(len(clues.rows), len(clues.columns))
        self.solution_clues = converter.NonogramConverter.convert_to_clues(self.solution)
        self.row_correctness = (self.clues.rows == self.solution_clues.rows)
        self.column_correctness = (self.clues.columns == self.solution_clues.columns)
