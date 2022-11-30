from cmath import log, sqrt
import mpmath


def _step_wealth_utility(wealth_at: float, mu: float):
    return sqrt(wealth_at / mu)

def _step_labor_disutility(labor_ratio: float):
    return -log(1 - labor_ratio)

def _consumption_step_utility(consumption: float, xi: float):
    return sqrt(consumption / xi)

def discounted_expected_utility(labor_ratio: float, consumption: float, salary: float, price: float, discount_rate: float, mu: float, xi: float):
    """
    Expected lifetime utility of a laborer discounted for present value, starting from zero wealth.
    """
    accumulated_wealth_at = salary * labor_ratio - price * consumption
    effective_discount = mpmath.fp.polylog(-0.5, discount_rate)
    return (_consumption_step_utility(consumption, xi) - _step_labor_disutility(labor_ratio))/(1 - discount_rate) + _step_wealth_utility(accumulated_wealth_at, mu) * effective_discount


def optimal_consumption_given_labor_ratio(labor_ratio: float, salary: float, price: float, discount_rate: float, mu: float, xi: float):
    """
    Optimal consumption given a labor ratio, assuming the laborer starts with zero wealth.
    """
    max_consumption = (salary * labor_ratio) / price
    moderation_factor = ((1 - discount_rate) * mpmath.fp.polylog(-0.5, discount_rate)) ** 2
    minimal_consumption = price * xi
    return max_consumption  / (1 + minimal_consumption * moderation_factor / mu)

def optimal_labor_ratio(salary: float, price: float, discount_rate: float, mu: float, xi: float):
    """
    Optimal labor ratio given a salary, assuming the laborer starts with zero wealth and consumes the optimal amount.
    """
    moderation_factor = ((1 - discount_rate) * mpmath.fp.polylog(-0.5, discount_rate)) ** 2
    base_salary =  mu * price * xi / (mu + moderation_factor * price * xi)
    return 1 - 2 * (salary / base_salary) * (sqrt(1 + salary / base_salary) - 1)