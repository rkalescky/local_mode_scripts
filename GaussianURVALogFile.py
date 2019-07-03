import numpy
from GeneralSupport import *
from GaussianLocalModeLogFile import GaussianLocalModeLogFile

class GaussianURVALogFile(GaussianLocalModeLogFile):

    def __init__(self, input_file):
        GaussianLocalModeLogFile.__init__(self, input_file)
        self.__file = self._GaussianLogFile__file
        self.__file_name_root = getFileNameRoot(input_file)
        self.__getPathPoints()
        self.__getReactionPathVectors()
        self.__getReactionPathCurvatureTotalsCartesianCoordinates()
        self.__getReactionPathCurvatureVectorsInternalCoordinates()
        self.__numberCompletedPoints()
    
    def __getPathPoints(self):
        path_points = []
        for i in range(0, len(self.__file)):
            if "IPoCou =" in self.__file[i]:
                path_points.append(self.__file[i].split()[8])
        self.__path_points = numpy.array(path_points, dtype=numpy.float)
        self.__number_path_points = self.__path_points.shape[0]
        return None

    def __getReactionPathVectors(self):
        self.__reaction_path_vectors = numpy.zeros(shape=(self.__number_path_points, self.numberParameters()))
        point = 0
        for i in range(0, len(self.__file)):
            if "dmq_n/ds" in self.__file[i]:
                for j in range(0, self.numberParameters()):
                    self.__reaction_path_vectors[point][j] = float(self.__file[i + j + 2].split('!')[8])
                point += 1
                i += self.numberParameters() + 1
        return None
    
    def __getReactionPathCurvatureTotalsCartesianCoordinates(self):
        totals = []
        for i in range(0, len(self.__file)):
            if "Total reaction path curvature" in self.__file[i]:
                totals.append(self.__file[i].split()[4])
        self.__reaction_path_curvature_totals_cartesian_coordinates = numpy.array(totals, dtype=numpy.float)
        return None
    
    def __getReactionPathCurvatureVectorsInternalCoordinatesData(self, with_db = True):
        vectors = numpy.zeros(shape=(self.__number_path_points, self.numberParameters()))
        totals = numpy.zeros(shape=(self.__number_path_points))
        point = 0
        self.__internal = False
        for i in range(0, len(self.__file)):
            if "A.Kappa =" in self.__file[i]:
                self.__internal = True
                break
        for i in range(0, len(self.__file)):
            if with_db == True and self.__internal == False:
                search_term_1 = "Total contribution (with dB)"
                search_term_2 = "Adiab.A ="
            elif with_db == False and self.__internal == False:
                search_term_1 = "Total contribution (without dB)"
                search_term_2 = "Adiab.A ="
            else:
                search_term_1 = "Total contribution (in a.u.):"
                search_term_2 = "A.Kappa ="
            
            if search_term_1 in self.__file[i]:
                totals[point] = float(self.__file[i].split()[4])
                i += 1
                k = 0
                while search_term_2 in self.__file[i]:
                    line = self.__file[i].split()
                    for j in range(2, len(line)):
                        vectors[point][k] = float(line[j])
                        k += 1
                    i += 1
                point += 1
        return totals, vectors
    
    def __getReactionPathCurvatureVectorsInternalCoordinates(self):
        self.__rpc_totals_with_db, self.__rpc_vectors_with_db = self.__getReactionPathCurvatureVectorsInternalCoordinatesData(True)
        self.__rpc_totals_without_db, self.__rpc_vectors_without_db = self.__getReactionPathCurvatureVectorsInternalCoordinatesData(False)
        return None
    
    def __numberCompletedPoints(self):
        lengths = [self.__number_path_points,
                   len(self.__reaction_path_curvature_totals_cartesian_coordinates),
                   len(self.__rpc_totals_with_db),len(self.__rpc_totals_without_db)]
        if lengths[1:] != lengths[:-1]:
            if 0 in self.__path_points and len(self.__reaction_path_curvature_totals_cartesian_coordinates) == self.__number_path_points - 1:
                self.__number_completed_points = self.__number_path_points
            else:
                print "Number of points is not consistent, please check calculation."
                self.__number_completed_points = min(lengths)
        else:
            self.__number_completed_points = self.__number_path_points
        return None
    
    def numberPathPoints(self):
        return self.__number_path_points
    
    def reactionPathVectors(self):
        return self.__reaction_path_vectors
    
    def printReactionPathVectors(self, label_type = None):
        file = open(self.__file_name_root + "_RP_Vectors.txt", 'w')
        file.write('{:>16s}'.format("s"))
        
        if label_type == None:
            labels = self.localModeUserLabels()
        else:
            labels = self.localModeLabels()
        
        for i in range(0, self.numberParameters()):
            file.write('{:>16s}'.format(labels[i]))
        file.write('\n')
        
        for i in range(0, self.__number_completed_points):
            file.write('{:16.4f}'.format(self.__path_points[i])),
            for j in range(0, self.numberParameters()):
                file.write('{:16.3f}'.format(self.__reaction_path_vectors[i][j])),
            file.write('\n'),
        file.close()
        return None
    
    def __printReactionPathCurvatureVectorsData(self, internal_totals, internal_vectors, label_type = None, with_db = True):
        if with_db == True and self.__internal == False:
            file = open(self.__file_name_root + "_RP_Curvature_Vectors_With_dB.txt", 'w')
        elif with_db == True and self.__internal == False:
            file = open(self.__file_name_root + "_RP_Curvature_Vectors_Without_dB.txt", 'w')
        else:
            file = open(self.__file_name_root + "_RP_Curvature_Vectors.txt", 'w')
        
        file.write('{:>16s}{:>16s}{:>16s}'.format("s", "Cartesian", "Internal"))
        
        if label_type == None:
            labels = self.localModeUserLabels()
        else:
            labels = self.localModeLabels()
        
        for i in range(0, self.numberParameters()):
            file.write('{:>16s}'.format(labels[i]))
        file.write('\n'),
        
        for i in range(0, self.__number_completed_points):
            file.write('{:16.4f}'.format(self.__path_points[i])),
            
            # Totals at TS are wrong, exclude. The value is given for internal coordinates, but not for cartesian.
            if self.__path_points[i] < 0.:
                file.write('{:16.4f}'.format(self.__reaction_path_curvature_totals_cartesian_coordinates[i])),
                file.write('{:16.4f}'.format(internal_totals[i])),
            elif self.__path_points[i] > 0.:
                file.write('{:16.4f}'.format(self.__reaction_path_curvature_totals_cartesian_coordinates[i - 1])),
                file.write('{:16.4f}'.format(internal_totals[i])),
            else:
                file.write('{:>16s} {:>16s}'.format("NA", "NA")),
            
            for j in range(0, self.numberParameters()):
                file.write('{:16.4f}'.format(internal_vectors[i][j])),
            file.write('\n'),
        file.close()
        return None
    
    def printReactionPathCurvatureVectors(self, label_type = None):
        self.__printReactionPathCurvatureVectorsData(self.__rpc_totals_with_db, self.__rpc_vectors_with_db, label_type, True)
        self.__printReactionPathCurvatureVectorsData(self.__rpc_totals_without_db, self.__rpc_vectors_without_db, label_type, False)
        return None
