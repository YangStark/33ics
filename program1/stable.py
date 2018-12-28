# Submitter: ziany(Yang, Zian)
import prompt
import goody

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    preference = {}
    for line in open_file.readlines():
        line = line.strip().split(";")
        preference[line[0]]=[None,[line[i+1] for i in range(len(line)-1)]]
    return preference

def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    prt_str = ""
    for keys in sorted(d,key = key, reverse = reverse):
        prt_str += "  "+str(keys+" -> "+str(d[keys])+"\n")
    return prt_str



def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return p1 if order.index(p1) < order.index(p2) else p2



def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return set((male,men[male][0]) for male in men)
    

def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    men_dict_copy = men
    prt_str = ""
    prt_str += "Women Preferences (unchanging)\n"+dict_as_str(women)
    
    current_match = dict((women,None) for women in women.keys())
    unmatched = set([i for i in men_dict_copy.keys()])
    while len(unmatched) != 0:
        pairing_men = unmatched.pop()
        while men_dict_copy[pairing_men][0] == None:
            prt_str += "Men Preferences (current)\n"+dict_as_str(men)+"\n"
            prt_str += "unmatched men = "+str(unmatched)+"\n"

            prefer_women = men_dict_copy[pairing_men][1].pop(0)
            
            if current_match[prefer_women] == None:
                prt_str += pairing_men+" "+"proposes to "+prefer_women+", who is currently unmatched, accepting the proposal"
                men_dict_copy[pairing_men][0] = prefer_women ###None -> propose accepted
                current_match[prefer_women] = pairing_men
            else:
                if pairing_men == who_prefer(women[prefer_women][1],current_match[prefer_women],pairing_men):
                    prt_str += pairing_men+" "+"proposes to "+prefer_women+", who is currently matched, accepting the proposal"+", rejecting match with "+current_match[prefer_women]
                    men_dict_copy[current_match[prefer_women]][0] = None     ###else divorced
                    unmatched.add(current_match[prefer_women])###else become unmatched
                    men_dict_copy[pairing_men][0] = prefer_women ###else -> propose accepted
                    current_match[prefer_women] = pairing_men
                else:
                    prt_str += pairing_men+" "+"proposes to "+prefer_women+", who is currently matched, rejecting the proposal (likes current match better)"
                    pass ###he got rejected by the current prefered women and go to next round
            prt_str += "\n"
    fresult = extract_matches(men_dict_copy)
    if trace:
        print(prt_str+"algorithm stopped: matches = "+str(fresult))
    else:
        print("matches = "+str(fresult))
    return fresult



  
    
if __name__ == '__main__':
    # Write script here
    men_data = read_match_preferences(goody.safe_open("Choose the file name representing preferences of the men","r","Error: file does not exist"))
    women_data = read_match_preferences(goody.safe_open("Choose the file name representing preferences of the women","r","Error: file does not exist"))
    print()
    print("Men Preferences")
    print(dict_as_str(men_data))
    print("Women Preferences")
    print(dict_as_str(women_data))
    trace_on = prompt.for_bool("Choose whether to trace this algorithm", True, "Invalid bool") 
    finalmatch = make_match(men_data,women_data,trace_on)
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
