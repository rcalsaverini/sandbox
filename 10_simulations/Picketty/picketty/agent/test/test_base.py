from picketty.agent import Agent
from picketty.agent.laborer import Laborer
import numpy as np
import itertools as it

def random_laborer():
    return Laborer(
        wealth=np.random.lognormal(0, 1),
        needs=np.random.uniform(0, 1),
        wealth_factor=np.random.lognormal(0, 1),
        discount_rate=np.random.uniform(0, 1),
        skill=np.random.lognormal(0, 1),
    )


def test_agent():
    agent = Agent(0.0, 1.0)
    assert agent is not None
    
def test_laborer_base_salary():
    laborer = random_laborer()
    prices = np.linspace(0, 10, 11)
    limit = laborer.wealth_factor / laborer.moderation_factor
    for price in prices:
        base_salary = laborer._get_base_salary(price)
        assert base_salary >= 0.0
        assert base_salary <= limit


def test_laborer_optimal_labor_ratio():
    laborer = random_laborer()
    prices = np.linspace(0.1, 10, 11)
    salaries = np.linspace(0.1, 10, 11)
    for price, salary in it.product(prices, salaries):
        labor_ratio = laborer.get_optimal_labor_ratio(salary, price)
        assert labor_ratio >= 0.0
        assert labor_ratio <= 1.0
    assert False