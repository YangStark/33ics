# Submitter: ziany(Yang, Zian)
import goody
from goody import irange
import prompt
from random import choice
from collections import defaultdict


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    return_dict = defaultdict(list)
    word_list = [result_item for result_item in word_at_a_time(file)]
    for i in range(len(word_list)-os):
        key_tuple = tuple(word_list[i:i+os])
        try:
            if word_list[i+os] not in return_dict[key_tuple]:
                return_dict[key_tuple].append(word_list[i+os])
            else:
                pass
        except IndexError:
            pass
    return_dict = dict(return_dict)
    for keys in return_dict.keys():
        return_dict[keys] = list(return_dict[keys])
    return return_dict


def corpus_as_str(corpus : {(str):[str]}) -> str:
    prt_str = ""
    len_min = min([len(i) for i in list(corpus.values())]) 
    len_max = max([len(i) for i in list(corpus.values())])
    for keys in sorted(list(corpus.keys())):
        prt_str += "  "+str(keys)+ " can be followed by any of "+str(corpus[keys])+"\n"
    prt_str += "max/min list lengths = "+str(len_max)+"/"+str(len_min)+"\n"
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



        
if __name__ == '__main__':
    # Write script here
    while True:
        try:
            os = int(input("Choose the order statistic:"))          
            input_file  = read_corpus(os,goody.safe_open("Choose the file name to process", "r", "Error: file does not exist"))
            break
        except ValueError:
            print("Invalid Input, Please type a integer for order statistic")
            pass
    print("Corpus\n")
    print(corpus_as_str(input_file))
    while True:
        print("Choose "+str(os)+" words to start with")
        try: 
            word_list = []
            for i in range(os):
                word_list.append(input("Choose word "+str(i+1)+":"))
            num_words = int(input("Choose # of words for generation:"))
            break
        except ValueError:
            print("Invalid Input, Please type a integer for number of words")
    print("Random text ="+str(produce_text(input_file,word_list,num_words)))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
