from random import choice
from collections import defaultdict

# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    file = open("wginput1.txt","r")
    for line in file:
        for item in line.strip().split():
            yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    return_dict = defaultdict(set)
    word_list = [result_item for result_item in word_at_a_time(file)]
    for i in range(len(word_list)-os+1):
        key_tuple = tuple(word_list[i:i+os])
        try:
            return_dict[key_tuple].add(word_list[i+os])
        except IndexError:
            pass
    return_dict = dict(return_dict)
    for keys in return_dict.keys():
        return_dict[keys] = list(return_dict[keys])
    return return_dict


def corpus_as_str(corpus : {(str):[str]}) -> str:
    prt_str = "Corpus\n"
    len_min = min([len(i) for i in list(k.values())]) 
    len_max = max([len(i) for i in list(k.values())])
    for keys in sorted(list(corpus.keys())):
        prt_str += "  "+str(keys)+ " can be followed by any of "+str(corpus[keys])+"\n"
    prt_str += "max/min list lengths = "+str(len_max)+"/"+str(len_min)
    return prt_str

def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    random_text = start
    len_pattern = len(list(corpus.keys())[0])
    for i in range(count):
        if tuple(random_text[-len_pattern:]) not in list(corpus.keys()):
            random_text.append(None)
            break
        else:
            random_text.append(choice(corpus[tuple(random_text[-len_pattern:])]))
    return random_text


k = read_corpus(2,"asdf")
print(k)
print(corpus_as_str(k))
print(produce_text(k,["a","d"],10))
