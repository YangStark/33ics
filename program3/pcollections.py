# Submitter: ziany(Yang, Zian)
import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable= False):
    def show_listing(s):
        for line_num, line_text in enumerate(s.split('\n'), 1):
            print(f' {line_num: >3} {line_text.rstrip()}')
## from Professor Pattis's notes
    def unique(iterable):
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i
                
    pattern  = re.compile(r'^[a-zA-Z]([a-zA-Z0-9_])*$')

    type_name = str(type_name)
    if pattern.match(type_name) == None:
        raise SyntaxError("Invalid type name")
    if type(field_names) not in [str,list]:
        raise SyntaxError("Invalid field name type") 

    if type(field_names) == str:
        field_names = field_names.replace(","," ")

    field_names = field_names.strip().split() if type(field_names)==str else field_names

    if not all([pattern.match(i)!=None for i in field_names]):
        raise SyntaxError("Invalid field names")
    if any([i in keyword.kwlist for i in field_names+[type_name]]):
        raise SyntaxError("Illegal name")
    field_names = [i for i in unique(field_names)]

    
    class_def1 ='''
class {type_name}:
    def __init__(self,{args}):

        values = [{args}]
        for i in range(len(values)):
            self.__dict__[{field_names}[i]] = values[i]

        self._fields = {field_names}
        self._mutable = {mutable}
        


    def __repr__(self):

        return "{type_name}("+",".join([i+"="+repr(self.__dict__[i]) for i in {field_names}])+")"

'''.format(type_name = type_name,args = ",".join(field_names),field_names = field_names, mutable = mutable)



    class_def2 = str("\n".join(["    def get_{x}(self):\n        return self.{x}\n".format(x=i) for i in field_names]))

    class_def3 ='''
    def __getitem__(self,iii):
        if type(iii)==int and iii<len(self._fields):

            return eval("self.get_"+self._fields[iii]+"()")
        elif type(iii) == str and iii in self._fields:
            return eval("self.get_"+iii+"()")
        else:
            raise IndexError

    def __eq__(self,right):
        if repr(self)!=repr(right):
            return False
        for i in self._fields:

            
            if self[i] != right[i]:

                return False

        return True

    def _replace(self,**kargs):

        for i in kargs.keys():
            if i not in self._fields:
                raise TypeError
        if self._mutable:
            for i in kargs.keys():
                self.__dict__[i] = kargs[i]
        else:
            rt_class_obj = {type_name}(*[self[i] for i in self._fields])
        
            rt_class_obj._mutable = True
            
            for i in kargs.keys():
                rt_class_obj.__dict__[i] = kargs[i]
            

            rt_class_obj._mutable = False

            return rt_class_obj
            
'''.format(type_name = type_name,args = ",".join(field_names),mutable = mutable)

    class_definition = class_def1+class_def2+class_def3


    # put your code here
    # bind class_definition (used below) to the string constructed for the class



    # While debugging, remove comment below showing source code for the class
    # show_listing(class_definition)
    
    # Execute this class_definition str in a local name space; then, bind the
    #   source_code attribute to class_defintion; after that try, return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict(__name__  =  f'pnamedtuple_{type_name}')
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):   
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test pnamedtuple in script below: use Point = pnamedtuple('Point','x,y')

    #driver tests
    import driver
    driver.default_file_name = 'bscp3S18.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
