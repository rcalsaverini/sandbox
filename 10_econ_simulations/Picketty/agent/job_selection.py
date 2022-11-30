from typing import List, Optional
from .utility_optimization import discounted_expected_utility
from .base import Agent
from ..company import Job

def _is_skill_enough(laborer: Agent, job: Job):
    return job.skill_requirement <= laborer.skill

def _job_utility(laborer: Agent, job: Job, price: float):
    consumption = laborer.get_optimal_consumption(price, job.labor_ratio)
    return discounted_expected_utility(job.labor_ratio, consumption, job.salary, price, laborer.discount_rate, laborer.wealth_factor, laborer.needs)

def _no_job_utility(laborer: Agent, price: float):
    consumption = laborer.get_optimal_consumption(price, 0.0)
    return discounted_expected_utility(0.0, consumption, 0.0, price, laborer.discount_rate, laborer.wealth_factor, laborer.needs)

def _get_utility(laborer: Agent, job: Job, price: float):
    return _job_utility(laborer, job, price) if job is not None else _no_job_utility(laborer, price)

def select_best_job(laborer: Agent, price: float, jobs: List[Job]):
    applicable_jobs = filter(lambda job: _is_skill_enough(laborer, job), [laborer.job] + jobs)
    return max(applicable_jobs, key=lambda job: _get_utility(laborer, job, price))
