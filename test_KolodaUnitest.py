import unittest
from koloda import Koloda

class testKoloda( unittest.TestCase ):
    def setUp(self) -> None:
        self.k = Koloda()

    def tearDown(self) -> None:
        pass

    def test_get_count(self):
        self.assertEqual( self.k.get_count(), 36 )