import sys
import numpy as np
from uuid import uuid4 as uuid
from converter import NonogramConverter

class NonogramGenerator:
    def __init__(self, directory, shape):
        self.directory = directory
        self.shape = shape

    def generate(self, count):
        for _ in range(count):
            name = uuid()
            self.generate_single(name)

    def generate_single(self, name):
        example = np.random.randint(2, size=self.shape)
        nc = NonogramConverter.convert_to_clues(example)
        path = f'{self.directory}/{name}.non'
        with open(path, 'w') as f:
            f.write(f'title "{name}"\n')
            f.write(f'width {self.shape[0]}\n')
            f.write(f'height {self.shape[1]}\n')
            f.write('\n')
            f.write('rows\n')
            self.__generate_one_orientation(f, nc.rows)
            f.write('\n')
            f.write('columns\n')
            self.__generate_one_orientation(f, nc.columns)
            f.write('\n')
            goal = ''.join(map(str, example.flatten()))
            f.write(f'goal "{goal}"\n')
    
    def __generate_one_orientation(self, f, orientation_clues):
        for single in orientation_clues:
            f.write(','.join(map(str, single)))
            f.write('\n')


def main():
    if len(sys.argv) < 5:
        return 
    directory = sys.argv[1]
    shape = tuple(map(int, sys.argv[2:4]))
    count = int(sys.argv[4])
    gen = NonogramGenerator(directory, shape)
    gen.generate(count)

if __name__ == "__main__":
    main()