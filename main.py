import sys

def ReadFile(name, path='./'):
    file = open(path+name, 'r')
    return [x.replace(u'\n', '') for x in file]


def main(argv):
    action_path = argv[0]
    goto_path = argv[1]
    grammar_path = argv[2]
    input_path = argv[3]
    for ele in ReadFile(action_path): print(ele)
    for ele in ReadFile(goto_path): print(ele)
    for ele in ReadFile(grammar_path): print(ele)
    for ele in ReadFile(input_path): print(ele)


if __name__ == "__main__":
   main(sys.argv[1:])