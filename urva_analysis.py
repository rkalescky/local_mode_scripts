import sys
from GaussianURVALogFile import GaussianURVALogFile

if sys.version_info < (2, 7):
    print("Python version 2.7 or higher is required.")
    sys.exit()

# Create Gaussian file object
urvaLogFile = GaussianURVALogFile(sys.argv[1])

# Print files
if len(sys.argv) == 2:
    label_type = None
else:
    label_type = sys.argv[2]

urvaLogFile.printReactionPathVectors(label_type)
urvaLogFile.printReactionPathCurvatureVectors(label_type)
