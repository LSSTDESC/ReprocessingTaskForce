from java.util import HashMap

def runscripts():
    process = pipeline.getProcessInstance("setup_processccd")
    vars = HashMap(process.getVariables())
    workdir = vars.remove("WORK_DIR")
    num = 0
    for filt in ['u', 'g', 'r', 'i', 'z']:
        nscript = vars.remove('n' + filt + 'scripts')
        for i in range(1, int(nscript) + 1):
            script = workdir + "/02-processccd/scripts/%s/visit_%03d_script.sh" % (filt, i)
            vars.put("CUR_SCRIPT", script)
            pipeline.createSubstream("processFilter", num, vars)
            num += 1
