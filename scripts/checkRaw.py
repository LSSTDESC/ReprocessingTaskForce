import os
import numpy as np
from astropy.io import fits

filter = "u"

output = filter + "_new.list"

rawDir = "../../rawDownload"

fname = os.path.join("../..", filter + ".list")
print fname
with open(fname) as f:
    content = f.readlines()
    
fout = open(output,'w')
    
for line in content :
    visit = line.rstrip().split("=")[1]
    print "Checking visit %s"%(visit)

    fn = rawDir + "/"+ visit + "p.fits.fz"
    hdulist = fits.open(fn)

#    fig, ax = plt.subplots(ncols=6, nrows=6, figsize=(20, 20))

    bad = []
    for i in range(0, 36) :
        k = i//6
        l = i%6
        scidata = hdulist[i+1].data.ravel()
        pmax = np.amax(scidata)
        filt = scidata > 0.9*pmax
        a = scidata[filt]
        num = filt.sum()
        if num > 100000 :
            print "Found saturated CCD %d in Visit %s - %d"%(i, visit, num)
            bad.append(i)
    if len(bad) == 0 :
        lnOut = "--id visit=" + visit + " ccd=0..35"
    else :
        lnOut = "--id visit=" + visit
        first = True
        for b in range (0, 36) :
            if b in bad :
                next
            else :
                if first :
                    lnOut += " ccd=" + str(b)
                    first = False
                else :
                    lnOut += "^" + str(b)
    fout.write(lnOut + "\n")
fout.close()
