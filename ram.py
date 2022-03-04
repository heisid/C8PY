import sys

class RAM:
    def __init__(self):
        # The memory should be 4 kB (4 kilobytes, ie. 4096 bytes) large
        self.data = [0] * 4096

    def address_exception(func):
        # Exception handler for out of range memory
        # address must be the first argument
        def wrapper(*args, **kwargs):
            address = args[1]
            try:
                if 0x000 <= address <= 0xfff:
                    return func(*args, **kwargs)
                else:
                    raise IndexError()
            except IndexError:
                print(f'Invalid memory address: {hex(address)}', file=sys.stderr)
                sys.exit(1)
        return wrapper

    @address_exception
    def __getitem__(self, address):
        return self.data[address]

    @address_exception
    def __setitem__(self, address, value):
        # Limit only 8-bit per address slot
        self.data[address] = 0xff & value

    def bulk_write(self, start_addr, data):
        # Write many bytes at once in contiguous memory space
        for idx, data_byte in enumerate(data):
            self.__setitem__(start_addr + idx, data_byte)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        printed_str = ''
        for address, value in enumerate(self.data):
            printed_str += f'0x{address:03x}: 0x{value:02x}\n'
        return printed_str


# Testing purpose
if __name__ == '__main__':
    # Initialization test
    ram = RAM()
    print(len(ram))

    # Write test
    ram[0x100] = 0xfff # should return 0xff on read

    # Read test
    print(hex(ram[0x100]))
    #ram[0xfff + 1] # should raise exception
    #ram[0xfff + 1] = 100

    ram[0xfff] = 0x42
    print(ram)
