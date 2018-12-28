# Submitter: ziany(Yang, Zian)
import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    graph = {}
    openfile = file
    for line in openfile.readlines():
        line = line.strip()
        if line.split(";")[0] not in graph:
            graph[line.split(";")[0]]=set([str(line.split(";")[1])])
        else:
            graph[line.split(";")[0]].add(str(line.split(";")[1]))
    return graph               

def graph_as_str(graph : {str:{str}}) -> str:
    return_str = ""
    for key in sorted(graph):
        return_str += "  "+str(key+" -> "+str(sorted(graph[key]))+"\n")
    return return_str
        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reached_set = set([])
    exploring_list = [start]
    while exploring_list != []:
        prt_str = "reached set    = "+(str(reached_set) if len(reached_set)>0 else "set()")+"\n"+"exploring list = "+str(exploring_list)+"\n"
        explore_temp = exploring_list.pop(0)
        prt_str += "removing node from exploring list and adding it to reached list: node = "+str(explore_temp)+"\n"      
        if explore_temp not in reached_set:
            if graph.get(explore_temp) != None:
                exploring_list = list(set(exploring_list+list(graph.get(explore_temp))))
                reached_set.add(explore_temp)
            else:
                reached_set.add(explore_temp)
        prt_str += "after adding all nodes reachable directly from f but not already in reached, exploring = "+str(exploring_list)
        if trace == True:
            print(prt_str+"\n")
 
    return reached_set





if __name__ == '__main__':
    # Write script here
    graphk = goody.safe_open("Choose the file name representing the graph", "r", "Error: file does not exist")                  
    k = read_graph(graphk)
    print()
    print("Graph: any node -> [all that node's destination nodes]")
    print(graph_as_str(k))
    while True:
        input_from_user = str(input("Choose the start node (or choose quit): "))
        if input_from_user not in k.keys() and input_from_user != "quit":
            print("  Entry Error:",input_from_user,";  Illegal: not a source node\n  Please enter a legal String")    
        elif input_from_user in k.keys():
            trace_on = prompt.for_bool("Choose whether to trace this algorithm", True, "Invalid bool")
            print("From e the reachable nodes are",reachable(k,input_from_user,trace_on))
        elif input_from_user == "quit":
            break
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
