# Given an array arr[] of n integers and a target value, the task is to find
# whether there is a pair of elements in the array whose sum is equal to target.


# Examples:

# Input: arr[] = [0, -1, 2, -3, 1], target = -2
# Output: true
# Explanation: There is a pair (1, -3) with the sum equal to given target, 1 + (-3) = -2.


# Input: arr[] = [1, -2, 1, 0, 5], target = 0
# Output: false
# Explanation: There is no pair with sum equals to given target.


def two_sum_brute_force(arr, target):
    return any(
        [
            arr[i] + arr[j] == target
            for i in range(len(arr))
            for j in range(i + 1, len(arr))
            if i != j
        ]
    )


def two_sum_pointers(arr, target):
    arr.sort()
    i = 0
    j = len(arr) - 1
    while i < j:
        if arr[i] + arr[j] == target:
            return True
        else:
            if arr[i] + arr[j] < target:
                i += 1
            else:
                j -= 1
    return False


def two_sum_hash(arr, target):
    seen = set()
    for num in arr:
        if (target - num) in seen:
            return True
        seen.add(num)
    return False


def two_sum_binary_search(arr, target):
    """
    This function is not correct.
    It reuses a number twice. It returns True in this case:
        arr = [0 , 1]
        target = 2
    It should return False.
    """

    def binary_search(arr, target):
        low = 0
        high = len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return None

    arr.sort()
    for i in range(len(arr)):
        j = binary_search(arr, target - arr[i])
        if j is not None and i != j:
            return True
    return False
