# C8PY

*Note: Still in early progress*

This is a CHIP-8 emulator. According to [Wikipedia](https://en.wikipedia.org/wiki/CHIP-8): CHIP-8 is an interpreted programming language, developed by Joseph Weisbecker. It was initially used on the COSMAC VIP and Telmac 1800 8-bit microcomputers in the mid-1970s. CHIP-8 programs are run on a CHIP-8 virtual machine.

There are already many CHIP-8 emulators out there, but I make it anyway for learning purpose to know better about internal working of a computer (CPU opcodes, decoding, executing, etc).

Plan:

- I'm going to follow this guide: [https://tobiasvl.github.io/blog/write-a-chip-8-emulator/] and this CHIP-8 specification: [http://devernay.free.fr/hacks/chip8/C8TECH10.HTM]

- For user interface (settings, etc), display and sound, I'll be using pygame as a backend.

- For CHIP-8 program ROMs I will pick some from [https://johnearnest.github.io/chip8Archive/]

- In user interface, there will be ROM file loader (of course), keyboard mapping, and display color. And maybe emulator clock speed and live RAM viewer (looks cool) - visualized not text (would be unreadable)
