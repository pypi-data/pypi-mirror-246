class Calculator:
    """
    A simple calculator class that can perform basic arithmetic operations:
    Addition, Subtraction, Multiplication and Division.

    It can also calculate the n-th root of a number, and reset the current result.

    """
    def __init__(self, res=0):
        """
        Initializes the calculator with a starting result. Default is 0. 
        
        """
        self.__res = res 

    @property
    def res(self):
        return self.__res

    @staticmethod
    def verify_input(number):
        """
        Validates the input first and ensures it is a number. 
        Raises a ValueError if the input is invalid.

        """
        try:
            return float(number)
        except ValueError:
            raise ValueError("Error: The provided input is not a number.")

    def add(self, number):
        verified_number = Calculator.verify_input(number)
        self.__res += verified_number
        return(self.__res)

    def subtract(self, number):
        verified_number = Calculator.verify_input(number)
        self.__res -= verified_number
        return(self.__res)

    def multiply(self, number):
        verified_number = Calculator.verify_input(number)
        self.__res *= verified_number
        return(self.__res)
     
    def divide(self, number):
        verified_number = Calculator.verify_input(number)
        self.__res /= verified_number
        return(self.__res)

    def n_root(self, root):
        """
        Calculates the nth root of the current result.

        Checks for a special case where the root is even and the number
        is negative, raising a ValueError in this case.
        
        """
        verified_root = Calculator.verify_input(root)
        if self.__res < 0 and int(verified_root) % 2 == 0:
            raise ValueError("Error: Cannot take an even root of a negative number.")
        else:
            self.__res **= (1 / verified_root)
            return(self.__res)

    def reset(self):
        self.__res =0
        return(self.__res)
