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
                'symbol': S, 'production': p, 'size': int(size)
            }
    
    def __getitem__(self, index):
        if index not in self.productions: Exception('Index does not exist')
        return self.productions[index] 

    def __str__(self):
        msg = ''
        for key,val in self.productions.items():
            msg += f'{key} : {val} \n'
        return msg

class StateTable():
    def __init__(self, Actions, Goto):
        self.states = {}
        # Remove the headers
        A_header = Actions.pop(0).split(',')
        Goto.pop(0)
        # If Goto has less items than Actions then increase it to match
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

    def __str__(self):
        msg = ''
        for key,val in self.states.items():
            msg += f'{key} : {val} \n'
        return msg


class LR():
    def __init__(self, grammar, state_table):
        self.grammar = grammar
        self.state_table = state_table


    def JudgeString(self, input_string):
        stack = [0]
        pointer = 0
        symbol = '$'
        GenerateRow('stack', 'symbol', 'input', 'action')
        while True:
            letter = input_string[pointer]
            state = stack[-1]
            # res tell us what to do given a state and letter, this information is encoded in a string
            # with one letter and a positive interger.
            #print(state, letter)
            res = self.state_table[state][letter]

            # This generates a formated row with information
            GenerateRow(stack, symbol, input_string[pointer:], res)
            
            if res =='accept': 
                print('Done!!')
                return

            # we split this information into what action we do (reduce or move to a state) and which of the
            # actions we perform (the number or the state or reduction). 
            action, index = res[0], int(res[1:])
            
            
            if action == 's':
                stack.append(index)
                symbol += input_string[pointer]
                pointer +=1

            elif action == 'r':
                production = self.grammar[index]
                size = production['size']
                sym = production['symbol']

                symbol = symbol[:-size] + sym
                stack = stack[:-size]
                temp_state = stack[-1]
                temp_res = self.state_table[temp_state]
                stack.append(temp_res['goto'])

            else:
                Exception(f"""
                Someting went wrong
                Stack: {stack} 
                Symbol: {symbol}
                Action: {res}
                Input: {input_string}
                Failure at {pointer} with symbol {letter}
                """)


def ReadFile(name, path='./'):
    """ Returns an array where every element is one line of the file
    """
    file = open(path+name, 'r')
    return [x.replace(u'\n', '') for x in file]


def GenerateRow(stack, symbol, inp, action):
    msg = f"|{str(stack):<20}|{symbol:<20}|{inp:<25}|{action}|"
    print(msg)

def main(argv):
    action_path = argv[0]
    goto_path = argv[1]
    grammar_path = argv[2]
    input_path = argv[3]

    grammar_file = ReadFile(grammar_path)
    action_file = ReadFile(action_path)
    goto_file = ReadFile(goto_path)
    input_file = ReadFile(input_path)
    
    grammar = Grammar(grammar_file)
    state_table = StateTable(action_file, goto_file)
    input_string = input_file[0].replace(' ','')

    lr =LR(grammar, state_table)
    lr.JudgeString(input_string)


if __name__ == "__main__":
   main(sys.argv[1:])