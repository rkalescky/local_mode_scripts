import numpy
import math
from GaussianLogFile import GaussianLogFile

class GaussianFrequencyLogFile(GaussianLogFile):

    def __init__(self, input_file):
        GaussianLogFile.__init__(self, input_file)
        self.__file = self._GaussianLogFile__file
        self.__getNumberModes()
        self.__getNormalModeFrequencies()
        self.__getNormalModeSymmetries()

    def moleculeIsLinear(self):
        if "*" in self.moleculeSymmetry():
            return True
        else:
            return False

    def __getNumberModes(self):
        if self.moleculeIsLinear():
            L = 5
        else:
            L = 6
        self.__number_modes = 3 * self.numberAtoms() - L
        return None

    def __getNormalModeFrequencies(self):
        self.__normal_mode_frequencies = numpy.zeros(shape=(self.__number_modes))
        k = 0
        for i in range(0, len(self.__file)):
            if "Frequencies --" in self.__file[i]:
                line = self.__file[i].split()
                for j in range(2, len(line)):
                    self.__normal_mode_frequencies[k] = float(line[j])
                    k += 1
                    if k == self.__number_modes:
                        break
            if k == self.__number_modes:
                break
        return None
    
    def __getNormalModeSymmetries(self):
        self.__normal_mode_symmetries = []
        k = 0
        for i in range(0, len(self.__file)):
            if "Frequencies --" in self.__file[i]:
                for j in range(0, len(self.__file[i - 1].split())):
                    self.__normal_mode_symmetries.append(str(self.__file[i - 1].split()[j]))
                    k += 1
                    if k == self.__number_modes:
                        break
        return None

    def numberModes(self):
        return self.__number_modes
    
    def normalModeFrequencies(self):
        return self.__normal_mode_frequencies
    
    def normalModeSymmetries(self):
        return self.__normal_mode_symmetries
