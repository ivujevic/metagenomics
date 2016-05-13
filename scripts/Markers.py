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
            clade = mObj.group(4)[3:]

            ls = self.marker_species.get((gi,position),[])

            for o in ext.split(","):
		if o == "":
			continue
		ti = tax_tree.get_ti(o.strip()[1:-1])
		if ti == None:
			continue
                ls.append(ti)

	    f = clade.find("_noname")
	    if f != -1:
		clade = "unclassified_"+clade[:f]
	    if clade == "Staphylococcus_caprae_capitis":
		clade = "Staphylococcus_capitis"
	    elif clade == "Streptomyces_roseochromogenes":
		clade = "Streptomyces_roseochromogenes_sic"
	    ti = tax_tree.get_ti(clade)
	    if ti == None:
		continue
            ls += tax_tree.get_species(ti)

            self.marker_species[(gi,position)] = ls

    def get_species(self,gi,position):
        return self.marker_species.get((gi, position), [])
    def print_dict(self):
	f = open("dict.txt","w")
	f.write(str(self.marker_species))
	f.close()

