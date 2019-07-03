import numpy
import matplotlib.pyplot
import math
from operator import itemgetter

class GaussianLogFile:

    def __init__(self, inputFile):
        file_handle = open(inputFile, 'r')
        self.__file = file_handle.readlines()
        file_handle.close()
        self.__getNumberCenters()
        self.__getNumberAtoms()
        self.__getMoleculeSymmetry()
        self.__getAtomElements()

    def __getNumberCenters(self):
        self.__number_centers = 0
        structure_start = 0
        structure_end = 0
        for i in range(0, len(self.__file)):
            if "Charge =" in self.__file[i]:
                structure_start = i
                for j in range(i + 1, len(self.__file)):
                    if len(self.__file[j].split()) == 0 or self.__file[j].lower().find("variables") != -1:
                        structure_end = j
                        break
                break
        self.__number_centers = structure_end - structure_start - 1
        return None

    def __getNumberAtoms(self):
        self.__number_atoms = 0
        for i in range(0, len(self.__file)):
            if "orientation:" in self.__file[i]:
                while "-----" not in self.__file[i + self.__number_atoms + 5]:
                    self.__number_atoms += 1
                break
        return None

    def __getMoleculeSymmetry(self):
        for i in range(0, len(self.__file)):
            if "Full point group" or "Framework group" in self.__file[i]:
                temp = self.__file[i].split()
                self.__molecule_symmetry = temp[len(temp) - 1].split()[0]
                break
        return None

    def __getAtomElements(self):
        self.__atom_elements = []
        for i in range(0, len(self.__file)):
            if "Distance matrix" in self.__file[i]:
                for j in range(2, self.__number_atoms + 2):
                    self.__atom_elements.append(self.__file[i + j].split()[1])
                break
        return None
    
    def numberCenters(self):
        return self.__number_centers
    
    def numberAtoms(self):
        return self.__number_atoms
    
    def moleculeSymmetry(self):
        return self.__molecule_symmetry
    
    def atomElements(self):
        return self.__atom_elements
