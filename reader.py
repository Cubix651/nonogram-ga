from models import NonogramClues, NonogramSolution

class NonReader():
    def __init__(self, path):
        self.path = path
    
    def read(self):
        with open(self.path) as f:
            has_solution = False
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if line == 'rows':
                    rows = list(self.__read_one_orientation(f))
                elif line == 'columns':
                    columns = list(self.__read_one_orientation(f))
                elif line.startswith('goal'):
                    has_solution = True
                    solution = list(map(int, line[4:].strip(' "')))
        nc = NonogramClues(columns, rows)
        if not has_solution:
            #add random solution
            solution = [x % 2 for x in range(len(columns)*len(rows))]
        ns = NonogramSolution(nc, solution)
        return ns
    
    def __read_one_orientation(self, f):
        while True:
            line = f.readline()
            if line.strip() == '':
                break
            yield list(map(int, line.split(',')))