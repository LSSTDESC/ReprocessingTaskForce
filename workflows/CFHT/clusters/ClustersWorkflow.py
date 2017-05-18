from java.util import HashMap


FILTERS = ['u', 'g', 'r', 'i', 'z']

def run_processCcd():
    process = pipeline.getProcessInstance("setup_processccd")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    num = 0
    for filt in FILTERS:
        nscript = vars.remove('n' + filt + 'scripts')
        for i in range(1, int(nscript) + 1):
            script = workdir + "/02-processccd/scripts/%s/visit_%03d_script.sh" % (filt, i)
            vars.put("CUR_SCRIPT", script)
            pipeline.createSubstream("processFilter", num, vars)
            num += 1


def run_jointcal():
    process = pipeline.getProcessInstance("setup_jointcal")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    for num, filt in enumerate(FILTERS):
        script = workdir + "/04-jointcal/scripts/%s/jointcal_%s.sh" % (filt, filt)
        vars.put("CUR_SCRIPT", script)
        pipeline.createSubstream("jointcalFilter", num, vars)


def run_jointcalCoadd():
    process = pipeline.getProcessInstance("setup_jointcalCoadd")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    for num, filt in enumerate(FILTERS):
        script = workdir + "/05-jointcalCoadd/scripts/%s/patches_%s_script.sh" % (filt, filt)
        vars.put("CUR_SCRIPT", script)
        pipeline.createSubstream("jointcalCoaddFilter", num, vars)


def run_assembleCoadd():
    process = pipeline.getProcessInstance("setup_assembleCoadd")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    num = 0
    for filt in FILTERS:
        nscript = vars.remove('n' + filt + 'scripts')
        for i in range(1, int(nscript) + 1):
            script = workdir + "/06-assembleCoadd/scripts/%s/patches_%03d.sh" % (filt, i)
            vars.put("CUR_SCRIPT", script)
            pipeline.createSubstream("assembleCoaddFilter", num, vars)
            num += 1


def run_detectCoaddSources():
    process = pipeline.getProcessInstance("setup_detectCoaddSources")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    for num, filt in enumerate(FILTERS):
        script = workdir + "/07-detectCoaddSources/scripts/%s/patches_%s.sh" % (filt, filt)
        vars.put("CUR_SCRIPT", script)
        pipeline.createSubstream("detectCoaddSourcesFilter", num, vars)


def run_mergeCoaddDetections():
    process = pipeline.getProcessInstance("setup_mergeCoaddDetections")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    nscript = vars.remove('nscripts')
    for num in range(int(nscript)):
        script = workdir + "/08-mergeCoaddDetections/scripts/patches_all.txt_%02d.sh" % num
        vars.put("CUR_SCRIPT", script)
        pipeline.createSubstream("mergeCoaddDetectionsFilter", num, vars)


def run_measureCoaddSources():
    process = pipeline.getProcessInstance("setup_measureCoaddSources")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    num = 0
    for filt in FILTERS:
        nscript = vars.remove('n' + filt + 'scripts')
        for i in range(int(nscript)):
            script = workdir + "/09-measureCoaddSources/scripts/%s/patches_%s.txt_%02d.sh" % \
                     (filt, filt, i)
            vars.put("CUR_SCRIPT", script)
            pipeline.createSubstream("measureCoaddSourcesFilter", num, vars)
            num += 1