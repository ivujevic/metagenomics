import subprocess
import utility_sam
import re, math, os


class BBMAP:
    def __init__(self, bbmapPath, refPath, inPath, outPath):
        self.bbmapPath = bbmapPath
        self.refPath = refPath
        self.inPath = inPath
        self.outPath = outPath
        self.ti_cs = {}
        self.ti_rank = {}
	self.ti_parent = {}
	print "DA"
	f_tax = open("/home/ivujevic/tax/nodes.dmp","r")
      	print "Start tax"
        for line in f_tax:
            cells = [i.strip() for i in line.strip().split('|')]
            nodeTi = int(cells[0])
            parentTi = int(cells[1])
            rank = cells[2]

            ls = self.ti_cs.get(parentTi,[])
            ls.append(nodeTi)

            self.ti_cs[parentTi] = ls
            self.ti_rank[nodeTi] = rank
            self.ti_parent[nodeTi] = parentTi
	print "End tax"

    def run(self):
        command = "{} ref={} in={} out={}".format(self.bbmapPath, self.refPath, self.inPath, self.outPath)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]

    def getMapQs(self):
        f = open(self.output, 'r')

        mapQScores = {}
        for line in f:
            if (len(line.strip()) == 0 or line[0] == '@'):
                continue

            sam_line = utility_sam.SAMLine(line.rstrip())
            mapQScores.get((sam_line.qname, sam_line.rname), []).append(int(sam_line.mapq))

        for key in mapQScores:
            ls = mapQScores[key]
            mapQScores[key] = sum(ls) / float(len(ls))

        return mapQScores

    def find_entry_score(self, ln, l, pScoreCutoff):
        mxBitSc = 700
        sigma2 = 3
        skipFlag = False
        mapq = float(l[4])
        mapq2 = mapq / (-10.0)
        pScore = 1.0 - pow(10, mapq2)
        if (pScore < pScoreCutoff):
            skipFlag = True

        return (pScore, skipFlag)

    def rescale_samscore(self, U, NU, maxScore, minScore):
        if (minScore < 0):
            scalingFactor = 100.0 / (maxScore - minScore)
        else:
            scalingFactor = 100.0 / maxScore

        for rIdx in U:
            if (minScore < 0):
                U[rIdx][1][0] = U[rIdx][1][0] - minScore
            U[rIdx][1][0] = math.exp(U[rIdx][1][0] * scalingFactor)
            U[rIdx][3] = U[rIdx][1][0]

        for rIdx in NU:
            NU[rIdx][3] = 0.0
            for i in range(0, len(NU[rIdx][1])):
                if (minScore < 0):
                    NU[rIdx][1][i] = NU[rIdx][1][i] - minScore

                NU[rIdx][1][i] = math.exp(NU[rIdx][1][i] * scalingFactor)
                if NU[rIdx][1][i] > NU[rIdx][3]:
                    NU[rIdx][3] = NU[rIdx][1][i]
        return (U, NU)

    def getCladesChildren(self,clade_ti):
        ls = []
	if self.ti_rank[int(clade_ti)] == "species":
		return [int(clade_ti)]
        for c in self.ti_cs.get(int(clade_ti),[]):
            if self.ti_rank[c] == "species" or len(self.ti_cs.get(int(),[])) == 0:
                ls += [c]
            else:
                ls += self.getCladesChildren(c)
	return ls
    def conv_alig2GRmat(self, pScoreCutoff):
        in1 = open(self.outPath, 'r')
        U = {}
        NU = {}
        h_readId = {}
        h_refId = {}
        genomes = []
        read = []
        gCnt = 0
        rCnt = 0

        maxScore = None
        minScore = None

        for ln in in1:
            if (ln[0] == '@' or len(ln.strip()) == 0):
                continue

            l = ln.split('\t')
            readId = l[0]
            if int(l[1]) & 0x4 == 4:  # segment unmapped
                continue
            refId = l[2]

            if refId == '*':
                continue

            parent_ti = refId.split("|")[-1]
	    if parent_ti == "95611":
		continue
            for c in self.getCladesChildren(parent_ti):
                refId = "ti|" + str(c);
		if c == 197575 and parent_ti != "197575":
			print parent_ti
                (pScore, skipFlag) = self.find_entry_score(ln, l, pScoreCutoff)

                if skipFlag:
                    continue
                if maxScore == None or pScore > maxScore:
                    maxScore = pScore
                if minScore == None or pScore < minScore:
                    minScore = pScore

                gIdx = h_refId.get(refId, -1)
                if gIdx == -1:
                    gIdx = gCnt
                    h_refId[refId] = gIdx
                    genomes.append(refId)
                    gCnt += 1

                rIdx = h_readId.get(readId, -1)

                if rIdx == -1:
                    rIdx = rCnt
                    h_readId[readId] = rIdx
                    read.append(readId)
                    rCnt += 1
                    U[rIdx] = [[gIdx], [pScore], [float(pScore)], pScore]
                else:
                    if (rIdx in U):
                        if gIdx in U[rIdx][0]:
                            continue
                        NU[rIdx] = U[rIdx]
                        del U[rIdx]

                    if gIdx in NU[rIdx][0]:
                        continue

                    NU[rIdx][0].append(gIdx)
                    NU[rIdx][1].append(pScore)

                    if pScore > NU[rIdx][3]:
                        NU[rIdx][3] = pScore
        in1.close()
        (U, NU) = self.rescale_samscore(U, NU, maxScore, minScore)
        del h_refId, h_readId
        for rIdx in U:
            U[rIdx] = [U[rIdx][0][0], U[rIdx][1][0]]  # keep gIdx and score only
        for rIdx in NU:
            pScoreSum = sum(NU[rIdx][1])
            NU[rIdx][2] = [k / pScoreSum for k in NU[rIdx][1]]  # Normalizing pScore

        return U, NU, genomes, read
