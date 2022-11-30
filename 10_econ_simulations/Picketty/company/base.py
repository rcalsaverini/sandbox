from dataclasses import dataclass
from typing import List
from agent import Agent

@dataclass
class Job:
    salary: float
    labor_ratio: float
    
    
@dataclass
class Company:
    ceo: Agent
    workers: List[Agent]
