import sys
import bbMapWraper
import pathoscope


def test():
    path = sys.argv[1]
    bb = bbMapWraper.BBMAP("", "", "", path)
    (U, NU, genomes, reads, coverage) = bb.conv_alig2GRmat(0.01)
    if len(U) == 0 and len(NU) == 0:
        print("No hits found")
        return

    (bestHitInitialReads, bestHitInitial, level1Initial, level2Initial) = pathoscope.computeBestHit(U, NU, genomes,
                                                                                                    reads)
    (initPi, pi, _, NU) = pathoscope.algorithm(U, NU, genomes, 50, 0.01, True, 1, 1)
    (bestHitFinalReads, bestHitFinal, level1Final, level2Final) = pathoscope.computeBestHit(U, NU, genomes, reads)
    tmps = zip(pi, genomes, bestHitFinal, bestHitInitial)
    tmps = sorted(tmps, reverse=True)
    k = 0
    for tmp in tmps:
        print(str(tmp[0]) + "\t" + tmp[1] + "\t" + str(tmp[2])+ "\t"+ str(tmp[3]) + "\t" + str(sum(coverage[tmp[1]])))
        k += 1
        if k == 10:
            break


if __name__ == "__main__":
    test()
