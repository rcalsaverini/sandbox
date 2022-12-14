from .base import Agent
from ..company import Job
from dataclasses import dataclass
from typing import Optional, List
from functools import cached_property
from mpmath import fp
from cmath import sqrt, log

@dataclass
class Laborer(Agent):
    needs: float
    wealth_factor: float
    discount_rate: float
    skill: float
    job: Optional[Job] = None
    
    @cached_property
    def moderation_factor(self):
        return ((1 - self.discount_rate) * fp.polylog(-0.5, self.discount_rate)) ** 2
            
    def accept_job(self, job: Job):
        self.job = job
        
    def get_dismissed(self):
        self.job = None
    
    def receive_salary(self):
        self.wealth += self.job.salary
        
    def get_optimal_labor_ratio(self, salary: float, price: float):
        """
        Optimal labor ratio given a salary, assuming the laborer starts with zero wealth and consumes the optimal amount.
        """
        base_salary = self._get_base_salary(price)
        return 1 - 2 * (base_salary / salary) * (sqrt(1 + salary / base_salary) - 1)
    
    def get_optimal_consumption(self, price: float, salary: float, labor_ratio: float):
        """
        Optimal consumption given a labor ratio, assuming the laborer starts with zero wealth.
        """        
        max_consumption = salary * labor_ratio / price
        min_consumption = price * self.needs
        return max_consumption  / (1 + min_consumption * self.moderation_factor / self.wealth_factor)

    def discounted_expected_utility(self, labor_ratio: float, consumption: float, salary: float, price: float):
        """
        Expected lifetime utility of a laborer discounted for present value, starting from zero wealth.
        """
        accumulated_wealth_each_step = salary * labor_ratio - price * consumption
        undiscounted_wealth_utility = step_wealth_utility(accumulated_wealth_each_step, self.wealth_factor) * sqrt(self.moderation_factor)
        undiscounted_labour_utility = -step_labor_disutility(labor_ratio)
        undiscounted_consumption_utility = consumption_step_utility(consumption, self.needs)
        return (undiscounted_consumption_utility + undiscounted_labour_utility + undiscounted_wealth_utility) / (1 - self.discount_rate)

    def select_best_job_from_list(self, jobs: List[Job], price: float):
        applicable_jobs = filter(self._is_skill_enough, jobs)
        return max(applicable_jobs, key=lambda job: self._get_utility(job, price))

    def _get_base_salary(self, price: float):
        needs_cost = self.needs * price
        limit = self.wealth_factor / self.moderation_factor
        return limit * needs_cost / (limit + needs_cost)

    def _is_skill_enough(self, job: Job):
        return job.skill_requirement <= self.skill

    def _job_utility(self, job: Job, price: float):
        consumption = self.get_optimal_consumption(price, job.labor_ratio)
        return self.discounted_expected_utility(job.labor_ratio, consumption, job.salary, price)

    def _no_job_utility(self, price: float):
        consumption = self.get_optimal_consumption(price, 0.0)
        return self.discounted_expected_utility(0.0, consumption, 0.0, price)

    def _get_utility(self, job: Job, price: float):
        return self._job_utility(job, price) if job is not None else self._no_job_utility(price)



def step_wealth_utility(wealth_at: float, mu: float):
    return sqrt(wealth_at / mu)

def step_labor_disutility(labor_ratio: float):
    return -log(1 - labor_ratio)

def consumption_step_utility(consumption: float, xi: float):
    return sqrt(consumption / xi)
