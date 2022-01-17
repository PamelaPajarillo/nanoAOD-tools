
#!/usr/bin/env python

import ROOT
from importlib import import_module
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.fatJetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *


def preprocess(Inputs, OutputFolder, Year, Run = "MC"):
    JSON = None
    useModules = [PrefCorr(Year)]
    if Run == "MC":
        jmeCorrectionsAK8 = createJMECorrector(True, Year, Run, "All", "AK8PFPuppi")
        useModules.append(jmeCorrectionsAK8())
        jmeCorrectionsAK4 = createJMECorrector(True, Year, Run, "All", "AK4PF")
        useModules.append(jmeCorrectionsAK4())
        if Year == "2016":
            useModules.append(puWeight_2016())
        if Year == "2017":
            useModules.append(puWeight_2017())
        if Year == "2018":
            useModules.append(puWeight_2018())

    p = PostProcessor(OutputFolder, [Inputs],  modules=useModules, provenance=False, outputbranchsel="/users/h2/ppajarillo/CMSSW_10_2_0/analysis_update/JetEnergySystematics/keep.txt", jsonInput=JSON)
    p.run()



outputfolder = '/cms/vlq/ppajarillo/Bprime_NanoAODv7/' + str(sys.argv[1]) + '/' + str(sys.argv[2]) + '/'
print(outputfolder)
preprocess(sys.argv[3], outputfolder, sys.argv[1])
