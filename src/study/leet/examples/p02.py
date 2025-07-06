# Given an array prices[] of length N, representing the prices of the stocks on
# different days, the task is to find the maximum profit possible by buying and
# selling the stocks on different days when at most one transaction is allowed.
# Here one transaction means 1 buy + 1 Sell.

# Note: Stock must be bought before being sold.

# Examples:

# Input: prices[] = {7, 10, 1, 3, 6, 9, 2} Output: 8 Explanation: Buy for price
# 1 and sell for price 9.


# Input: prices[] = {7, 6, 4, 3, 1} Output: 0 Explanation: Since the array is
# sorted in decreasing order, 0 profit can be made without making any
# transaction.

# Input: prices[] = {1, 3, 6, 9, 11} Output: 10 Explanation: Since the array is
# sorted in increasing order, we can make maximum profit by buying at price[0]
# and selling at price[n-1]


def solution_brute_force(prices):
    all_profits = [
        prices[j] - prices[i]
        for i in range(len(prices))
        for j in range(i + 1, len(prices))
    ]
    return max(all_profits) if all_profits else 0


def solution_single_pass(prices):
    min_so_far, *other_prices = prices
    max_profit = 0
    for price in other_prices:
        if price < min_so_far:
            min_so_far = price
        elif (price - min_so_far) > max_profit:
            max_profit = price - min_so_far
    return max_profit
