from dataclasses import dataclass
from typing import Callable
from nptyping import DataFrame, Double, Structure

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Position = Double  
Time = Double
Velocity = Double
Force = Double
State = Structure["t: Float, x: Float, v: Float"]
History = DataFrame[State]

def make_row(t: Time, x: Position, v: Velocity):
    return pd.Series({"t": t, "x": x, "v": v}).astype("double")

def initial_state() -> History:
    return pd.DataFrame([[0.0, 0.0, 0.0]], columns=["t", "x", "v"])

@dataclass
class Model:
    """Define a model according to the SDE:
    
        dX = V dt
        dV = f(X, t) dt + sigma dW

        Args:
            - f: Callable[[Position, Time], Force] - the force function
            - sigma: float - the volatility strength
    """
    sigma: float
    force: Callable[[Time, Position], Force]

    def V(self, s: History, dt: Time) -> Velocity:
        """Return the drift term."""
        current_state = s.iloc[-1]
        return make_row(1.0, current_state.v, self.force(current_state.t, current_state.x))

    def dW(self, s: History, dt: Time) -> Velocity:
        """Return the diffusion term."""
        return make_row(0.0, 0.0, self.sigma * np.random.normal(loc=0.0, scale=np.sqrt(dt)))

    def step(self, s: History, dt: Time) -> History:
        """Return the next step of the simulation."""
        dU = self.V(s, dt)*dt
        dW = self.dW(s, dt)
        new_state = pd.DataFrame([s.iloc[-1] + dU + dW], index=[len(s)])
        return pd.concat([s, new_state])
    
    def simulate_until_time(self, t: Time, dt: Time) -> History:
        """Simulate the model until time t."""
        s = initial_state()
        while s.t.iloc[-1] < t:
            s = self.step(s, dt)
        return s
    
    def simulate_until_distance(self, target_distance: Position, dt: Time, max_time: Time) -> History:
        """Simulate the model until distance `target_distance`."""
        s = initial_state()
        while np.abs(s.x.iloc[-1]) < target_distance:
            s = self.step(s, dt)
            if s.t.iloc[-1] > max_time:
                break
        return s
