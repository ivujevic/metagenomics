import sys

species_ti = sys.argv[1]
assembly_file = open(sys.argv[2], "r")

for line in assembly_file:
    line = line.strip()
    if line[0] == '#':
        continue
    ls = line.split("\t")

    if ls[6] == species_ti:
        print(ls[-2])