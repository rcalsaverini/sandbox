from src.event import Event
from src.expr import Expr, Attr, Literal
from typing import List
from dataclasses import dataclass
from torch import Tensor, nn


@dataclass
class Row:
    input_events: List[Event]
    next_events: List[Event]
    scoring_timestamp: float


class Task:
    def prediction(self, embedding: Tensor) -> Tensor:
        pass

    def loss(self, prediction: Tensor, target: Tensor) -> Tensor:
        pass

    def create_target(self, row: Row) -> float:
        pass


@dataclass
class CountPredicatedNextEventsTask(Task):
    predicate: Expr[bool]

    def create_target(self, row: Row) -> float:
        predicated_events = [e for e in row.next_events if self.predicate(e)]
        return len(predicated_events)

    def loss(self, prediction: Tensor, target: Tensor) -> Tensor:
        """
        Poisson log-likelihood loss
        """

        return nn.functional.poisson_nll_loss(
            prediction, target, log_input=True, full=False, eps=1e-8
        )

    def prediction(self, embedding: Tensor) -> Tensor:
        layers = nn.Sequential(
            nn.Linear(embedding.shape[1], 1),
            nn.ReLU(),
        )
        return layers(embedding)


CCTransactionsOver1000Task = CountPredicatedNextEventsTask(
    (Attr("amount") > Literal(1000)) & (Attr("event_type") == Literal("cc_transaction"))
)


