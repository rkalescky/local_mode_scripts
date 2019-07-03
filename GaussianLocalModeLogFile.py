import numpy
import math
from operator import itemgetter
from GaussianFrequencyLogFile import GaussianFrequencyLogFile

class GaussianLocalModeLogFile(GaussianFrequencyLogFile):

    def __init__(self, input_file):
        GaussianFrequencyLogFile.__init__(self, input_file)
        self.__file = self._GaussianLogFile__file
        self.__getNumberOfParameters()
        self.__isExperimentalLocalModeCalculation()
        self.__getLocalModeCharacter()
        self.__getAtomConnectivity()
        self.__getLocalModeForceConstants()
        self.__getLocalModeFrequencies()
        self.__getNumberStretchesBendsTorsions()
        self.__getLocalModeLabels()
        self.__getConnectivityTypes()
        self.__getLocalModeUserLabels() 
    
    def __getNumberOfParameters(self):
        for i in range(0, len(self.__file)):
            if "NParm(New)=" in self.__file[i]:
                line = self.__file[i].split()
                self.__number_parameters = int(line[len(line) - 1])
                break
        return None

    def __isExperimentalLocalModeCalculation(self):
        for i in range(0, len(self.__file)):
            if "Experimental frequencies read from input stream" in self.__file[i]:
                self.__local_mode_experimental = True
                break
            else:
                self.__local_mode_experimental = False
        return None

    def __getLocalModeCharacter(self):
        temp = numpy.zeros(shape=(self.numberModes(), self.numberModes()))
        self.__local_mode_character = numpy.zeros(shape=(self.numberModes(), self.numberModes()))
        exp_freq = numpy.zeros(shape=(self.numberModes()))
        normal_mode = 0
        experimental_local_mode_section_found = False
        for i in range(0, len(self.__file)):
            if self.__local_mode_experimental == True and experimental_local_mode_section_found == False:
                if "Using experimentaly corrected force constants" in self.__file[i]:
                    experimental_local_mode_section_found = True
            if self.__local_mode_experimental == False or experimental_local_mode_section_found == True:
                if " <Absolute amplitudes:>" in self.__file[i]:
                    exp_freq[normal_mode] = float(self.__file[i - 1].split()[4])
                if "<Renormalized to percentage:>" in self.__file[i]:
                    for j in range(2, 2 + self.numberModes()):
                        if "<End of Renormalized to percentage:>" in self.__file[i + j]:
                            break
                        else:
                            parameter_number = int(self.__file[i + j].split()[0]) - 1
                            mode_percentage = float(self.__file[i + j].split()[2]) * 100
                            temp[normal_mode, parameter_number] = mode_percentage
                    normal_mode = normal_mode + 1
                if normal_mode == self.numberModes():
                    break
        
        if self.__local_mode_experimental == True:
            self._GaussianFrequencyLogFile__normal_mode_frequencies = sorted(exp_freq)
            exp_arrangement = numpy.argsort(exp_freq)
            for i in range(0, self.numberModes()):
                for j in range(0, self.numberModes()):
                    self.__local_mode_character[i][j] = temp[exp_arrangement[i]][j]
            self.__local_mode_character = numpy.transpose(self.__local_mode_character)
            return None
                
        self.__local_mode_character = numpy.transpose(temp)
        return None

    def __getAtomConnectivity(self):
        self.__atom_connectivity = numpy.zeros(shape=(self.__number_parameters, 4), dtype=numpy.int8)
        local_mode_section = False
        for i in range(0, len(self.__file)):
            if "Leading Parameter Analysis" in self.__file[i]:
                local_mode_section = True
            elif "Total amount of memory requested:" in self.__file[i] and local_mode_section == True:
                for j in range(1, self.__number_parameters + 1):
                    for k in range(0, 4):
                        self.__atom_connectivity[j - 1,k] = int(self.__file[i + j].split()[k])
                break
        return None

    def __getLocalModeForceConstants(self):
        self.__local_mode_force_constants = numpy.zeros(self.__number_parameters)
        for i in range(0, len(self.__file)):
            if self.__local_mode_experimental == True:
                if "Using experimentaly corrected force constants" in self.__file[i]:
                    for k in range(i, len(self.__file)):
                        if "AvK" in self.__file[k]:
                            for j in range(1, self.__number_parameters + 1):
                                self.__local_mode_force_constants[j - 1] = float(self.__file[k + j].split()[1])
                            break
            else:
                if "AvK" in self.__file[i]:
                    for j in range(1, self.__number_parameters + 1):
                        self.__local_mode_force_constants[j - 1] = float(self.__file[i + j].split()[1])
                    break
        return None

    def __getLocalModeFrequencies(self):
        self.__local_mode_frequencies = numpy.zeros(self.__number_parameters)
        for i in range(0, len(self.__file)):
            if "ParNo     AvK   AvM   AvFr  AvMG  AvFrG" in self.__file[i]:
                for j in range(1, self.__number_parameters + 1):
                    self.__local_mode_frequencies[j - 1] = float(self.__file[i + j].split()[5])
                if self.__local_mode_experimental == False:
                    break
        return None
    
    def __getNumberStretchesBendsTorsions(self):
        self.__number_torsions = 0
        self.__number_bends = 0
        self.__number_stretches = 0
        for i in range(0, self.__number_parameters):
            if self.__atom_connectivity[i][3] != 0:
                self.__number_torsions = self.__number_torsions + 1
        for i in range(0, self.__number_parameters):
            if self.__atom_connectivity[i][2] != 0:
                self.__number_bends = self.__number_bends + 1
        self.__number_stretches = self.__number_parameters - self.__number_bends
        self.__number_bends = self.__number_bends - self.__number_torsions
        return None

    def __getLocalModeLabels(self):
        self.__local_mode_labels = []
        for i in range(0, self.__number_parameters):
            if self.__atom_connectivity[i][2] == 0 and self.__atom_connectivity[i][3] == 0:
                self.__local_mode_labels.append('{}{}{}{}{}'.format(
                    self.atomElements()[self.__atom_connectivity[i][0] - 1], self.__atom_connectivity[i][0], "-",
                    self.atomElements()[self.__atom_connectivity[i][1] - 1],self.__atom_connectivity[i][1]))
            elif self.__atom_connectivity[i][2] != 0 and self.__atom_connectivity[i][3] <= 0:
                label = '{}{}{}{}{}{}{}{}'.format(
                    self.atomElements()[self.__atom_connectivity[i][0] - 1],
                    self.__atom_connectivity[i][0], "-", self.atomElements()[self.__atom_connectivity[i][1] - 1],
                    self.__atom_connectivity[i][1], "-", self.atomElements()[self.__atom_connectivity[i][2] - 1],
                    self.__atom_connectivity[i][2])
                if self.__atom_connectivity[i][3] == -1:
                    label += " (x)"
                elif self.__atom_connectivity[i][3] == -2:
                    label += " (y)"
                self.__local_mode_labels.append(label)
            else:
                self.__local_mode_labels.append('{}{}{}{}{}{}{}{}{}{}{}'.format(
                    self.atomElements()[self.__atom_connectivity[i][0] - 1], self.__atom_connectivity[i][0], "-",
                    self.atomElements()[self.__atom_connectivity[i][1] - 1], self.__atom_connectivity[i][1], "-",
                    self.atomElements()[self.__atom_connectivity[i][2] - 1], self.__atom_connectivity[i][2], "-",
                    self.atomElements()[self.__atom_connectivity[i][3] - 1], self.__atom_connectivity[i][3]))
        return None
    
    def __getConnectivityTypes(self):
        self.__element_connectivity = []
        for i in range(0, self.__number_parameters):
            if self.__atom_connectivity[i][2] == 0 and self.__atom_connectivity[i][3] == 0:
                self.__element_connectivity.append('{}{}'.format(
                    self.atomElements()[self.__atom_connectivity[i][0] - 1],
                    self.atomElements()[self.__atom_connectivity[i][1] - 1]))
            elif self.__atom_connectivity[i][2] != 0 and self.__atom_connectivity[i][3] == 0:
                self.__element_connectivity.append('{}{}{}'.format(
                    self.atomElements()[self.__atom_connectivity[i][0] - 1],
                    self.atomElements()[self.__atom_connectivity[i][1] - 1],
                    self.atomElements()[self.__atom_connectivity[i][2] - 1]))
            else:
                self.__element_connectivity.append('{}{}{}{}'.format(
                    self.atomElements()[self.__atom_connectivity[i][0] - 1],
                    self.atomElements()[self.__atom_connectivity[i][1] - 1],
                    self.atomElements()[self.__atom_connectivity[i][2] - 1],
                    self.atomElements()[self.__atom_connectivity[i][3] - 1]))
        self.__connectivity_types, self.__connectivity_types_inverse = numpy.unique(self.__element_connectivity, return_inverse=True)
        self.__connectivity_counts = numpy.bincount(self.__connectivity_types_inverse)
        return None
    
    def __getLocalModeUserLabels(self):
        self.__local_mode_user_labels = []
        for i in range(0, len(self.__file)):
            if "Adia para name" in self.__file[i]:
                for j in range(2, self.__number_parameters + 2):
                    self.__local_mode_user_labels.append(self.__file[i + j].split()[1])
                break
        return None
    
    def numberParameters(self):
        return self.__number_parameters
    
    def localModeCharacter(self):
        return self.__local_mode_character
    
    def atomConnectivity(self):
        return self.__atom_connectivity
    
    def localModeForceConstants(self):
        return self.__local_mode_force_constants
    
    def localModeFrequencies(self):
        return self.__local_mode_frequencies
    
    def numberStretches(self):
        return self.__number_stretches

    def numberBends(self):
        return self.__number_bends

    def numberTorsions(self):
        return self.__number_torsions
    
    def localModeLabels(self):
        return self.__local_mode_labels
    
    def elementConnectivity(self):
        return self.__element_connectivity
    
    def connectivityTypes(self):
        return self.__connectivity_types
    
    def connectivityTypesInverse(self):
        return self.__connectivity_types_inverse
    
    def connectivityTypeCounts(self):
        return self.__connectivity_counts
    
    def localModeUserLabels(self):
        return self.__local_mode_user_labels
