import sys
import bbMapWraper
import pathoscope


def test():
    path = sys.argv[1]
    bb = bbMapWraper.BBMAP("", "", "", path)
    (U, NU, genomes, reads) = bb.conv_alig2GRmat(0.01)
    if len(U) == 0 and len(NU) == 0:
        print("No hits found")
        return

    (bestHitInitialReads, bestHitInitial, level1Initial, level2Initial) = pathoscope.computeBestHit(U, NU, genomes,
                                                                                                    reads)
    (initPi, pi, _, NU) = pathoscope.algorithm(U, NU, genomes, 50, 0.01, True, 1, 1)
    (bestHitFinalReads, bestHitFinal, level1Final, level2Final) = pathoscope.computeBestHit(U, NU, genomes, reads)
    tmp = zip(pi, genomes, bestHitFinal, bestHitInitial)
    tmp = sorted(tmp, reverse=True)
    k = 0
    for i in tmp:
        print(tmp[i])
        k += 1
        if k == 10:
            break


if __name__ == "__main__":
    test()
