
def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    preference = {}
    for line in open_file.readlines():
        line = line.strip().split(";")
        preference[line[0]]=[None,[line[i+1] for i in range(len(line)-1)]]
    return preference

def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    prt_str = ""
    for key in d:
        prt_str += "  "+str(key+" -> "+str(d[key])+"\n")
    return prt_str

def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return p1 if order.index(p1) < order.index(p2) else p2

def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return set((male,men[male][0]) for male in men)
    

def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    men_dict_copy = men
    current_match = dict((women,None) for women in women.keys())
    print(current_match)
    unmatched = set([i for i in men_dict_copy.keys()])
    print(unmatched,"unmatched")

    while len(unmatched) != 0:
        pairing_men = unmatched.pop()
        
        while men_dict_copy[pairing_men][0] == None:
            prefer_women = men_dict_copy[pairing_men][1].pop(0)
            
            if current_match[prefer_women] == None:
                men_dict_copy[pairing_men][0] = prefer_women ###None -> propose accepted
                current_match[prefer_women] = pairing_men
                
            else:
                print(women[prefer_women],"asdfasdfasdfasdfasfd")

                if pairing_men == who_prefer(women[prefer_women][1],current_match[prefer_women],pairing_men):
                    men_dict_copy[current_match[prefer_women]][0] = None     ###else divorced
                    unmatched.add(current_match[prefer_women])###else become unmatched
                    men_dict_copy[pairing_men][0] = prefer_women ###else -> propose accepted
                    current_match[prefer_women] = pairing_men

                else:
                    pass ###he got rejected by the current prefered women and go to next round
    print(extract_matches(men_dict_copy))


    return men_dict_copy
        
    

p = open("men2.txt","r")
q = open("women2.txt","r")
men0 = read_match_preferences(p)
women0 = read_match_preferences(q)
o = dict_as_str(p)
print(o)

def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    return p1 if order.index(p1) < order.index(p2) else p2

output = make_match(men0,women0)
op = dict_as_str(output)
print(op)
