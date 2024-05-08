from enum import Enum
from dataclasses import dataclass
from typing import Dict


class EventType(Enum):
    CC_TRANSACTION = "cc_transaction"
    DEBIT_TRANSACTION = "debit_transaction"
    PIX_TRANSACTION = "pix_transaction"
    SCREEN_LOADED = "screen_loaded"
    BUTTON_CLICKED = "button_clicked"
    FORM_SUBMITTED = "form_submitted"
    LOAN_REQUESTED = "loan_requested"
    LOAN_APPROVED = "loan_approved"
    LIMIT_INCREASED = "limit_increased"
    CC_BILL_PAID = "cc_bill_paid"
    CC_BILL_LATE = "cc_bill_late"


@dataclass
class Event:
    event_type: EventType
    timestamp: float
    attributes: Dict[str, str]
