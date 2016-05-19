from Bio import SeqIO
import sys

for elem in SeqIO.parse(sys.argv[1],"fasta"):
    print(">"+elem.id+"\n"+str(elem.seq) + "\n")
    print(">"+elem.id+"\n"+str(elem.seq.reverse_complement()) + "\n")