class Illustrate_Recursive:
    def __init__(self,f):
        self.f = f
        self.trace = False
        
    def illustrate(self,*args,**kargs):
        self.indent = 0
        self.trace = True
        answer = self.__call__(*args,**kargs)
        self.trace = False
        return answer
    
    def __call__(self,*args,**kargs):
        if self.trace:
            if self.indent == 0:
                print('Starting recursive illustration'+30*'-')
            print (self.indent*"."+"calling", self.f.__name__+str(args)+str(kargs))
            self.indent += 2
        answer = self.f(*args,**kargs)
        if self.trace:
            self.indent -= 2
            print (self.indent*"."+self.f.__name__+str(args)+str(kargs)+" returns", answer)
            if self.indent == 0:
                print('Ending recursive illustration'+30*'-')
        return answer



@Illustrate_Recursive
def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

print(factorial.illustrate(5))

##
##def deco(func):
##    def wrapper():
##        print("wrapperup")
##        func()
##        print("wrapperdown")
##    return wrapper
##
##@deco
##def printsth():
##    print("sbsbsb")
##
##printsth()
