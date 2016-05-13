import TaxTree
import re
import ast

class Markers:
    def __init__(self,path,tax_tree):
        self.path = path
        self.tax_tree = tax_tree

        self.marker_species = {}

        f_marker = open(path,"r")
        for line in f_marker:
            line = line.strip()

            ars = line.strip("  ")
            mObj = re.search("gi\|(\d+)\|[^\|]+\|[^\|]+\|(:c*\d+-\d+)*\t.*set\(\[([^\]]*)\]\),.*'clade': '([^']+)'",line)
            if mObj == None:
                continue
            gi = mObj.group(1)
            position = mObj.group(2) if mObj.group(2) != None else ""
            ext = mObj.group(3)
            clade = mObj.group(4)

            ls = self.marker_species.get((gi,position),[])

            for o in ext.split(","):
                ls.append(tax_tree.get_ti(o.strip()[1:-1]))

            ls += tax_tree.get_species(clade)
