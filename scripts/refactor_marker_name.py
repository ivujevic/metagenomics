import sys
import re
from Bio import SeqIO
import TaxTree
import Markers

tax_name = sys.argv[1]
tax_ti = sys.argv[2]
ref_name = sys.argv[3]

markers_info = sys.argv[4]
p_markers = sys.argv[5]


tax_tree = TaxTree.TaxTree(tax_ti,ref_name,tax_name)
print("Finished with tax tree")

markers = Markers.Markers(markers_info,tax_tree)


f_out = open("/home/ivujevic/Markeri/renamed_markersLen.fa","w")

for elem in SeqIO.parse(p_markers,"fasta"):
    name = elem.id
    sequence = str(elem.seq)
    ars = name.split('|')
    gi = ars[1]
    position = ars[4]

    cs = set(markers.get_species(gi,position))
    if len(cs) == 0:
        continue
    tis = ','.join([str(ti) for ti in cs])

    f_out.write(">gi|"+gi+"|ti|"+tis + "|" + str(len(sequence))+"\n"+sequence+"\n")

f_out.close()
