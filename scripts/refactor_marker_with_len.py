import sys
from Bio import SeqIO



f_out = open("/home/ivujevic/Markeri/renamed_markersLen.fa","w")

for elem in SeqIO.parse("/home/ivujevic/Markeri/renamed_markers1.fa","fasta"):
    name = elem.id
    sequence = str(elem.seq)
    ars = name.split('|')
    gi = ars[1]

    tis = ars[3]

    f_out.write(">gi|"+gi+"|ti|"+tis + "|" + str(len(sequence))+"\n"+sequence+"\n")

f_out.close()
