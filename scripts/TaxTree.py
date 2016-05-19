import re
class TaxTree:
    def __init__(self,tax_path,ref_seq_path, tax_names):
        self.tax_path = tax_path
        self.refSeq_path = ref_seq_path
        self.tax_names = tax_names
        self.ti_cs = {}
        self.name2ti = {}
        self.ti_rank = {}

        f_tax = open(self.tax_path,"r")

        # Add children to the parents
        for line in f_tax:
            line = line.strip()
            ars = line.split("|")
            cs = self.ti_cs.get(ars[1].strip(),[])
            cs.append(ars[0].strip())
            self.ti_cs[ars[1].strip()] = cs
            self.ti_rank[ars[0].strip()] = ars[2].strip()

        # read names.dmp and map names to ti
        f_tax.close()
        f_tax_names = open(self.tax_names,"r")
        for line in f_tax_names:
            line = line.strip()
            ars = line.split("|")
            
	  
	    ti = ars[0].strip()
            name = ars[1].strip()
            name = re.sub('[^\w]+','_',name)
	    name = name.strip('_')
	    if self.name2ti.get(name,"") == "":
		self.name2ti[name] = ti
	    elif ars[3].strip() == "scientific name":
                self.name2ti[name] = ti

        # GCF to species ti
        f_ref_seq = open(self.refSeq_path,"r")
        for line in f_ref_seq:
            line = line.strip()
            ars = line.split("\t")
            if line == "" or line[0] == '#':
                continue

            name = ars[0].strip().split('.')[0]
	    name = name[4:]
            spec_ti = ars[6].strip()
            if self.name2ti.get(name,"") == "":
                self.name2ti["GCF_"+name] = spec_ti
                self.name2ti["GCA_"+name] = spec_ti

    def get_ti(self,name):
	ret = self.name2ti.get(name,"")
	if ret == "":
		print("Nema ", name)
	else:
		return ret

    def get_species(self,clade_ti):
        ls = []
        if self.ti_rank[clade_ti] == "species":
            return [int(clade_ti)]

        for c in self.ti_cs.get(clade_ti,[]):
            if self.ti_rank[c] == "species" or len(self.ti_cs.get(clade_ti,[])) == 0:
                ls += [int(c)]
            else:
                ls += self.get_species(c)

        return ls
