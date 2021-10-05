import pytest
from koloda import Koloda

class Test_Koloda:
    def setup(self):
        self.k = Koloda()

    def teardown(self):
        pass

    def test_get_count(self):
        assert self.k.get_count() == 36
