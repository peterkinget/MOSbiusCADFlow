import unittest
import os
from BitStream import BitStream


class TestBitStream(unittest.TestCase):
    def setUp(self):
        self.bs = BitStream()
        self.bs.netlistInput("test_schem_inv_nl.txt")
        bitstream = self.bs.generateBitstream()

    # # def test_manualInput(self):
    #     # Test manualInput method
    #     self.bs.manualInput()
    #     self.assertIsNotNone(self.bs.active_buslist)
    #     self.assertIsNotNone(self.bs.active_pinlists)

    def test_netlistInput(self):
        # Test netlistInput method
        correct_abuslist = [1, 2, 9, 10]
        correct_apinlists = [[13, 36], [12, 35], [18, 37], [1, 14]]
        self.assertEqual(self.bs.active_buslist, correct_abuslist)
        self.assertEqual(self.bs.active_pinlists, correct_apinlists)

    def test_generateBitstream(self):
        # Test generateBitstream method
        bitstream = self.bs.generateBitstream()
        # Assert that bitmatrix and bitstream attributes are set correctly
        self.assertEqual(len(self.bs.bitmatrix), 10) 
        self.assertEqual(len(self.bs.bitmatrix[0]), 65) 
        self.assertIsInstance(self.bs.bitmatrix[0][0], int)
        self.assertEqual(len(self.bs.bitstream), 650)
        self.assertIsInstance(self.bs.bitstream[0], int)

    def test_getPowerBuses(self):
        # Test getPowerBuses method
        correct_power_buses = [9, 10]
        power_buses = self.bs.getPowerBuses()
        self.assertEqual(power_buses, correct_power_buses)


    def test_compareStream(self):
        # Test compareStream method
        cstream = self.bs.bitstream
        self.assertTrue(self.bs.compareStream(cstream))

    def test_compareFile(self):
        # Test compareFile method
        cfpath = "output_bitstream_tst.txt"
        self.bs.writeBitFile(cfpath)
        self.assertTrue(self.bs.compareFile(cfpath))

    def test_writeBitFile(self):
        # Test writeBitFile method
        output_path = "test_output_bitstream.txt"
        self.bs.writeBitFile(output_path)
        self.assertTrue(os.path.exists(output_path))

    def test_writeHexFile(self):
        # Test writeHexFile method
        output_path = "test_output_hexstring.txt"
        self.bs.writeHexFile(output_path)
        self.assertTrue(os.path.exists(output_path))


if __name__ == "__main__":
    unittest.main()
