from cmath import sqrt
from dataclasses import dataclass
import datetime
from typing import Dict, List
import numpy as np
from scipy import optimize as opt  # type: ignore
from nptyping import NDArray
from matplotlib import pyplot as plt
import seaborn as sns # type: ignore
import pandas as pd


@dataclass
class Agent:
    economy: "Economy"
    wealth: float
    needs: float
    
    @staticmethod
    def random_agent(economy: "Economy"):
        return Agent(
            economy=economy,
            wealth=0.0,
            needs=np.random.uniform(0, 0.1)
        )
        
    
    def _wealth_update(self: "Agent", labor: float, consumption: float):
        wealth_return = self.wealth * self.economy.return_of_capital
        labor_payment = labor * self.economy.salary
        consumed_wealth = consumption * self.economy.price
        return self.wealth + wealth_return + labor_payment - consumed_wealth
    
    def get_wealth_utilitiy(self: "Agent", labor: float, consumption: float):
        next_wealth = self._wealth_update(labor, consumption)
        return max(next_wealth, 0)
    
    def get_consumption_utility(self, consumption):
        if consumption < self.needs:
            return 0.0
        else:
            return max(((consumption - self.needs)/self.needs), 0)
    
    def get_labor_disutility(self, labor):
        return 1/(1 - sqrt(labor)) # self.labor_base - np.log(1 - labor ** self.labor_exponent)
    
    def utility(self: "Agent", labor: float, consumption: float):
        if consumption < self.needs:
            return 0.0
        consumption_utility = self.get_consumption_utility(consumption)
        labor_disutility = self.get_labor_disutility(labor)
        wealth_utility = self.get_wealth_utilitiy(labor, consumption)
        return  wealth_utility * consumption_utility / labor_disutility
    
    def get_utility_map(self: "Agent", labors: NDArray, consumptions: NDArray) -> pd.DataFrame:
        pairs = np.array(np.meshgrid(labors, consumptions)).T.reshape(-1, 2)
        utilities = np.array([self.utility(*pair) for pair in pairs])
        return pd\
            .DataFrame({"labor": pairs[:, 0], "consumption": pairs[:, 1], "utility": utilities})\
    
    def get_outputs(self: "Agent") -> Dict[str, float]:
        labor_space = np.linspace(0.0, 1, 101)
        consumption_space = np.linspace(0.0, 10, 101)
        utilities = self.get_utility_map(labor_space, consumption_space).set_index(["labor", "consumption"])
        (labor, consumption) = utilities.utility.idxmax() # type: ignore
        return {"labor": labor, "consumption": consumption, "utility": utilities.utility.max()} # type: ignore

    def get_outputs_opt(self: "Agent", max_fun: int = 40) -> Dict[str, float]:
        def disutility(x):
            labor, consumption = x
            return -self.utility(labor, consumption)
        optimum = opt.minimize(disutility, [0.5, 0.5], bounds=[(0, 0.999), (0, None)], options={"maxiter": max_fun, "disp": False})
        labor, consumption = optimum.x
        return {
            "labor": labor,
            "consumption": consumption,
            "utility": -optimum.fun,
            "message": optimum.message,
            "success": optimum.success,
        }
        

@dataclass
class Economy:
    agents: List[Agent]
    return_of_capital: float
    price: float
    salary: float
    
    @staticmethod
    def create(return_of_capital: float, price: float, salary: float, n_agents: int) -> "Economy":
        new_economy = Economy(agents=[], return_of_capital=return_of_capital, price=price, salary=salary)
        new_economy.agents = [new_economy.random_agent() for _ in range(n_agents)]
        return new_economy

    def random_agent(self: "Economy"):
        return Agent.random_agent(self)
    
    def simulate(self: "Economy", n_periods: int, reporter: "Reporter"):
        reporter.initialize(n_periods, n_agents=len(self.agents))
        for period in range(n_periods):
            results = self.step()
            reporter.report(period, results)
            
    def step(self: "Economy") -> List[Dict[str, float]]:
        results = []
        for agent in self.agents:
            outputs = agent.get_outputs_opt()
            agent.wealth = agent._wealth_update(outputs["labor"], outputs["consumption"])
            outputs["wealth"] = agent.wealth
            outputs["needs"] = agent.needs
            results.append(outputs)
        return results


class Reporter:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
    def initialize(self, n_periods: int, n_agents: int):
        self.data = pd.DataFrame(
            columns=["labor", "consumption", "utility", "wealth", "needs", "success"],
            index=pd.MultiIndex.from_product([range(n_periods), range(n_agents)], names=["period", "agent"]),
        )
        
    def report(self, time: int, results: List[Dict[str, float]]):
        for agent, result in enumerate(results):
            for column in self.data.columns:
                self.data.loc[(time, agent), column] = float(result[column]) # type: ignore
            
        if self.verbose:
            output = ""
            output += f"Period: {time}"
            for column in self.data.columns:
                output += f"\t{column}: {self.data.loc[time].mean()[column]:.2f}" # type: ignore
            print(output)
                
    def get_data(self):
        return pd.DataFrame(self.data).reset_index().astype(float)
        
    def _plot_column(self, data, column, ax, yscale="linear"):
        ax.set_title(column)
        ax.set_xlabel("Time")
        ax.set_ylabel(column)
        ax.set_yscale(yscale)
        average = data.groupby("period")[column].mean()
        q1 = data.groupby("period")[column].quantile(0.25)
        q2 = data.groupby("period")[column].quantile(0.75)
        min_ = data.groupby("period")[column].min()
        max_ = data.groupby("period")[column].max()
        average.plot(ax=ax)
        ax.fill_between(q1.index, q1, q2, alpha=0.2)
        ax.fill_between(min_.index, min_, max_, alpha=0.1)
        
    def _plot_column_by_column(self, data, column_to_plot, column_to_group, ax, yscale="linear"):
        ax.set_title(column_to_plot)
        ax.set_xlabel("Time")
        ax.set_ylabel(column_to_plot)
        ax.set_yscale(yscale)
        qcuts = pd.qcut(data[column_to_group], 11, duplicates="drop")
        print(qcuts.unique())
        for group in sorted(qcuts.unique()):
            data.loc[qcuts == group].groupby("period")[column_to_plot].mean().plot(ax=ax, label=group)
        ax.legend()
        
    def plot_utility(self, data, ax):
        self._plot_column(data, "utility", ax)
        
    def plot_wealth(self, data, ax):
        self._plot_column(data, "wealth", ax)
        
    def plot_labor(self, data, ax):
        self._plot_column(data, "labor", ax)
        
    def plot_consumption(self, data, ax):
        self._plot_column(data, "consumption", ax)
    
    
    def plot(self):
        data = self.get_data()
        fig = plt.figure(figsize=(30, 30))
        # self.plot_wealth(data, fig.add_subplot(3, 3, 1))
        # self.plot_labor(data, fig.add_subplot(3, 3, 2))
        # self.plot_consumption(data, fig.add_subplot(3, 3, 3))
        # self.plot_utility(data, fig.add_subplot(3, 3, 4))
        for k, column in enumerate(["wealth", "labor", "consumption", "utility"]):
            self._plot_column_by_column(data, column, "needs", fig.add_subplot(2, 2, k + 1))


if __name__ == "__main__":
    economy = Economy.create(return_of_capital=0.05, price=1.0, n_agents=10, salary=10.0)
    reporter = Reporter(verbose=True)
    economy.simulate(n_periods=100, reporter=reporter)
    reporter.plot()
    plt.show()