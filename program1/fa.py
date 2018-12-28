# Submitter: ziany(Yang, Zian)
import goody


def read_fa(file:open) ->{}:
    fa = {}
    for line in file.readlines():
        line = line.strip().split(";")
        fa[line[0]] = dict((line[2*(i+1)-1],line[2*(i+1)]) for i in range(len(line)//2))
    return fa

def fa_as_str(fa : {str:{str:str}}) -> str:
    prt_str = ""
    for key in sorted(fa.keys()):
        prt_str += "  "+key+" transitions: "+str([(key2,fa[key][key2]) for key2 in sorted(fa[key])])+"\n"
    return prt_str

def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    result_list = [state]
    possible_inputs = list(fa[state].keys())
    start = state
    for step in inputs:
        if step in possible_inputs:

            result_list.append((step,fa[start][step]))
            start = fa[start][step]

        else:
            result_list.append((step,None))
            break
    return result_list

def interpret(fa_result : [None]) -> str:
    prt_str = "Start state = "+fa_result[0]+"\n"
    for i in range(len(fa_result)-1):
        if fa_result[i+1][1] != None:
            prt_str += "  Input = "+fa_result[i+1][0]+"; new state = "+fa_result[i+1][1]+"\n"
        else:
            prt_str += "  Input = "+fa_result[i+1][0]+"; illegal input: simulation terminated\n"
    if fa_result[-1][1] != None:
        prt_str += "Stop state = "+fa_result[i+1][1]+"\n"
    else:
        prt_str += "Stop state = None\n"
    return prt_str





if __name__ == '__main__':
    # Write script here
    rule = read_fa(goody.safe_open("Choose the file name representing the finite automaton", "r", "Error: file does not exist"))
    print()
    print("The Description of the chosen Finite Automaton\n")
    print(fa_as_str(rule)) 
    input_file = goody.safe_open("Choose the file name representing the start-states and their inputs","r","Error: file does not exist")
    for line in input_file.readlines():
        print("Begin tracing the next FA simulation")
        line = line.strip().split(";")
        print(interpret(process(rule, line[0], line[1:])))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
