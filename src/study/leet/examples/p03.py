# Given an array arr[] of n elements that contains elements from 0 to n-1, with
# any of these numbers appearing any number of times. The task is to find the
# repeating numbers.

# Note: The repeating element should be printed only once.

# Example:

# Input: n = 7, arr[] = [1, 2, 3, 6, 3, 6, 1] Output: 1, 3, 6 Explanation: The
# numbers 1 , 3 and 6 appears more than once in the array.


# Input : n = 5, arr[] = [1, 2, 3, 4 ,3] Output: 3 Explanation: The number 3
# appears more than once in the array.


def solution_brute_force(numbers: list[int]) -> set[int]:
    """
    Identifies duplicate numbers in a list.

    Args:
        numbers (list): A list of integers to check for duplicates.

    Returns:
        set: A set containing the duplicate numbers found in the input list.
    """
    seen = set()
    output = set()
    for i, number in enumerate(numbers):
        if (number in seen) and (number not in output):
            output.add(number)
        else:
            seen.add(number)
    return output
