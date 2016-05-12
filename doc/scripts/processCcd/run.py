#!/usr/bin/env python

import os
import time
import sys
from optparse import OptionParser

def submit(visitList, toWrite, config, filt, clobber) :
    
    filename = "scripts/" + filt + "/" + visitList + ".list"
    if not os.path.isdir("scripts/" + filt) :
        os.makedirs("scripts/" + filt)
        
    theFile = open(filename,"w+")
    for line in toWrite:
        print>>theFile, line
    
    configFile=config

    if filt == 'u':
        configFile='processConfig_u.py'

    cmd = "processCcd.py _parent/input --output _parent/output @" + filename + " --configfile " + configFile 
    if clobber :
        cmd = cmd + " --clobber-config"
    print cmd
    
    cwd = os.getcwd()
    dirLog = cwd + "/log/" + filt
    if not os.path.isdir(dirLog) :
        os.makedirs(dirLog)
    log = dirLog + "/" + visitList + ".log"
    print log
    qsub = "qsub -P P_lsst_prod -l sps=1,ct=80000,h_vmem=16G -j y -o "+ log + " <<EOF"
    scriptName = "scripts/" + filt + "/" + visitList + ".sh"
    script = open(scriptName,"w")
    script.write(qsub + "\n")
    script.write("#!/usr/local/bin/bash\n")
    script.write(" cd " + cwd + "\n")
    script.write("bash " + "\n")
    script.write(" which setup " + "\n")
    script.write(" source setup_processCcd.sh\n")
    script.write(" " + cmd + "\n")
    script.write("EOF" + "\n")
    script.close()
    os.system("chmod +x " + scriptName)
    os.system("./"+scriptName)
    time.sleep(1)

if __name__ == "__main__":

    filters = "ugriz"
    parser = OptionParser()
    parser.add_option("-F", "--filter", type="string", default="r", help="Filter [%default]")
    parser.add_option("-m", "--mod", type="int", default=10, help="Nbr. of visits per job [%default]")
    parser.add_option("-M", "--max", type="int", default=999, help="Max nbr of jobs to be submitted [%default]")
    parser.add_option("-c", "--config", type="string", default="processConfig.py", help="Configuration file [%default]")
    parser.add_option("-C", "--clobber", action="store_true", default=False, help="Clobber config if present")
    parser.add_option("-l", "--list", type="string", default="u.list", help="List to be processed [%default]")
    opts, args = parser.parse_args()

    clobber = opts.clobber

    filt = opts.filter
    if filt not in filters :
        sys.exit("Unknown filter : " + filt)
        
    #filename = filt + ".list"
     
    filename=opts.list

    print 'The following list will be processed: ',filename
    
    modularity = opts.mod
    maxVisit = opts.max
    configFile = opts.config
     
    file = open(filename,"r")
    imod = 0
    visitList = ""
    toWrite = []
    flag = 0
    count_visit={}
    
    for cnt, line in enumerate(file) :
        line = line[:-1]
        
        words = line.split()
        
        for vals in words:
            if vals.count('visit'):
                visit = vals.split("=")[1]

        if len(words) == 2 :
            line = line + " filter=" +filt
            line = line + " ccd=0..35"
        if cnt > maxVisit-1 :
            break
        if imod < modularity :
            visitList = visitList + visit + "_"
            toWrite.append(line)
            imod += 1
        else :
            visitList = visitList[:-1]
            if not count_visit.has_key(visitList):
                count_visit[visitList]=1
            else:
               count_visit[visitList]+=1 
            print visitList,count_visit[visitList]
            submit(visitList+"_"+str(count_visit[visitList]), toWrite, configFile, filt, clobber)
            toWrite = []
            toWrite.append(line)
            visitList = visit + "_"
            imod = 1

    visitList = visitList[:-1]
    submit(visitList, toWrite, configFile, filt, clobber)
    
	
	
	
