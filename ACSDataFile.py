import numpy
import math
from operator import itemgetter
import sys
import logging

class ACSDataFile:

    def __init__(self, input_file):
        file_handle = open(input_file, 'r')
        self.__file = file_handle.readlines()
        file_handle.close()
        self.__getNumberPointsAndModes()
        self.__getACSData()
        self.__getNormalModeSymmetries()

    def __getNumberPointsAndModes(self):
        
        for i in range(0, len(self.__file)):
            if "Freq." in self.__file[i]:
                self.__step_size = math.fabs(float(self.__file[i + 3].split()[0]) - float(self.__file[i + 4].split()[0]))
                self.__number_points = int(1. / self.__step_size)
                self.__number_modes = len(self.__file[i + 3].split()) - 1
                break
            elif "IR Int." in self.__file[i]:
                self.__number_points = int(1. / math.fabs(float(self.__file[i + 3].split()[0]) - float(self.__file[i + 4].split()[0])))
                self.__number_modes = len(self.__file[i + 3].split()) - 1
                break
        self.__number_points += 2
        
        logging.debug("Number of ACS Points: %d", self.__number_points)
        logging.debug("Number of ACS Modes: %d", self.__number_modes)
        
        return None

    def __getACSData(self):
        acs_offset = 5
        self.__acs_data = numpy.zeros(shape=(self.__number_points, self.__number_modes))
        for i in range(0, self.__number_points):
            for j in range(0, self.__number_modes):
                self.__acs_data[i][j] = float(self.__file[(self.__number_points - i - 1) + acs_offset].split()[j + 1])
                
        # logging.debug(self.__printACSData())
        
        return None
        
    def __getNormalModeSymmetries(self):
        self.__normal_mode_symmetries = []
        for i in range(0, len(self.__file)):
            if "Symm." in self.__file[i]:
                for j in range(0, self.__number_modes):
                    self.__normal_mode_symmetries.append(str(self.__file[i].split()[j + 1]))
                break
        
        logging.debug("ACS Normal Mode Symmetries: %s", self.__normal_mode_symmetries)
        
        return None
    
    def __printACSData(self):
        print "ACS Data:"
        for i in range(0, self.__number_points):
            for j in range(0, self.__number_modes):
                print self.__acs_data[i][j], " ",
            print "\n",
        
        return None
    
    def stepSize(self):
        return self.__step_size
    
    def numberPoints(self):
        return self.__number_points
    
    def numberModes(self):
        return self.__number_modes

    def data(self):
        return self.__acs_data

    def localModeFrequencies(self):
        return self.__acs_data[0]

    def normalModeFrequencies(self):
        return self.__acs_data[self.__number_points - 1]
    
    def normalModeSymmetries(self):
        return self.__normal_mode_symmetries
