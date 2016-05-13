import sys
import re
from Bio import SeqIO
import TaxTree
import Markers

tax_name = sys.argv[1]
tax_ti = sys.argv[2]
ref_name = sys.argv[3]

markers_info = sys.argv[4]
markers = sys.argv[5]


tax_tree = TaxTree.TaxTree(tax_ti,ref_name,tax_name)
print("Finished with tax tree")

markers = Markers.Markers(markers_info,tax_tree)
