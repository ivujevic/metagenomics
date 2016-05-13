import sys
import re
from Bio import SeqIO

p_markers_info = sys.argv[1];
p_markers = sys.argv[2]
p_tax = sys.argv[3]


f_markers_info = open(p_markers_info,"r")
f_tax = open(p_tax,"r")
ds = {}

ti_cs = {}

ti_rank = {}

ti_parent = {}

letterToTaxName = {
        's': "species",
        'g': "genus",
        'f': "family",
        'o': "order",
        'c': "class",
        'p': "phylum",
        't': "species",
        }


def getCladeTi(clade_name, curr_ti):
    parent_ti = curr_ti
    while True:
        parent_ti = ti_parent[parent_ti]
        parent_clade_name = ti_rank[parent_ti]
        if parent_clade_name == clade_name:
            return parent_ti

def getCladesChildren(clade_ti):
    ls = []
    for c in ti_cs[clade_ti]:
        if ti_rank[c] == "species":
            ls+= [c]
        else:
            ls+=getCladesChildren(c)
    if len(ls) == 0:
        for c in ti_cs[clade_ti]:
            ls += getCladesChildren(c)
    return ls

print "Gradim tax"
for line in f_tax:
    cells = [i.strip() for i in line.strip().split('|')]
    nodeTi = int(cells[0])
    parentTi = int(cells[1])
    rank = cells[2]

    ls = ti_cs.get(parentTi,[])
    ls.append(nodeTi)
    
    ti_cs[parentTi] = ls
    ti_rank[nodeTi] = rank
    ti_parent[nodeTi] = parentTi

print "Gotov tax"
for line in f_markers_info:
    line = line.strip()
    mObj = re.search("gi\|(\d+)\|[^\|]+\|[^\|]+\|(:c*\d+-\d+)*\t.*clade': '([^']+)'",line)
    if mObj == None:
        continue
    gi = mObj.group(1)
    position = mObj.group(2) if mObj.group(2) != None else ""
    clade = mObj.group(3)
    ds[(gi,position)] = letterToTaxName[clade[0]]


print "Gotov marker info"

for elem in SeqIO.parse(p_markers,"fasta"):

    name = elem.id
    sequence = str(elem.seq)
    ars = name.split('|')
    gi = ars[1]
    position = ars[4]
    clade_name = ds.get((gi,position),None)
    if clade_name == None:
        continue

    print(">"+name+"\n"+sequence+"|"+getCladeTi(clade_name,int(ars[5]))+"\n")

'''    clade_ti = getCladeTi(clade_name,int(ars[5]))

    children = getCladesChildren(clade_ti)

    print children
    print("==============================")
   # print [elem for ls in children for elem in ls]'''
