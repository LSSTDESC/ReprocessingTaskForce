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
        script = workdir + "/05-jointcal/scripts/%s/jointcal_%s.sh" % (filt, filt)
        vars.put("CUR_SCRIPT", script)
        pipeline.createSubstream("jointcalFilter", num, vars)

