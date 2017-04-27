from java.util import HashMap

def runscripts():
    process = pipeline.getProcessInstance("setup_processccd")
    vars = HashMap(process.getVariables())
    for filt in ['u', 'g', 'r', 'i', 'z']:
        nscript = vars.remove['n' + filt + 'scripts']
        for i in range(1, nscript + 1):
            script = vars["WORK_DIR"] + "/02-processccd/scripts/%s/visit_%03d_script.sh" % (filt, i)
            vars.put("CUR_SCRIPT", script)
            pipeline.createSubstream("processFilter", i, vars)