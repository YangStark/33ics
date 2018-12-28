from collections import defaultdict


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
        
        
a = Bag(['d','a','b','d','c','b','d'])
