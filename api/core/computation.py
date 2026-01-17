from typing import List

from api.core.constants import SequenceWords


def _find_fizzbuzz_up_to(n: int) -> str:
    """Performs a standard FizzBuzz check on a given number.

    If the number is divisible by 3, returns "Fizz". If the number
    is divisible by 5, returns "Buzz". If the number is divisible by
    both 3 and 5, returns "FizzBuzz". Otherwise, returns the string
    representation of the number.

    Parameters:
        n (int): The number to be checked

    Returns:
        str: The FizzBuzz result for the given number.
    """
    result = ""

    if n % 3 == 0:
        result += SequenceWords.Fizz

    if n % 5 == 0:
        result += SequenceWords.Buzz

    return result.strip() if result else str(n)


def generate_fizzbuzz_sequence(limit: int) -> List[str]:
    """Creates a list for API output.

    Args:
        limit (int): Count of how many numbers to run

    Returns:
        list: Resulting FizzBuzz outputs
    """
    return [_find_fizzbuzz_up_to(i) for i in range(1, limit + 1)]
