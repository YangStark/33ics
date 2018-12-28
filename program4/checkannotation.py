from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self,check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self,check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # Below, setting the class attribute to True allows checking to occur
    #   (but only if self._checking_on is also True)
    checking_on  = True
  
    # set self._checking_on to True too, for checking the decorated function 
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
class Check_Annotation:
    # Below, setting the class attribute to True allows checking to occur
    #   (but only if self._checking_on is also True)
    checking_on  = True
  
    # set self._checking_on to True too, for checking the decorated function 
    def __init__(self, f):
        self._f = f
        self._checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.

    def check(self,param,annot,value,check_history=''):
        if annot == None:
            return None
        else:
            def p():pass##functionclass\

            if annot in [int,float,str,list,dict,tuple,set,frozenset,type(p)]:###enter if not instance just word 
                assert annot == type(value), ''''{var}' failed annotation check(wrong type): value = {value}
  was type {type_F} ...should be type {type_T}{history}'''.format(var = param,value = "'"+value+"'" if type(value)==str else value,type_F = value.__class__.__name__,type_T = annot.__name__,history = check_history)
            else:
###for list & tuple
                if type(annot) in [list,tuple]:               
                    ##make sure the value is typelist    
                    assert type(value) == type(annot),''''{var}' failed annotation check(wrong type): value = {value}
  was type {type_F} ...should be type {type_T}{history}'''.format(var = param,value = "'"+value+"'" if type(value)==str else value,type_F = value.__class__.__name__,type_T = type(annot).__name__,history = check_history)
                        
                    if len(annot) == 1:##make sure every element is correct type
                        h = ""
                        for i in range(len(value)):
                            if i == 0:
                                h += "\n{typelistortuple}[{count}] check: {classinfo}".format(typelistortuple = type(annot).__name__,count = i,classinfo = annot[0])
                            else:
                                h += "\n{typelistortuple}[{count}] check: {classinfo}".format(typelistortuple = type(annot).__name__,count = i,classinfo = annot[0])
                            self.check(param,annot[0],value[i],check_history+h)
                            h = ""
                    elif len(annot) >1:##make sure for annot>1
                        assert len(annot) == len(value),''''{var}' failed annotation check(wrong type): value = {value}
  annotation had {numberofele} elements{annot}'''.format(var = param,value =  "'"+value+"'" if type(value)==str else value,numberofele = len(annot),annot = annot)
                        for i in range(len(annot)):
                            h = "\n{typelistortuple}[{count}] check: {classinfo}".format(typelistortuple = type(annot).__name__,count = i,classinfo = annot[i])
                            self.check(param,annot[i],value[i],check_history+h)


##for dict
                if type(annot) == dict:
                    assert type(value) == dict,''''{var}' failed annotation check(wrong type): value = {value}
  was type {type_F} ...should be type {type_T}{history}'''.format(var = param,value = "'"+value+"'" if type(value)==str else value,type_F = value.__class__.__name__,type_T = type(annot).__name__,history = check_history)

                    if len(annot) == 1:
                        h = ""
                        for i in range(len(value)):##check key
                            h += "\ndict {attr} check: {classinfo}".format(attr = "key",classinfo = list(annot.keys())[0])
                            self.check(param,list(annot.keys())[0],list(value.keys())[i],check_history+h)
                            h = ""
                        for j in range(len(value)):##check value
                            h +="\ndict {attr} check: {classinfo}".format(attr = "value",classinfo = list(annot.values())[0])
                            self.check(param,list(annot.values())[0],list(value.values())[j],check_history+h)
                            h = ""

                    elif len(list(annot.keys()))>1:##raise error for 
                        assert False,''''{var}' annotation inconsistency: dict should have 1 item but had {lenannot}
  annotation = {annot}'''.format(var = param,lenannot = len(list(annot.keys())),lenvalue = len(list(value.keys())),numberofele = len(annot),annot = annot)
###for set for frozenset
                if type(annot) in [set,frozenset]:
                    assert type(value) == type(annot),''''{var}' failed annotation check(wrong type): value = {value}
  was type {type_F} ...should be type {type_T}{history}'''.format(var = param,value = "'"+value+"'" if type(value)==str else value,type_F = value.__class__.__name__,type_T = type(annot).__name__,history = check_history)

                    if len(annot) == 1:
                        h = ""
                        listannot =list(annot)
                        listset = list(value)
                        for i in range(len(value)):
                            h +="\n{settype} value check: {classinfo}".format(settype = type(annot).__name__,classinfo = listannot[0])
                            self.check(param,listannot[0],listset[i],check_history+h)
                            h = ""
                    elif len(list(annot))>1:##raise error for
                        assert False,''''{var}' annotation inconsistency: {settype} should have 1 item but had {lenannot}
  annotation = {annot}'''.format(var = param,settype = type(annot).__name__,lenannot = len(list(annot)),lenvalue = len(list(value)),numberofele = len(annot),annot = annot)
###for lambda
                if inspect.isfunction(annot):
                    ###for multiple input

                    assert len(annot.__code__.co_varnames) == 1, ''''{var}' annotation inconsistency: predicate should have 1 parameter but had {lenannot}
  predicate = {annot}'''.format(var = param,lenannot = len(annot.__code__.co_varnames),annot = annot)
                    rt = False
                    try:
                        rt = annot(value)
                    except Exception as errorinfo:
                        raise AssertionError(''''{var}' annotation predicate({annot}) raised exception\n  exception = '''.format(var = param,annot = annot)+str(errorinfo)+check_history)

                    h = ''''{var}' failed annotation check: value = {value}
  predicate = {annot}'''.format(var = param,value = "'"+value+"'" if type(value)==str else value,lenannot = len(annot.__code__.co_varnames),annot = annot)
                    
                    h += check_history
                    assert rt,h
                if inspect.isfunction(annot):
                    ###for multiple input

                    assert len(annot.__code__.co_varnames) == 1, ''''{var}' annotation inconsistency: predicate should have 1 parameter but had {lenannot}
  predicate = {annot}'''.format(var = param,lenannot = len(annot.__code__.co_varnames),annot = annot)
                    rt = False
                    try:
                        rt = annot(value)
                    except Exception as errorinfo:
                        raise AssertionError(''''{var}' annotation predicate({annot}) raised exception\n  exception = '''.format(var = param,annot = annot)+str(errorinfo)+check_history)

                    h = ''''{var}' failed annotation check: value = {value}
  predicate = {annot}'''.format(var = param,value = "'"+value+"'" if type(value)==str else value,lenannot = len(annot.__code__.co_varnames),annot = annot)
                    
                    h += check_history
                    assert rt,h
                if inspect.isfunction(annot):
                    ###for multiple input

                    assert len(annot.__code__.co_varnames) == 1, ''''{var}' annotation inconsistency: predicate should have 1 parameter but had {lenannot}
  predicate = {annot}'''.format(var = param,lenannot = len(annot.__code__.co_varnames),annot = annot)
                    rt = False
                    try:
                        rt = annot(value)
                    except Exception as errorinfo:
                        raise AssertionError(''''{var}' annotation predicate({annot}) raised exception\n  exception = '''.format(var = param,annot = annot)+str(errorinfo)+check_history)

                    h = ''''{var}' failed annotation check: value = {value}
  predicate = {annot}'''.format(var = param,value = "'"+value+"'" if type(value)==str else value,lenannot = len(annot.__code__.co_varnames),annot = annot)
                    
                    h += check_history
                    assert rt,h


                            
                            


            

                        
                    
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # Below, decode check function's annotation; check it against arguments
        pass 
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, storing the function header's parameters in order)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        try:
            if not Check_Annotation.checking_on == True and self.checking_on == True:
                print(param_arg_bindings()) 
                return self._f(*args,**kargs)
            self.binding = dict(param_arg_bindings())
            self.annots = self._f.__annotations__

            for key,value in self.binding.items():

                self.check(key,self.annots[key] if key in list(self.annots.keys()) else None,value)
                
            # Check the annotation for all parameters (if there are any)
                    
            # Compute/remember the value of the decorated function
            
            # If 'return' is in the annotation, check it
            
            # Return the decorated answer
            
            pass #remove after adding real code in try/except
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
##            print(80*'-')
##            for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
##                print(l.rstrip())
##            print(80*'-')
            raise



  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
##    def f(x:int): pass
##    f = Check_Annotation(f)
##    f(3)
##    f('a')
           
    #driver tests
    import driver
    driver.default_file_name = 'bscp4F18.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
