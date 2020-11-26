import sys
import execjs

class Grammar():
    def __init__(self, productions):
        """Create entries that match the index of the production to the symbol, the production and the size of the production
        Productions is a list with string with the following format: S -> aa,2
        """
        self.productions = {}
        for index, line in enumerate(productions):
            S, P = line.split('->')
            S = S.replace(' ', '')
            P = P.split(',')
            p = P.pop(0).replace(' ', '')
            size = P.pop(0)
            func = CreateExec(','.join(P).replace('function(ss)', 'function(ss){')+'}') if P else None 
            self.productions[index] = {
                'symbol': S, 'production': p, 'size': int(size), 'func': func
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
        G_header = Goto.pop(0).split(',')
        # If Goto has less items than Actions then increase it to match
        while len(Goto) < len(Actions): Goto.append('')

        for index, T in enumerate(zip(Actions, Goto)):
            A, G = T
            self.states[index] = {h:a for h,a in zip(A_header,A.split(','))}
            self.states[index]['goto'] = {h:int(v) if v else None for h,v in zip(G_header, G.split(','))}

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
        # right sentential form
        rsf = input_string[:-1]
        stack = [0]
        pointer = 0
        symbol = '$'
        GenerateRow('stack', 'symbol', 'input', 'Right Sentential Form', 'action', header=True)
        # Initialize list to execute calculations
        ss = [{},{},{},{}]
        while True:
            letter = input_string[pointer]
            state = stack[-1]
            # res tell us what to do given a state and letter, this information is encoded in a string
            # with one letter and a positive interger.
            #print('Stack: ',stack)
            #print(state, letter)
            res = self.state_table[state][letter]
            #print(state, letter, res)

            # This generates a formated row with information
            GenerateRow(stack, symbol, input_string[pointer:], rsf, res)
            
            if res =='accept': 
                if ss[0]: print(ss[0])
                print('Done!!')
                return

            # we split this information into what action we do (reduce or move to a state) and which of the
            # actions we perform (the number or the state or reduction). 
            action, index = res[0], int(res[1:])
            #print(f'action: {action} index: {index}')
            
            if action.lower() == 's':
                stack.append(index)
                symbol += input_string[pointer]
                pointer +=1

            elif action.lower() == 'r':                
                production = self.grammar[index]
                size = production['size']
                sym = production['symbol']
                func = production['func']
                #print(production, ' chosen grammar: ',index)


                symbol = symbol[:-size] + sym
                rsf = symbol[1:] + input_string[pointer:-1]
                stack = stack[:-size]
                temp_state = stack[-1]
                temp_res = self.state_table[temp_state]
                stack.append(temp_res['goto'][sym])

                if func:
                    ctx = execjs.compile(func)
                    ss = ctx.call("f", ss)
                    if index in (0,1): ss[3] = ss[0].copy()
                    elif index == 2:
                        if not ss[3]: ss[3] = ss[2].copy()
                        ss[1] = {}
                    elif index == 13: 
                        if not ss[3]: ss[3] = ss[0].copy()
                        else: ss[2] = ss[0].copy()
                    elif ss[1]: ss[2] = ss[0].copy()
                    else: ss[1] = ss[0].copy()
                    print(index)
                    print(ss)
            else:
                Exception(f"""
                Someting went wrong
                Stack: {stack} 
                Symbol: {symbol}
                Action: {res}
                Input: {input_string}
                Failure at {pointer} with symbol {letter}
                """)

#.replace('X', 'DIGITS').replace('W', 'DIGIT')
def ReadFile(name, path='./'):
    """ Returns an array where every element is one line of the file
    """
    file = open(path+name, 'r')
    return [x.replace(u'\n', '') for x in file]


def GenerateRow(stack, symbol, inp, rsf, action, header = False):
    if not header:
        temp = ''
        for c in symbol:
            c = c.replace('X', 'DIGITS').replace('W', 'DIGIT')
            temp += c+' '
        symbol = temp[:-1]

        temp = ''
        for c in rsf:
            c = c.replace('X', 'DIGITS').replace('W', 'DIGIT')
            temp += c+' '
        rsf = temp[:-1]

    msg = f"|{str(stack):<25}|{symbol:<26}|{inp:<26}|{rsf:<26}|{action}|"
    print(msg)

def CreateExec(func):
    """This create a JS excetuable string"""
    # Populates objects with the necesary methods
    pop = 'function (ss) {\nfor(var i = 0; i < ss.length; i++) {\n\n\n   ss[i]["put"] = function(key,value) {this[key] = value};\n\n\n   ss[i]["containsKey"] = function(key) {return this[key] != null};\n\n\n   ss[i]["get"] = function(key) {return this[key]};\n}\n}'
    body = f'f1 = {func} \nf2 = {pop} \nf2(ss); \nf1(ss); \nreturn(ss);'
    wrapper = 'f = function(ss){ \n'+body+'\n}'
    return wrapper


def main(argv):
    action_path = argv[0]
    goto_path = argv[1]
    grammar_path = argv[2]
    input_path = argv[3]

    grammar_file = ReadFile(grammar_path)
    action_file = ReadFile(action_path)
    goto_file = ReadFile(goto_path)
    input_file = ReadFile(input_path)

    # Make it easier to process multiple word production words
    grammar_file = [x.replace('DIGITS', 'X').replace('DIGIT', 'W') for x in grammar_file]
    goto_file = [x.replace('DIGITS', 'X').replace('DIGIT', 'W') for x in goto_file]
    
    grammar = Grammar(grammar_file)
    state_table = StateTable(action_file, goto_file)
    input_string = input_file[0].replace(' ','')
    # print(grammar)

    lr =LR(grammar, state_table)
    lr.JudgeString(input_string)


if __name__ == "__main__":
   main(sys.argv[1:])