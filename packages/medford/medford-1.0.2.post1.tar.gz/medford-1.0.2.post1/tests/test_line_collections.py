import pytest

from MEDFORD.objs.linecollections import *
from MEDFORD.objs.linereader import LineReader as lr
from MEDFORD.objs.linecollector import LineCollector

class TestAtAtCollections() :
    def test_AtAt_validation_err(self) :
        ex_line = lr.process_line("@Major-@MajorTwo Name", 0)
        assert ex_line is not None

        lc : LineCollector = LineCollector([ex_line])
        #line: AtAt = lc.