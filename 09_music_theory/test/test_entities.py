from pytest import raises
from theory.entities import *

def test_Note__str__():
    for note, name in zip(notes, "C C♯ D D♯ E F F♯ G G♯ A A♯ B".split()):
        assert str(note) == name

def test_Note__repr__():
    for note, name in zip(notes, "C C♯ D D♯ E F F♯ G G♯ A A♯ B".split()):
        assert repr(note) == name
        
def test_IntervalDegree_perfectable():
    assert IntervalDegree.perfectable() == {UNISON, FOURTH, FIFTH, OCTAVE}

def test_IntervalDegree_is_perfectable():
    assert UNISON.is_perfectable()
    assert not SECOND.is_perfectable()
    assert not THIRD.is_perfectable()
    assert FOURTH.is_perfectable()
    assert FIFTH.is_perfectable()
    assert not SIXTH.is_perfectable()
    assert not SEVENTH.is_perfectable()
    assert OCTAVE.is_perfectable()
    
def test_IntervalQuality__is_valid():
    for degree in IntervalDegree:
        assert DIMINISHED._is_valid(degree)
        assert AUGMENTED._is_valid(degree)
    for degree in {UNISON, FOURTH, FIFTH, OCTAVE}:
        assert PERFECT._is_valid(degree)
    for degree in {SECOND, THIRD, SIXTH, SEVENTH}:
        assert MINOR._is_valid(degree)
        assert MAJOR._is_valid(degree)    

def test_IntervalQuality___call__():
    for degree in {UNISON, FOURTH, FIFTH, OCTAVE}:
        assert PERFECT(degree) == Interval(degree, PERFECT)
        assert DIMINISHED(degree) == Interval(degree, DIMINISHED)
        assert AUGMENTED(degree) == Interval(degree, AUGMENTED)
        raises(ValueError, MINOR, degree)
        raises(ValueError, MAJOR, degree)
    for degree in {SECOND, THIRD, SIXTH, SEVENTH}:
        assert MINOR(degree) == Interval(degree, MINOR)
        assert MAJOR(degree) == Interval(degree, MAJOR)
        assert DIMINISHED(degree) == Interval(degree, DIMINISHED)
        assert AUGMENTED(degree) == Interval(degree, AUGMENTED)
        raises(ValueError, PERFECT, degree)
    
    
def test_Interval_to_semitones():
    assert PERFECT(UNISON).to_semitones() == 0
    assert PERFECT(FOURTH).to_semitones() == 5
    assert PERFECT(FIFTH).to_semitones() == 7
    assert PERFECT(OCTAVE).to_semitones() == 12
    
    assert MINOR(SECOND).to_semitones() == 1
    assert MAJOR(SECOND).to_semitones() == 2   
    assert MINOR(THIRD).to_semitones() == 3
    assert MAJOR(THIRD).to_semitones() == 4
    assert MINOR(SIXTH).to_semitones() == 8
    assert MAJOR(SIXTH).to_semitones() == 9
    assert MINOR(SEVENTH).to_semitones() == 10
    assert MAJOR(SEVENTH).to_semitones() == 11

    assert DIMINISHED(UNISON).to_semitones() == -1
    assert DIMINISHED(SECOND).to_semitones() == 0
    assert DIMINISHED(THIRD).to_semitones() == 2
    assert DIMINISHED(FOURTH).to_semitones() == 4
    assert DIMINISHED(FIFTH).to_semitones() == 6
    assert DIMINISHED(SIXTH).to_semitones() == 7
    assert DIMINISHED(SEVENTH).to_semitones() == 9
    assert DIMINISHED(OCTAVE).to_semitones() == 11
    
    assert AUGMENTED(UNISON).to_semitones() == 1
    assert AUGMENTED(SECOND).to_semitones() == 3
    assert AUGMENTED(THIRD).to_semitones() == 5
    assert AUGMENTED(FOURTH).to_semitones() == 6
    assert AUGMENTED(FIFTH).to_semitones() == 8
    assert AUGMENTED(SIXTH).to_semitones() == 10
    assert AUGMENTED(SEVENTH).to_semitones() == 12
    assert AUGMENTED(OCTAVE).to_semitones() == 13

    