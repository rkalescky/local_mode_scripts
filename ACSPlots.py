import sys
import os
import logging
from operator import itemgetter
import numpy
import matplotlib.pyplot
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from ACSDataFile import ACSDataFile
from LatexSupport import *
from GeneralSupport import *
if sys.platform == "darwin":
    from Foundation import *
    import objc

class ACSPlots(ACSDataFile):
    
    __color_list = ['black','red','blue','green','magenta','cyan','#800000','#008080','#000080','#000080']
    
    def __init__(self, input_file, number_plots):
        ACSDataFile.__init__(self, input_file)
        self.__frequencySeparation(number_plots)
        self.__normalModeSymmetryTypes()
        self.__normalModeSymmetryColorsAndNumbers()
        self.__file_name_root = getFileNameRoot(input_file)
    
    def __frequencyGroups(self, separation):
        local_mode_frequencies_sorted = []
        for i in range(0, self.numberModes()):
            local_mode_frequencies_sorted.append([self.localModeFrequencies()[i], i])
        local_mode_frequencies_sorted = sorted(local_mode_frequencies_sorted, key=itemgetter(0))
        frequency_groups = []
        self.__number_frequency_groups = 1
        for i in range(0, self.numberModes()):
            frequency_groups.append([local_mode_frequencies_sorted[i][1],self.__number_frequency_groups])
            if (i + 1 < self.numberModes()):
                frequency_separation = ((local_mode_frequencies_sorted[i + 1][0] - local_mode_frequencies_sorted[i][0]) /
                (local_mode_frequencies_sorted[self.numberModes() - 1][0] - local_mode_frequencies_sorted[0][0]))
                if frequency_separation >= separation:
                    self.__number_frequency_groups += 1
        self.__frequency_groups = sorted(frequency_groups, key=itemgetter(0))
        return self.__frequency_groups

    def __frequencySeparation(self, number_plots):
        for i in range(1000, 0, -1):
            self.__frequencyGroups(float(i) / 1000.0)
            if self.__number_frequency_groups >= number_plots:
                break
        return None
    
    def __normalModeSymmetryTypes(self):
        self.__symmetry_types = []
        for i in range(0, self.numberModes()):
            symmetry_Found = False
            for j in range(0, len(self.__symmetry_types)):
                if self.normalModeSymmetries()[i] == self.__symmetry_types[j]:
                    symmetry_Found = True
                    break
                else:
                    symmetry_Found = False
            if symmetry_Found == False:
                self.__symmetry_types.append(self.normalModeSymmetries()[i])
        return None

    def __normalModeSymmetryColorsAndNumbers(self):
        self.__normal_mode_symmetry_colors = []
        self.__normal_mode_symmetry_color_numbers = []
        for i in range(0, self.numberModes()):
            if len(self.__symmetry_types) <= len(self.__color_list):
                for j in range(0, len(self.__symmetry_types)):
                    if self.normalModeSymmetries()[i] == self.__symmetry_types[j]:
                        self.__normal_mode_symmetry_colors.append(self.__color_list[j])
                        self.__normal_mode_symmetry_color_numbers.append(j)
            else:
                self.__normal_mode_symmetry_colors.append('k')
        return None
    
    def frequencyGroups(self):
        return self.__frequency_groups
    
    def numberFrequencyGroups(self):
        return self.__number_frequency_groups
    
    def normalModeSymmetryColors(self):
        return self.__normal_mode_symmetry_colors
    
    def acsPlotsDataGraph(self, type_file):
        if sys.platform != "darwin":
            print "OS X is required for DataGraph file generation; Skipping."
            return None
        
        number_plots         = self.__number_frequency_groups
        script_directory     = os.path.dirname(os.path.realpath(__file__))
        data_graph_framework = script_directory + "/DataGraph.framework"
        if type_file == "intensity":
            data_graph_template  = script_directory + "/intensity_template.dgraph"
        else:
            data_graph_template  = script_directory + "/acs_template.dgraph"
        objc.loadBundle("DGController", globals(), bundle_path=objc.pathForFramework(data_graph_framework))

        acsData = NSMutableArray.arrayWithCapacity_(self.numberPoints())
        colors = NSArray.arrayWithObjects_(NSColor.blackColor(), NSColor.redColor(), NSColor.blueColor(), NSColor.greenColor(), NSColor.brownColor(), NSColor.cyanColor(), NSColor.darkGrayColor(), NSColor.grayColor(), NSColor.lightGrayColor(), NSColor.magentaColor(), NSColor.orangeColor(), NSColor.purpleColor(), NSColor.yellowColor())

        column = 0
        # self.__frequencySeparation(number_plots)
        for plot_number in range(1, number_plots + 1):

            controller = DGController.controllerWithContentsOfFile_(data_graph_template)
            
            if type_file == "intensity":
                firstPoint = 1
                acsData.addObject_(NSString.stringWithFormat_(u"%.4f", -1.00))
                acsData.addObject_(NSString.stringWithFormat_(u"%.4f", -0.05))
            else:
                firstPoint = 0
            
            for i in range(firstPoint, self.numberPoints()):
                acsData.addObject_(NSString.stringWithFormat_(u"%.4f", i * self.stepSize()))
            controller.addDataColumnWithName_type_(NSString.stringWithFormat_(u"%d", 1), u'Ascii')
            controller.dataColumnAtIndex_(1).setDataFromArray_(acsData)
            acsData.removeAllObjects()

            for i in range(0, self.numberModes()):
                column = i + 2
                
                if type_file == "intensity":
                    acsData.addObject_(NSString.stringWithFormat_(u"%.2f", self.data()[0][i]))
                    acsData.addObject_(NSString.stringWithFormat_(u"%.2f", self.data()[0][i]))
                for j in range(firstPoint, self.numberPoints()):
                    acsData.addObject_(NSString.stringWithFormat_(u"%.2f", self.data()[j][i]))
                controller.addDataColumnWithName_type_(NSString.stringWithFormat_(u"%d", column), u'Ascii')
                controller.dataColumnAtIndex_(column).setDataFromArray_(acsData)
                acsData.removeAllObjects()
    
                if self.__frequency_groups[i][1] == plot_number:
                    controller.createPlotCommand().selectXColumn_yColumn_(controller.dataColumnAtIndex_(1), controller.dataColumnAtIndex_(column))
                    controller.plotCommand_(controller.howManyDrawingCommands() - 2).setLineColor_(colors.objectAtIndex_(self.__normal_mode_symmetry_color_numbers[i]))
                    controller.plotCommand_(controller.howManyDrawingCommands() - 2).setLineWidth_(3)
            
            #controller.createGraphicCommand()
            #controller.plotCommand_(controller.howManyDrawingCommands() - 2).setGraphicFromFile_("Orbital Figures.pdf")
            #[controller addDrawingCommandWithType:@"Graphic"];
            
            controller.writeToPath_(str(self.__file_name_root) + "-" + str(plot_number) + ".dgraph")
            #controller.writeToPDF_(self.__file_name_root + "-" + str(plot_number) + ".pdf")
        
        return None
