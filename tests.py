#!/usr/bin/env python

""" Unit test for CPU and memory of CHIP-8 emulator """

__author__ = "Rosyid Haryadi"
__license__ = "GPLv3"

import unittest
from unittest.mock import Mock

from cpu import CPU
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
        self.assertEqual(ram.data[0x000:0x003], [0x01, 0x01, 0x00],
                         "Two bytes data must be written in 0x000 to 0x001 and nowhere else")


class TestCPU(unittest.TestCase):
    def test_cpu_init(self):
        cpu = CPU()
        self.assertEqual(cpu.pc, 0x200, "Program counter must initialized 0x200")
        self.assertEqual(cpu.i, 0x0, "Index register is set to 0x0")
        self.assertEqual(len(cpu.stack), 0, "Stack memory must be empty")
        self.assertEqual((cpu.delay_timer, cpu.sound_timer), (0, 0), "Timers are set to 0")

    def test_cpu_load_font(self):
        ram = RAM()
        cpu = CPU(ram=ram)
        FONT = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
        ]
        cpu.load_font()
        self.assertEqual(ram.data[0x050:0x050 + len(FONT)], FONT, "Font must be loaded to RAM")

    def test_cpu_fetch(self):
        ram = RAM()
        cpu = CPU(ram=ram)
        ram.bulk_write(0x200, [0x61, 0xff])
        opcode = cpu.fetch()
        self.assertEqual(opcode, 0x61ff, "CPU must fetch opcode 0x61ff from memory address 0x200")
        self.assertEqual(cpu.pc, 0x200 + 2, "CPU PC register must increase by 2")

    def test_cpu_op_0x00e0(self):
        screen = Mock()
        cpu = CPU(screen=screen)
        exe_status = cpu.op_0(0x0e0)
        self.assertTrue(exe_status, "0x00e0 must execute successfully")
        screen.clear.assert_called_once()

    def test_cpu_op_0x00ee(self):
        cpu = CPU()
        cpu.stack = [addr for addr in range(0x200, 0x200 + 5)]
        stack_top = cpu.stack[-1]
        orig_stack_size = len(cpu.stack)
        exe_status = cpu.op_0(0x0ee)
        self.assertTrue(exe_status, "0x00ee must execute successfully")
        self.assertEqual(cpu.pc, stack_top, f"{stack_top} must be popped from stack to pc")
        self.assertEqual(len(cpu.stack), orig_stack_size - 1, "Stack size must shrink")


if __name__ == '__main__':
    unittest.main()
