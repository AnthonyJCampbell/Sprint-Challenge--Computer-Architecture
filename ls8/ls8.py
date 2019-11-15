#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}: {sys.argv[1]} not found")
    else:
        file_name = sys.argv[1]
        program = []

        with open(file_name) as program_file:
            for line in program_file:
                line = line.split("#")[0]
                line = line.strip()

                if line == '':
                    continue
                
                val = int(line, 2)
                program.append(val)


        cpu = CPU()

        cpu.load(program)
        cpu.run()