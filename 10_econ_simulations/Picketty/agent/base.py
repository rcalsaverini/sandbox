from dataclasses import dataclass
from typing import List, Optional
from ..company import Job
from .utility_optimization import optimal_consumption_given_labor_ratio, optimal_labor_ratio, discounted_expected_utility


HOURS_PER_DAY = 24.0

@dataclass
class Agent:
    wealth: float
    needs: float
    wealth_factor: float
    discount_rate: float
    skill: float

