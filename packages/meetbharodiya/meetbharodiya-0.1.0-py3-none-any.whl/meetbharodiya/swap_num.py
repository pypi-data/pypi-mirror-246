'''Write a program to take two integers  as input. Print those two integers as output and then call a function to swap those two integers.
	- Write function for each possible way to swap two integers 
'''

number1 = int(input("Enter the first number: "))
number2 = int(input("Enter the second number: "))

def swap_numbers_using_temp(num1, num2):
    """Swaps the values of two numbers using a temporary variable.

    Args:
        num1 (int): The first number.
        num2 (int): The second number.

    Returns:
        tuple: A tuple containing the swapped numbers.
    """
    temp = num1
    num1 = num2
    num2 = temp
    return num1, num2

def swap_numbers_using_addition(num1, num2):
    """Swaps the values of two numbers using addition.

    Args:
        num1 (int): The first number.
        num2 (int): The second number.

    Returns:
        tuple: A tuple containing the swapped numbers.
    """
    num1 = num1 + num2
    num2 = num1 - num2
    num1 = num1 - num2
    return num1, num2

def swap_numbers_using_swap_function(num1,num2):
    """Swaps the values of two numbers using swap function.

    Args:
        num1 (int): The first number.
        num2 (int): The second number.

    Returns:
        tuple: A tuple containing the swapped numbers.
    """
    num1,num2=num2,num1
    return num1,num2

final_num1,final_num2=swap_numbers_using_swap_function(number1,number2)
(number1,number2)
print(final_num1,final_num2)
