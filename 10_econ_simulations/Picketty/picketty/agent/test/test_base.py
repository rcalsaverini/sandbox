from picketty.agent import Agent
from picketty.agent.laborer import Laborer
import numpy as np
import itertools as it

def test_agent():
    agent = Agent(0.0, 1.0, 1.0, 0.9, 0.0)
    assert agent is not None
    
def test_laborer_base_salary():
    laborer = Laborer(0.0, 1.0, 1.0, 0.9, 0.0)
    prices = np.linspace(0, 10, 11)
    limit = laborer.wealth_factor / laborer.moderation_factor
    for price in prices:
        base_salary = laborer.get_base_salary(price)
        assert base_salary >= 0.0
        assert base_salary <= limit