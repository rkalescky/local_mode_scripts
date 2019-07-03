import sys
from CFOURLogFile import CFOURLogFile

if sys.version_info < (2, 7):
    print("Python version 2.7 or higher is required.")
    sys.exit()

# Create Gaussian file object
cfourLogFile = CFOURLogFile(sys.argv[1])

# Print files
cfourLogFile.printCartesianCoordintes()

