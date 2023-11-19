"""
FIZZBUZZ MODULE
"""


def is_divisible_by(num: int, divisor: int) -> bool:
    """
    Function to unnecessarily complicate the modulo operation.

    Args:
        num (nnt): Number to be tested
        divisor (nnt): Number to test divisibility against

    Returns:
        bool: Returns True if the num is a multiple of divisor
    """
    return num % divisor == 0


def fizzbuzz(n: int) -> str:
    """
    Performs a standard FizzBuzz check on a given number. If the
    number is divisible by 3, returns "Fizz". If the number is
    divisible by 5, returns "Buzz". If the number is divisible by
    both 3 and 5, returns "FizzBuzz". Otherwise, returns the string
    representation of the number.

    Parameters:
        n (nnt): The number to be checked

    Returns:
        str: The FizzBuzz result for the given number.
    """
    result = ""

    if is_divisible_by(n, 3):
        result += "Fizz"

    if is_divisible_by(n, 5):
        result += "Buzz"

    return result.strip() if result else str(n)


def generate_fizzbuzz_sequence(limit: int) -> list:
    """
    Creates a list for API output

    Args:
        limit (int): Count of how many numbers to run

    Returns:
        list: Resulting FizzBuzz outputs
    """
    return [fizzbuzz(i) for i in range(1, limit + 1)]
