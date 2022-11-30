from dataclasses import dataclass


HOURS_PER_DAY = 24.0

@dataclass
class Agent:
    wealth: float
    needs: float
