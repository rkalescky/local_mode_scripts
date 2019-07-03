import numpy
from GeneralSupport import *
class CFOURLogFile:

    def __init__(self, inputFile):
        file_handle = open(inputFile, 'r')
        self.__file = file_handle.readlines()
        file_handle.close()
        self.__getNumberAtoms()
        self.__getCartesianCoordinates()

    def __getNumberAtoms(self):
        for i in range(0, len(self.__file)):
            if "entries found in Z-matrix " in self.__file[i]:
                self.__number_atoms = int(self.__file[i].split()[0])
        return None
    
    def __getCartesianCoordinates(self):
        self.__cartesian_coordinates = numpy.zeros(shape=(self.__number_atoms, 3))
        self.__atom_elements = []
        for i in range(0, len(self.__file)):
            if "Coordinates (in bohr)" in self.__file[i]:
                for j in range(0, self.__number_atoms):
                    line = self.__file[i + j + 3].split()
                    self.__atom_elements.append(line[0])
                    for k in range(0, 3):
                        self.__cartesian_coordinates[j][k] = float(line[k + 2])
        return None
    
    def numberAtoms(self):
        return self.__number_atoms
    
    def cartesianCoordinates(self):
        return self.__cartesian_coordinates
    
    def atomElements(self):
        return self.__atom_elements

    def printCartesianCoordintes(self):
        print("Angstrom")
        for i in range(0, self.__number_atoms):
            print('{:2s}'.format(self.__atom_elements[i])),
            for j in range(0, 3):
                print('{:12.8f}'.format(bohrToAngstrom(self.__cartesian_coordinates[i][j]))),
            print('\n'),
