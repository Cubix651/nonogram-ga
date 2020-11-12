from PIL import Image
import numpy as np

class NonogramSolutionVisualizer:
    FILLING_COLOR_OK = (0, 0, 0)
    EMPTY_COLOR_OK = (256, 256, 256)
    FILLING_COLOR_BAD = (100, 0, 0)
    EMPTY_COLOR_BAD = (256, 223, 223)
    FILLING_COLOR_DOUBLE_BAD = (200, 0, 0)
    EMPTY_COLOR_DOUBLE_BAD = (256, 200, 200)

    def __init__(self, zoom = 20):
        self.__zoom = zoom

    def set_nonogram_solution(self, nonogram_solution):
        self.__nonogram_solution = nonogram_solution
    
    def __create_image(self):
        size = tuple(np.array(self.__nonogram_solution.solution.shape) * self.__zoom)[::-1]
        img = Image.new( 'RGB', size, "white")
        pixels = img.load()
        self.__add_solution(pixels)
        return img
    
    def __add_solution(self, pixels):
        solution = self.__nonogram_solution.solution
        row_correctness = self.__nonogram_solution.row_correctness
        column_correctness = self.__nonogram_solution.column_correctness

        for row in range(solution.shape[0]):
            for column in range(solution.shape[1]):
                if solution[row, column] > 0:
                    if row_correctness[row] and column_correctness[column]:
                        color = NonogramSolutionVisualizer.FILLING_COLOR_OK
                    elif row_correctness[row] or column_correctness[column]:
                        color = NonogramSolutionVisualizer.FILLING_COLOR_BAD
                    else:
                        color = NonogramSolutionVisualizer.FILLING_COLOR_DOUBLE_BAD
                else:
                    if row_correctness[row] and column_correctness[column]:
                        color = NonogramSolutionVisualizer.EMPTY_COLOR_OK
                    elif row_correctness[row] or column_correctness[column]:
                        color = NonogramSolutionVisualizer.EMPTY_COLOR_BAD
                    else:
                        color = NonogramSolutionVisualizer.EMPTY_COLOR_DOUBLE_BAD
                self.__fill_field(pixels, column, row, color)


    def __fill_field(self, pixels, x, y, color):
        for a in range(self.__zoom):
            for b in range(self.__zoom):
                pixels[x*self.__zoom + a, y*self.__zoom + b] = color

    def show(self):
        img = self.__create_image()
        img.show()
