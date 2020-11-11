from models import NonogramSolution
import numpy as np

def convertToSolution(clues, short_repr):
    solution = []
    width = len(clues.columns)
    for r1, r2 in zip(short_repr, clues.rows):
        row = [0 for _ in range(width)]
        r = np.array(r1) + 1
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