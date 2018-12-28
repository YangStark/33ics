# Submitter: ziany(Yang, Zian)
import goody
from collections import defaultdict

def read_ndfa(file : open) -> {str:{str:{str}}}:
    ndfa = defaultdict(defaultdict)
    for line in file.readlines():
        line = line.strip().split(";")
        ndfa[line[0]] = defaultdict(set)
        for i in range(1,len(line),2):
            mapping,state = line[i],[line[i+1]]
            ndfa[line[0]][mapping].add(state[0])
        regular_dict = dict(ndfa[line[0]])
        ndfa[line[0]] = regular_dict

    ndfa = dict(ndfa)
    return ndfa

def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    prt_str = ""
    for key in sorted(ndfa.keys()):
        prt_str += "  "+key+" transitions: "+str(sorted([(key2,sorted(list(ndfa[key][key2]))) for key2 in sorted(ndfa[key])]))+"\n"
    return prt_str

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    result_list = [state]
    start = {state}
    for step in inputs:
        possible_results = []
        current_states = sorted(list(start))
        for try_state in current_states:
            possible_inputs = []
            for j in list(ndfa[try_state].keys()):
                possible_inputs.append(j)
            if step in possible_inputs:
                try:
##                print(ndfa[try_state])
                    for results in sorted(list(ndfa[try_state][step])):
                        possible_results.append(results)
                except:
                    pass
                
##                    print(possible_results)
        result_list.append((step,set(possible_results)))
        start = set(possible_results)
        if result_list[-1][1] == set():
            break

    return result_list


def interpret(result : [None]) -> str:
    prt_str = ""
    prt_str += "Start state = "+result[0]+"\n"
    for i in range(len(result)-1):
        prt_str += "  Input = "+result[i+1][0]+"; new possible states = "+str(sorted(list(result[i+1][1])))+"\n"
    prt_str += "Stop state(s) = "+str(sorted(list(result[-1][1])))+"\n"
    return prt_str




if __name__ == '__main__':
    # Write script here
    rule = read_ndfa(goody.safe_open("Choose the file name representing the non-deterministic finite automaton", "r", "Error: file does not exist"))
    print()          
    print("The Description of the chosen Non-Deterministic Finite Automaton")
    print(ndfa_as_str(rule)) 
    input_file = goody.safe_open("Choose the file name representing the start-states and their inputs","r","Error: file does not exist")
    for line in input_file.readlines():
        print("Begin tracing the next NDFA simulation")
        line = line.strip().split(";")
        print(interpret(process(rule, line[0], line[1:])))
    
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
