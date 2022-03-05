#!/usr/bin/env python

import unittest
from ram import RAM

class TestRAM(unittest.TestCase):
    def test_ram_initialization(self):
        ram = RAM()
        self.assertEqual(len(ram), 4096, "Memory size must be 4096")
        self.assertEqual(ram.data, [0x0] * 4096, "All initialized zero")

    def test_ram_write_normal(self):
        ram = RAM()
        ram[0x100] = 0xff
        for addr, data_byte in enumerate(ram.data):
            if addr == 0x100:
                self.assertEqual(data_byte, 0xff, "Byte must be written in 0x100")
            else:
                self.assertEqual(data_byte, 0x00, "Data should not be written anywhere else")

    def test_ram_write_cropped(self):
        ram = RAM()
        ram[0x100] = 0xff + 2
        self.assertEqual(ram.data[0x100], 0x01, "Data must be cropped to 8-bit")

    def test_ram_write_out_of_range(self):
        ram = RAM()
        with self.assertRaises(SystemExit, msg="Writing out of range must exit"):
            ram[0xfff + 1] = 0x01
            self.assertRaises(IndexError, msg="Writing out of range must raise exception")

    def test_ram_read_normal(self):
        ram = RAM()
        ram.data[0xfff] = 0xff
        self.assertEqual(ram[0xfff], 0xff, "Should read data in 0xfff")

    def test_ram_read_out_of_range(self):
        ram = RAM()
        with self.assertRaises(SystemExit, msg="Reading out of range must exit"):
            data_at_0x1000 = ram[0xfff + 1]
            self.assertRaises(IndexError, msg="Reading out of range must raise exception")

    def test_ram_bulk_write(self):
        ram = RAM()
        ram.bulk_write(0x000, [0x01, 0x01])
        self.assertEqual(ram.data[0x000:0x003], [0x01, 0x01, 0x00], "Two bytes data must be written in 0x000 to 0x001 and nowhere else")


if __name__ == '__main__':
    unittest.main()