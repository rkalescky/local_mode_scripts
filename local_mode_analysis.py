# Robert Kalescky 2013
#
# A script to generate adiabatic connection schemes
#
# Python 2.7 or higher is required
#
# Usage: python script_name adiabatic_analysis_output_file

import sys
import logging
import numpy
from GaussianLocalModeAnalysis import GaussianLocalModeAnalysis
from ACSAnalysis import ACSAnalysis

if sys.version_info < (2, 7):
    print("Python version 2.7 or higher is required.")
    sys.exit()

# Logging level
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Analyze Data
# 1. Gaussian ACS log file
# 2. ACS tab file
# 3. ACS number of plots

if len(sys.argv) == 2 or len(sys.argv) == 3:
    analysis = GaussianLocalModeAnalysis(sys.argv[1])
    if len(sys.argv) == 3:
        analysis.localModeDecompositionPlot(numpy.fromstring(sys.argv[2], dtype=int, sep=','))
    else:
        analysis.localModeDecompositionPlot()
    analysis.decompositionTable()
elif len(sys.argv) == 4:
    acs = ACSAnalysis(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    acs.localModeDecompositionPlot()
    acs.decompositionTable()
    acs.analysisTable()
    acs.acsPlots()
    acs.acsPlotsDataGraph("freq")
elif len(sys.argv) == 5:
    acs = ACSAnalysis(sys.argv[1], sys.argv[2], int(sys.argv[3]))
#    acs.acsPlots()
    acs.acsPlotsDataGraph("intensity")
else:
    print "Check input files and try again."
