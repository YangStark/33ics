# Submitter: ziany(Yang, Zian)
from collections import defaultdict
from goody import type_as_str
import prompt

class Bag:
    def __init__(self,*iterable):
        self._info = defaultdict(int)
        if len(iterable) == 0:
            return None
        for i in iterable[0]:
            self._info[i] += 1

    def __repr__(self):
        temp_list = []
        if len(self._info.keys()) == 0:
            return "Bag()"
        else:
            for key,value in self._info.items():
                for i in range(value):
                    temp_list.append(key)
            return "Bag(['"+"','".join(temp_list)+"'])"
    def __str__(self):

        temp_str = "Bag("
        for key,value in self._info.items():
            temp_str += key+"["+str(value)+"],"
        if temp_str[-1] == "(":
            temp_str = temp_str+")"
        else:
            temp_str = temp_str[:-1]+")"

        return temp_str
    def __len__(self):
        return sum(list(self._info.values()))
    def unique(self):
        return len(list(self._info.keys()))
    def __contains__(self,contain_key):
        return contain_key in list(self._info.keys())
    def count(self,count_key):
        if count_key in self._info.keys():
            return self._info[count_key]
        return 0
    def add(self,add_key):
        self._info[add_key] += 1

    def __add__(self,add_key):
        if type(add_key) != Bag:
            raise TypeError(str(type(add_key))+" is not supported by +")
        temp_add = defaultdict(int)
        for key,value in add_key._info.items():
            temp_add[key] += value
        for key,value in self._info.items():
            temp_add[key] += value
        rt_bag = Bag([0])
        rt_bag._info = temp_add
        return rt_bag

    def remove(self,remove_key):
        if remove_key in list(self._info.keys()):
            if self._info[remove_key] == 1:
                del self._info[remove_key]
            else:
                self._info[remove_key] -= 1
        else:
            raise ValueError(remove_key+" not in the Bag")
        
    def __eq__(self,eq_bag):
        if type(eq_bag) != Bag:
            return False
        for key,value in eq_bag._info.items():
            if eq_bag._info[key] != self._info[key]:
                return False
        if len(list(self._info.keys())) != len(list(eq_bag._info.keys())):
            return False
        return True

    def __iter__(self):
        self._iterlist = defaultdict(int,{k:self._info[k] for k in self._info})
        return iter([k for k in self._info for i in range(self._info[k])])

    def __next__(self):
        if list(self._iterlist.keys()) == []:
            raise StopIteration
        else:
            for i in self._iterlist.keys():
                rt_key = i
                if self._iterlist[rt_key] ==1:
                    del self._iterlist[rt_key]
                else:
                    self._iterlist[rt_key] -= 1
                return rt_key
        
        




if __name__ == '__main__':
    
    #Simple tests before running driver
    #Put your own test code here to test Bag before doing the bsc tests
    #Debugging problems with these tests is simpler

    b = Bag(['d','a','d','b','c','b','d'])
    print(repr(b))
    print(all((repr(b).count('\''+v+'\'')==c for v,c in dict(a=1,b=2,c=1,d=3).items())))
    for i in b:
        print(i)

    b2 = Bag(['a','a','b','x','d'])
    print(repr(b2+b2))
    print(str(b2+b2))
    print([repr(b2+b2).count('\''+v+'\'') for v in 'abdx'])
    b = Bag(['a','b','a'])
    print(repr(b))
    print()
    
    import driver
    driver.default_file_name = 'bscp21F18.txt'
#     driver.default_show_exception = prompt.for_bool('Show exceptions when testing',True)
#     driver.default_show_exception_message = prompt.for_bool('Show exception messages when testing',True)
#     driver.default_show_traceback = prompt.for_bool('Show traceback when testing',True)
    driver.driver()
