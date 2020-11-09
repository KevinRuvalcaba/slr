import sys

class Grammar():
    def __init__(self, productions):
        """Create entries that match the index of the production to the symbol, the production and the size of the production
        Productions is a list with string with the following format: S -> aa,2
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

class StateTable():
    def __init__(self, Actions, Goto):
        self.states = {}
        # Remove the headers
        A_header = Actions.pop(0).split(',')
        Goto.pop(0)
        # If goto has less items than Actions then increase it to match
        while len(Goto) < len(Actions): Goto.append('')

        for index, T in enumerate(zip(Actions, Goto)):
            A, G = T
            self.states[index] = {h:a for h,a in zip(A_header,A.split(','))}
            self.states[index]['goto'] = int(G) if G else None

    def __getitem__(self, index):
        if index not in self.states: Exception('Index does not exist')
        return self.states[index]

    def __len__(self):
        return len(self.states)



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

    grammar_file = ReadFile(grammar_path)
    action_file = ReadFile(action_path)
    goto_file = ReadFile(goto_path)
    
    grammar = Grammar(grammar_file)
    state_table = StateTable(action_file, goto_file)

    for i in range(len(state_table)):
        print(state_table[i])



if __name__ == "__main__":
   main(sys.argv[1:])