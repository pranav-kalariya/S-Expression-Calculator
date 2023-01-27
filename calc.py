""" S-expression Calculator.
Supports operation on multiple operators in expression e.g. (add 2 3 4)
"""
import re
import sys
from functools import reduce
from typing import Union


class SExpression:
    """ SExpression parsing."""

    def __init__(self, usr_inp: str) -> None:
        self.user_inp = usr_inp
        self.output = ""
        self.expr_search_regex = r"\((add|multiply)(\s\d+)+\)|(^\d+$)"
        self.add_multiply_op_search_regex = r"\((add|multiply)(\s\d+)+\)"

    def add(self, exp: str) -> int:
        """ Evaluate ADD expression.
        :param self: Object of the SExpression
        :type self: Object
        :param exp: ADD Expression which will be calculated 
        :type exp: str 
        :return: Result of the ADD operation
        :rtype: int 
        """
        # Evaluation flow of exp: "(add 2 3)" -> "add 2 3" -> ["add" "2" "3"] -> [2 3] -> 5
        exp = exp[1:len(exp)-1]
        exp = re.split(r'\s', exp)
        return sum(list(map(int, exp[1:])))

    def multiply(self, exp: str) -> int:
        """ Evaluate MULTIPLY expression.
        :param self: Object of the SExpression
        :type self: Object
        :param exp: MULTIPLY Expression which will be calculated 
        :type exp: str 
        :return: Result of the MULTIPLY operation
        :rtype: int 
        """
        # Evaluation flow of exp: "(multiply 2 3)" -> "multiply 2 3" -> ["multiply" "2" "3"] -> [2 3] -> 6
        exp = exp[1:len(exp)-1]
        exp = re.split(r'\s', exp)
        return reduce((lambda x, y: x * y), (list(map(int, exp[1:]))))

    def replace(self, value: Union[str, int]) -> None:
        """ Replace the inner most Expression with the calculated result.
        For example: (multiply 5 (add 2 3)) will be converted to (multiply 5 5).
        :param self: Object of the SExpression
        :type self: Object
        :param value: calculated value of inner most expression
        :type exp: int, str
        :return: This method will update the user_inp variable of object 
        :rtype: None
        """

        self.user_inp = re.sub(
           self.expr_search_regex, str(value), self.user_inp, count=1)

    def get_expr(self) -> str:
        """ Get the inner most expression from user_inp.
        :param self: Object of the SExpression
        :type self: Object
        :return: Inner most expression of user_inp
        :rtype: str| None
        """
        match = re.search(self.expr_search_regex, self.user_inp)
        # if the regex does not match means S-expression is not in correct format.
        if not match:
            return ""
        return match.group()

    def get_type(self, exp: str) -> str:
        """ Get the type of given expression.
        :param self: Object of the SExpression
        :type self: Object
        :param value: calculated value of inner most expression
        :type exp: int, str
        :return: Type of expression from (add, multiply, digit, invalid)
        :rtype: str
        """
        # Get the type of given expression. If type does not match with supported types return "invalid"s
        if re.search(self.add_multiply_op_search_regex, exp):
            if "multiply" in exp:
                return "multiply"
            return "add"
        elif re.search(r"^\(\d+\)$|^\d+$", exp):
            return "digit"
        else:
            return "invalid"


def main(inp: str) -> None:
    """Driver function.

    Algorithm: 
        1> find inner most expression
        2> check the type of that expression
        3> if the expression type matches is in the supported types
            3.1> evaluate the expression and replace inner morst expression in the original expression with evaluated value.
            3.2> continue evaluating and replacing inner expressions till type is "digit" or "invalid"
            3.3> if type digit found, print it. if invalid found, print Invalid S-expression message
        4> if the expression type does not match with suppported type return Invalid syntax error 


    Example Positive Flow:
        1> (add 2 (multiply 2 3))
        2> (add 2 6)
        3> 8 


    Example Negative Flow:
        1> (add 2 (multiply 2 3)
        2> (add 2 6
        3> Invalid S-Expression 
    """
    obj = SExpression(inp.strip())  # creating object of SExpession

    while True:
        expression = obj.get_expr()  # getting the inner most expression
        if not expression:  # if expression is not of valid format return error.
            print("Invalid Expression. Please try again!")
            break
        # get the type of inner most expression
        type_exp = obj.get_type(expression)
        if type_exp == "digit":
            obj.replace(obj.user_inp)
            print(obj.user_inp)  # if a type is digit then simply print
            break

        # if a type is add expression then evaluate the expression and replace the result of it.
        elif type_exp == "add":
            value = obj.add(expression)
            obj.replace(value)

        # if a type is multiply expression then evaluate the expression and replace the result of it.
        elif type_exp == "multiply":
            value = obj.multiply(expression)
            obj.replace(value)

        # if a type does not match the S-expression syntax simple return error message.
        else:
            print("Invalid Expression. Please try again!")
            break


if __name__ == "__main__":
    try:
        # if more then one arguments given, let user know that first argument is considered.
        if len(sys.argv) != 2:
            print(
                "First argument {} is considered as S-expression! Other arguments will be ignored!".format(sys.argv[1]))
        inp = sys.argv[1]
        main(inp)
    except IndexError as err:  # if no arguments given ask user to try again with 1 argument
        print("Please provide 1 argument which contains S-expression to calculate!")
