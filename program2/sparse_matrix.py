# Submitter: ziany(Yang, Zian)
import prompt
from collections import defaultdict
import inspect

class Sparse_Matrix:

    # I have written str(...) because it is used in the bsc.txt file and
    #   it is a bit subtle to get correct. This function does not depend
    #   on any other method in this class being written correctly, although
    #   it could be simplified by writing self[...] which calls __getitem__.   
    def __init__(self,*args):
        self.matrix = defaultdict(int)
        used_position = []

        for i in range(len(list(args))):
            
            if i <= 1:
                assert type(args[i]) == int and args[i] > 0,"row and column number should be positive integers"
            else:
                assert args[i][0]<args[0] and args[i][1]<args[1],"row or column number out of range"
                assert type(args[i][0]) == int and type(args[i][1]) == int,"row or column number should be integer"
                assert type(args[i][2]) == int or type(args[i][2]) == float,"the value in the matrix should be integer or float"
                if tuple(args[i][:2]) not in used_position:

                    if args[i][2] != 0:
                        self.matrix[args[i][:2]] = args[i][2]
                        used_position.append(args[i][:2])

                    
                else:
                    raise AssertionError("Sparse_Matrix.__init__:repeated index "+str(args[i][:2]))
                
        self.rows = args[0]
        self.cols = args[1]
        self.matrix = dict(self.matrix)
                
    def size(self):
        return (self.rows,self.cols)
        
    def __str__(self):
        size = str(self.rows)+'x'+str(self.cols)
        width = max(len(str(self.matrix.get((r,c),0))) for c in range(self.cols) for r in range(self.rows))
        return size+':['+('\n'+(2+len(size))*' ').join ('  '.join('{num: >{width}}'.format(num=self.matrix.get((r,c),0),width=width) for c in range(self.cols))\
                                                                                             for r in range(self.rows))+']'
    def __len__(self):
        return self.rows*self.cols

    def __bool__(self):
        if self.matrix == {}:
            return False
        return True

    def __repr__(self):
        prt_list = [str(self.rows),str(self.cols)]
        for key,value in self.matrix.items():
            prt_list.append(str(tuple(list(key)+[value])))
        return "Sparse_Matrix("+", ".join(prt_list)+")"

    def __getitem__(self,*position_tuple):

        if type(position_tuple[0][0]) == int and type(position_tuple[0][1]) == int and len(position_tuple[0])==2:
            if 0 <= position_tuple[0][0] < self.rows and 0 <= position_tuple[0][1] < self.cols:
                if position_tuple[0] in list(self.matrix.keys()):
                    return self.matrix[position_tuple[0]]
                else:
                    return 0
        raise TypeError("position tuple invalid")

    def __setitem__(self,position_tuple,value):
        if type(position_tuple[0]) == int and type(position_tuple[1]) == int and type(value) in [int,float] and len(position_tuple)==2:
            if 0 <= position_tuple[0] < self.rows and 0 <= position_tuple[1] < self.cols:
                if value != 0:
                    self.matrix[position_tuple] = value
                else:
                    if position_tuple in list(self.matrix.keys()):
                        del self.matrix[position_tuple]
                return None

        raise TypeError("position tuple invalid")

    def __delitem__(self,position_tuple):
        self.__setitem__(position_tuple,0)

    def row(self,row_num):
        try:
            row_num = int(row_num)
        except ValueError:
            raise AssertionError("row number invalid")
        
        assert 0 <= row_num < self.rows and type(row_num) == int,"row number invalid"
        rt_row_list = [0 for i in range(self.cols)]
        for position,value in self.matrix.items():
            if position[0] == row_num:
                rt_row_list[position[1]] = self.matrix[position]
        return tuple(rt_row_list)

    def col(self,col_num):
        try:
            col_num = int(col_num)
        except ValueError:
            raise AssertionError("row number invalid")
        
        assert 0 <= col_num < self.cols and type(col_num) == int,"row number invalid"
        rt_col_list = [0 for i in range(self.rows)]
        for position,value in self.matrix.items():
            if position[1] == col_num:
                rt_col_list[position[0]] = self.matrix[position]
        return tuple(rt_col_list)

    def details(self):
        return " -> ".join([str(self.rows)+"x"+str(self.cols),str(self.matrix),str(tuple([self.row(i) for i in range(self.rows)]))])

    def __call__(self,new_row,new_col):
        assert type(new_row) == int and type(new_col) == int and new_row >= 0 and new_col >= 0, "new number of row or column not valid"
        self.matrix = {k:self.matrix[k] for k in self.matrix if k[0]<=new_row-1 and k[1]<=new_col-1}
        self.rows,self.cols = new_row,new_col

    def __iter__(self):
        for i in sorted([(key[0],key[1],value) for key,value in self.matrix.items()],key = lambda x:x[2]):
            yield i

    def __pos__(self):
        return Sparse_Matrix(self.rows,self.cols,*[(key[0],key[1],value) for key,value in self.matrix.items()])

    def __neg__(self):
        return Sparse_Matrix(self.rows,self.cols,*[(key[0],key[1],-value) for key,value in self.matrix.items()])

    def __abs__(self):
        return Sparse_Matrix(self.rows,self.cols,*[(key[0],key[1],abs(value)) for key,value in self.matrix.items()])

    def __add__(self,right):
        if type(right) in [int,float]:
            return self+Sparse_Matrix(self.rows,self.cols,*[(i,j,right) for i in range(self.rows) for j in range(self.cols)])
        elif type(right) == Sparse_Matrix:
            assert right.rows == self.rows and right.cols == self.cols,"Incompatible matrix"
            rt_matrix = +self
            for key,value in right.matrix.items():
                rt_matrix[key] += value
            return rt_matrix
        else:
            raise TypeError("unsupported operand type(s) for +: Sparse_Matrix and "+str(type(right)))
        
    def __radd__(self,left):

        if type(left) in [int,float]:
            return self+Sparse_Matrix(self.rows,self.cols,*[(i,j,left) for i in range(self.rows) for j in range(self.cols)])
        elif type(left) == Sparse_Matrix:
            assert left.rows == self.rows and left.cols == self.cols,"Incompatible matrix"
            rt_matrix = +self
            for key,value in left.matrix.items():
                rt_matrix[key] += value
            return rt_matrix
        else:
            raise TypeError("unsupported operand type(s) for +: Sparse_Matrix and "+str(type(left)))
            
    def __sub__(self,right):
        if type(right) in [int,float]:
            return self+Sparse_Matrix(self.rows,self.cols,*[(i,j,-right) for i in range(self.rows) for j in range(self.cols)])
        elif type(right) == Sparse_Matrix:
            assert right.rows == self.rows and right.cols == self.cols,"Incompatible matrix"
            return self+(-right)
        else:
            raise TypeError("unsupported operand type(s) for -: Sparse_Matrix and "+str(type(right)))
        
    def __rsub__(self,left):
        if type(left) in [int,float]:
            return Sparse_Matrix(self.rows,self.cols,*[(i,j,left) for i in range(self.rows) for j in range(self.cols)])+(-self)
        elif type(left) == Sparse_Matrix:
            assert left.rows == self.rows and left.cols == self.cols,"Incompatible matrix"
            return left+(-self)
        else:
            raise TypeError("unsupported operand type(s) for -: Sparse_Matrix and "+str(type(left)))

    def __mul__(self,right):
        if type(right) in [int,float]:
            return Sparse_Matrix(self.rows,self.cols,*[(key[0],key[1],value*right) for key,value in self.matrix.items()])
        elif type(right) == Sparse_Matrix:
            assert right.rows == self.cols and right.cols == self.rows,"Incompatible matrix"
            rt_matrix = Sparse_Matrix(self.rows,right.cols)
            for i in range(self.rows):
                for j in range(right.cols):
                    rt_matrix[(i,j)] = sum([self.row(i)[n]*right.col(j)[n] for n in range(len(self.row(i)))])
            return rt_matrix
        else:
            raise TypeError("unsupported operand type(s) for *: Sparse_Matrix and "+str(type(right)))
        
    def __rmul__(self,left):
        return self*left
        
    def __pow__(self,right):
        if type(right) != int:
            raise TypeError("unsupported operand type for **"+str(type(right)))
        assert type(right) == int and right > 0,"unsupported operand type(s) for **: Sparse_Matrix and "+str(type(right))
        rt_matrix = +self
        for i in range(right-1):
            rt_matrix = rt_matrix*self
        return rt_matrix

    def __eq__(self,right):
        if type(right) in [int,float]:
            return self == Sparse_Matrix(self.rows,self.cols,*[(i,j,right) for i in range(self.rows) for j in range(self.cols)])
        elif type(right) == Sparse_Matrix:
            try:
                if all([self.matrix[(key[0],key[1])]==right.matrix[(key[0],key[1])] for key,value in self.matrix.items()]):
                    pass
                else:
                    return False
            except KeyError:
                return False
            try:
                if all([self.matrix[(key[0],key[1])]==right.matrix[(key[0],key[1])] for key,value in right.matrix.items()]):
                    return True
                else:
                    return False
            except KeyError:
                return False

        else:
            return False
# Code from Pattis q3helper-private
    @staticmethod
    def in_Sparse_Matrix(calling):
        if calling.function not in Sparse_Matrix.__dict__:
            return False
        return calling.frame.f_code is Sparse_Matrix.__dict__[calling.function].__code__
       
    def __setattr__(self,name,value):

        calling = inspect.stack()[1]
 
        if Sparse_Matrix.in_Sparse_Matrix(calling) and calling.function in ["__init__","__call__"] :
            self.__dict__[name] = value
        else:
            raise AssertionError("Cannot manipulate matrix")






if __name__ == '__main__':
    
    #Simple tests before running driver
    #Put your own test code here to test Sparse_Matrix before doing the bsc tests
    #Debugging problems with these tests is simpler

    print('Printing')
    m = Sparse_Matrix(3,3, (0,0,1),(1,1,3),(2,2,1))
    print(m)
    print(repr(m))
    print(m.details())
  
    print('\nlen and size')
    print(len(m), m.size(),)
    
    print('\ngetitem and setitem')
    print(m[1,1])
    m[1,1] = 0
    m[0,1] = 2
    print(m.details())

    print('\niterator')
    for r,c,v in m:
        print((r,c),v)
    
    print('\nm, m+m, m+1, m==m, m==1')
    print(m)
    print(m+m)
    print(m+1)
    print(m==m)
    print(m==1)
    print()
    
    import driver
    driver.default_file_name = 'bscp22F18.txt'
#     driver.default_show_exception = prompt.for_bool('Show exceptions when testing',True)
#     driver.default_show_exception_message = prompt.for_bool('Show exception messages when testing',True)
#     driver.default_show_traceback = prompt.for_bool('Show traceback when testing',True)
    driver.driver()
