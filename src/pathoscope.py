import subprocess


def algorithm(U, NU, genomes, maxIter, emEpsilon, verbose, piPrior, thetaPrior):
    G = len(genomes)
    pi = [1. / G] * G
    initPi = pi
    theta = [1. / G] * G

    pisum0 = [0] * G

    Uweights = [U[i][1] for i in U]  # weights for unique reads...
    maxUweights = 0
    Utotal = 0

    if Uweights:
        maxUweights = max(Uweights)
        Utotal = sum(Uweights)
    for i in U:
        pisum0[U[i][0]] += U[i][1]

    NUweights = [NU[i][3] for i in NU]  # weights for non-unique reads...
    maxNUweights = 0
    NUtotal = 0
    if NUweights:
        maxNUweights = max(NUweights)
        NUtotal = sum(NUweights)
    priorWeight = max(maxUweights, maxNUweights)
    lenNU = len(NU)
    if lenNU == 0:
        lenNU = 1
 
    for i in range(maxIter):  ## EM iterations--change to convergence
        pi_old = pi
	theta_old = theta
        thetasum = [0 for k in genomes]

        # E Step

        for j in NU:  # for each non-uniq read, j
            z = NU[j]
            ind = z[0]  # a set of any genome mapping with j
            pitmp = [pi[k] for k in ind]  ### get relevant pis for the read
            thetatmp = [theta[k] for k in ind]  ### get relevant thetas for the read
            xtmp = [1. * pitmp[k] * thetatmp[k] * z[1][k] for k in range(len(ind))]  ### Calculate unormalized xs
            xsum = sum(xtmp)
            if xsum == 0:
                xnorm = [0.0 for k in xtmp]  ### Avoiding dividing by 0 at all times
            else:
                xnorm = [1. * k / xsum for k in xtmp]  ### Normalize new xs

            NU[j][2] = xnorm  ## Update x in NU

            for k in range(len(ind)):
                # thetasum[ind[k]] += xnorm[k]   		### Keep running tally for theta
                thetasum[ind[k]] += xnorm[k] * NU[j][3]  ### Keep weighted running tally for theta

        # M step
        pisum = [thetasum[k] + pisum0[k] for k in range(len(thetasum))]  ### calculate tally for pi
        pip = piPrior * priorWeight  # pi prior - may be updated later
        # pi = [(1.*k+pip)/(len(U)+len(NU)+pip*len(pisum)) for k in pisum]  		## update pi
        # pi = [1.*k/G for k in pisum]  		## update pi
        totaldiv = Utotal + NUtotal
        if totaldiv == 0:
            totaldiv = 1
        pi = [(1. * k + pip) / (Utotal + NUtotal + pip * len(pisum)) for k in pisum]  ## update pi
        if (i == 0):
            initPi = pi

        thetap = thetaPrior * priorWeight  # theta prior - may be updated later
        NUtotaldiv = NUtotal
        if NUtotaldiv == 0:
            NUtotaldiv = 1
        theta = [(1. * k + thetap) / (NUtotaldiv + thetap * len(thetasum)) for k in thetasum]
        # theta = [(1.*k+thetap)/(lenNU+thetap*len(thetasum)) for k in thetasum]

        cutoff = 0.0
	theta_cutoff = 0.0
        for k in range(len(pi)):
            cutoff += abs(pi_old[k] - pi[k])
	    theta_cutoff += abs(theta_old[k] - theta[k])
        if (theta_cutoff <= emEpsilon or lenNU == 1):
            break
    return initPi, pi, theta, NU


def write_tsv_report(nR, nG, pi, genomes, initPi, bestHitInitial, bestHitInitialReads,
                     bestHitFinal, bestHitFinalReads, level1Initial, level2Initial, level1Final, level2Final, noCutOff):
    tmp = zip(pi, genomes, initPi, bestHitInitial, bestHitInitialReads, bestHitFinal,
              bestHitFinalReads, level1Initial, level2Initial, level1Final, level2Final)
    tmp = sorted(tmp, reverse=True)
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11 = zip(*tmp)
    for i in range(len(x10)):
        if (not (noCutOff) and x1[i] < 0.01 and x10[i] <= 0 and x11[i] <= 0):
            break
        if i == (len(x10) - 1):
            i += 1
    tmp = zip(x2[:i], x1[:i], x6[:i], x7[:i], x10[:i], x11[:i], x3[:i], x4[:i], x5[:i], x8[:i],
              x9[:i])  # Changing the column order here
    return (x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11)

'''
Computes the best hit read metrics
'''


def computeBestHit(U, NU, genomes, read):
    bestHitReads = [0.0 for _ in genomes]
    level1Reads = [0.0 for _ in genomes]
    level2Reads = [0.0 for _ in genomes]
    for i in U:
        bestHitReads[U[i][0]] += 1
        level1Reads[U[i][0]] += 1
    for j in NU:
        z = NU[j]
        ind = z[0]
        xnorm = z[2]
        bestGenome = max(xnorm)
        numBestGenome = 0
        for i in range(len(xnorm)):
            if (xnorm[i] == bestGenome):
                numBestGenome += 1
        if (numBestGenome == 0):
            numBestGenome = 1
        for i in range(len(xnorm)):
            if (xnorm[i] == bestGenome):
                bestHitReads[ind[i]] += 1.0 / numBestGenome
                if (xnorm[i] >= 0.5):
                    level1Reads[ind[i]] += 1
                elif (xnorm[i] >= 0.01):
                    level2Reads[ind[i]] += 1

    nG = len(genomes)
    nR = len(read)
    bestHit = [bestHitReads[k] / nR for k in range(nG)]
    level1 = [level1Reads[k] / nR for k in range(nG)]
    level2 = [level2Reads[k] / nR for k in range(nG)]
    return bestHitReads, bestHit, level1, level2
