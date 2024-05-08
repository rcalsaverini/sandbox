from theory.notes import *
from theory.entities import *

def test_transpose():
    assert transpose(C, PERFECT(UNISON)) == C