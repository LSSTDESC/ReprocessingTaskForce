import os
import numpy as np
from astropy.io import fits

if __name__ == "__main__":

    #usage = """%prog [option]"""
    #description = """TBD"""
    #
    #parser = OptionParser(description=description, usage=usage)
    #parser.add_option("-f", "--filters", type="string", default=None,
    #                  help="Filter(s) [%default]. Can also be a list of filter (comma separated)")
    #parser.add_option("-c", "--configs", type="string", default="processConfig.py",
    #                  help="Configuration file [%default]. Several files (and filters with option -f) "
    #                  "can be given if a filter needs its own config file. In that case, include"
    #                  " '_f' in the name of the file. e.g.: processConfig.py,processConfig_u.py if you"
    #                  " want the 'u' filter to use a different configuration file. The default config"
    #                  " must be the first one.")
    #parser.add_option("-i", "--input", type="string", default="pardir/input", help="Input directory")
    #parser.add_option("-o", "--output", type="string", default="pardir/output",
    #                  help="output directory")
    #parser.add_option("-m", "--mod", type="int", default=4,
    #                  help="Nbr. of visits per job [%default]")
    #parser.add_option("-M", "--max", type="int", default=999,
    #                  help="Max nbr of jobs to be submitted [%default]")
    #parser.add_option("-a", "--autosubmit", action='store_true', default=False,
    #                  help="Submit the jobs automatically")
    #parser.add_option("-s", "--system", type="string", default="cl7",
    #                  help="System used to run the jobs")
    #parser.add_option("--vmem", type="string", default='4G', help="Job memory [%default]")
    #parser.add_option("--ct", type="int", default='60000', help="Job cpu time [%default]")
    #parser.add_option("--queue", type="string", help="Job queue [%default]")
    #parser.add_option("--otheroptions", type="string", help="Other options [%default]")
    #parser.add_option("--multicore", action='store_true', default=False,
    #                  help="Multicore jobs (mostly for processCcd)")
    #parser.add_option("--fromslac", action='store_true', default=False,
    #                  help="Run job from slac workflow interface")
    #opts, args = parser.parse_args()


#    filter = "u"
    
#    output = filter + "_new.list"
    
#    rawDir = "../../rawDownload"
    
#    fname = os.path.join("../..", filter + ".list")
#    print fname
#    with open(fname) as f:
#        content = f.readlines()
    content = [1]
    fout = open("output.list",'w')
    from glob import glob
    fns = glob("/home/chotard/Work/clusters/badvisits/*p.fits.fz")
    #for line in content:
    for fn in fns:
        #visit = line.rstrip().split("=")[1]
        #print "Checking visit %s"%(visit)

        #fn = rawDir + "/"+ visit + "p.fits.fz"
        #print fn
        #fn = "/home/chotard/Work/clusters/badvisits/1758036p.fits.fz"
        hdulist = fits.open(fn)

        bad = []
        for i in range(0, 36):
            k = i//6
            l = i%6
            scidata = hdulist[i+1].data.ravel()
            pmax = np.amax(scidata)
            filt = scidata > 0.9*pmax
            a = scidata[filt]
            num = filt.sum()
            if num > 100000: #100000:
                print "Found saturated CCD %d in Visit %s - %d" % (i, fn, num) #visit, num)
                bad.append(i)
            #if num > 10000:
            #    print i, num
        if len(bad) == 0:
            print "%s is OK" % fn
            #lnOut = "--id visit=" + visit + " ccd=0..35"
        else:
            lnOut = "--id visit=" #+ visit
            first = True
            for b in range (0, 36):
                if b in bad:
                    next
                else:
                    if first:
                        lnOut += " ccd=" + str(b)
                        first = False
                    else:
                        lnOut += "^" + str(b)
        #fout.write(lnOut + "\n")
    fout.close()
