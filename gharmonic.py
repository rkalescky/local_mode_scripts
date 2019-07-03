import sys
from GaussianFrequencyLogFile import GaussianFrequencyLogFile

if sys.version_info < (2, 7):
    print("Python version 2.7 or higher is required.")
    sys.exit()

# Create Gaussian file object
adiaLogFile = GaussianFrequencyLogFile(sys.argv[1])

for i in range(0, adiaLogFile.numberModes()):
	print adiaLogFile.normalModeSymmetries()[i], '\t',  adiaLogFile.normalModeFrequencies()[i]

