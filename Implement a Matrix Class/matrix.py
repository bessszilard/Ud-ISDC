import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def dot_product(vector1, vector2):
    if len(vector1) != len(vector2):
        print("__dot_product - vector1 and vector2 length is not equal")
        return None
    dot_prod = 0
    for i in range(len(vector1)):
        dot_prod += vector1[i] * vector2[i]

    return dot_prod

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        #1x1 matrix
        if self.w == 1:
            return self[0][0]
    
        #determinant of a 2x2 matrix
        return self[0][0] * self[1][1] - self[0][1] * self[1][0] 
                
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        trace = 0
        for i in range(self.h):
            trace += self[i][i]
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        
        if self.determinant() == 0:
            raise(ValueError, "Matrix determinant is zero. Inverse is not calculabe")
        
        matrixInverse = zeroes(self.h, self.w)
        #matrix is 1x1
        if self.h == 1:
            matrixInverse[0][0] = 1 / self[0][0]
            return matrixInverse
        
        #matrix is 2x2
        matrixInverse = 1 / self.determinant() * self.adj()
        
        return matrixInverse

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        #per-allocate memory for the matrix
        transp_array = zeroes( self.w, self.h )  # w and h swaped
        for i in range(self.h):
            for j in range(self.w):
                transp_array[j][i] = self[i][j]
        return transp_array

    def is_square(self):
        return self.h == self.w
    
    def adj(self):
        #it is a vector
        if self.w == 1:
            return None

        #it is not a 2x matrix
        elif self.h != 2 or self.h != 2:
            return None
        
        adjMatrix = zeroes( self.h, self.w )
        adjMatrix[0][0] =  self[1][1]
        adjMatrix[0][1] = -self[0][1]
        adjMatrix[1][0] = -self[1][0]
        adjMatrix[1][1] =  self[0][0]
        
        return adjMatrix
    
    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        #per-allocate memory for the matrix
        sum_array = zeroes( self.h, self.w )
        for i in range(self.h):
            for j in range(self.w):
                sum_array[i][j] = self[i][j] + other[i][j]
                
        return sum_array
    
    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        #per-allocate memory for the matrix
        neg_array = zeroes( self.h, self.w )
        for i in range(self.h):
            for j in range(self.w):
                neg_array[i][j] = -self[i][j]

        return neg_array

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        #per-allocate memory for the matrix
        sum_array = zeroes( self.h, self.w )
        for i in range(self.h):
            for j in range(self.w):
                sum_array[i][j] = self[i][j] - other[i][j]
                
        return sum_array

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        mult_array = zeroes( self.h, other.w )
        for r in range(self.h):
            for c in range(other.w):
                mult_array[r][c] = dot_product( self[r], other.T()[c] )
        return mult_array

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            rmul_array = zeroes( self.h, self.w )
            for i in range(self.h):
                for j in range(self.w):
                    rmul_array[i][j] = self[i][j] * other
            return rmul_array
