import sys
import bbMapWraper
import pathoscope

def test():
    path = sys.argv[1]
    print(path)
    bb = bbMapWraper.BBMAP("","","",path)
    (U,NU,genomes,reads) = bb.conv_alig2GRmat(0.01)
    (initPi, pi, _, NU) = pathoscope.algorithm(U,NU,genomes,50,0.01,False,0,0)
    tmp = zip(initPi,genomes)
    tmp = sorted(tmp,reverse=True)
    k = 0
    for i in tmp:
   	print i
	k+=1
	if k == 10:
		break

if __name__ == "__main__":
    test()
