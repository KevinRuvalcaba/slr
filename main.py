import sys

class Grammar():
    def __init__(self, productions):
        """Create entries that match the index of the production to the symbol, the production and the size of the production
        Productions is a list with string with the following format: S -> aa 
        """
        self.productions = {}
        for index, line in enumerate(productions):
            S, P = line.replace(' ', '').split('->')
            p, size = P.split(',')
            self.productions[index+1] = {
                'symbol': S, 'production': p, 'size': size
            }
    
    def __getitem__(self, index):
        if index not in self.productions: Exception('Index does not exist')
        return self.productions[index] 

def ReadFile(name, path='./'):
    """ Returns an array where every element is one line of the file
    """
    file = open(path+name, 'r')
    return [x.replace(u'\n', '') for x in file]


def main(argv):
    action_path = argv[0]
    goto_path = argv[1]
    grammar_path = argv[2]
    input_path = argv[3]
    grammar = Grammar(ReadFile(grammar_path))


if __name__ == "__main__":
   main(sys.argv[1:])