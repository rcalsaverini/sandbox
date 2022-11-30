from .base import Agent
from .utility_optimization import optimal_consumption_given_labor_ratio, optimal_labor_ratio
from .job_selection import select_best_job
from ..company import Job
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Laborer(Agent):
    job: Optional[Job] = None
    
    def accept_job(self, job: Job):
        self.job = job
        
    def get_dismissed(self):
        self.job = None
    
    def receive_salary(self):
        self.wealth += self.job.salary
        
    def get_optimal_labor_ratio(self, price: float):
        return optimal_labor_ratio(self.job.salary, price, self.discount_rate, self.wealth_factor, self.needs)
    
    def get_optimal_consumption(self, price: float, labor_ratio: float):
        return optimal_consumption_given_labor_ratio(labor_ratio, self.job.salary, price, self.discount_rate, self.wealth_factor, self.needs)
            
    def choose_job(self, jobs: List[Job], price: float):
        return select_best_job(self, price, jobs)