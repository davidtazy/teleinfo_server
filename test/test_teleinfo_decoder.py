import os
import unittest

from teleinfo.linky import decode_line


class test_teleinfo(unittest.TestCase):
    def test_decode(self):
        datafile = os.path.join(os.path.dirname(__file__), "data", "complete.bin")

        with open(datafile, "rb") as fd:
            trame = {}
            for line in fd:
                decode_line(line, trame)


        self.assertEqual(trame["OPTARIF"], "BBR(")
        self.assertEqual(trame["ISOUSC"], 45)
        self.assertEqual(trame["BBRHCJW"], 0)
        self.assertEqual(trame["BBRHPJW"], 0)
        self.assertEqual(trame["BBRHCJR"], 0)
        self.assertEqual(trame["BBRHPJR"], 0)
        self.assertEqual(trame["PTEC"], "HPJB")
        self.assertEqual(trame["DEMAIN"], "----")
        self.assertEqual(trame["IINST"], 2)
        self.assertEqual(trame["IMAX"], 90)
        self.assertEqual(trame["PAPP"], 540)
        self.assertEqual(trame["HHPHC"], "A")
        self.assertEqual(trame["BBRHCJB"], 11512125)
        self.assertEqual(trame["BBRHPJB"], 17442550)
        self.assertTrue("timestamp" in trame)
