from __future__ import print_function
import sys
import numpy
import matplotlib.pyplot
import math
from decimal import *
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from ACSPlots import ACSPlots
from GaussianLocalModeAnalysis import GaussianLocalModeAnalysis
from LatexSupport import *
from FrequencySupport import *
from GeneralSupport import *

class ACSAnalysis(ACSPlots, GaussianLocalModeAnalysis):

    def __init__(self, gaussian_local_mode_log_file, acs_data_file, number_plots):
        ACSPlots.__init__(self, acs_data_file, number_plots)
        GaussianLocalModeAnalysis.__init__(self, gaussian_local_mode_log_file)
        self.__getDataArrangement()
        self.__file_name_root = getFileNameRoot(gaussian_local_mode_log_file)
        self._ACSPlots__file_name_root = self.__file_name_root
        self._GaussianLocalModeAnalysis__file_name_root = self.__file_name_root
    
    def __roundDecimal(self, x):
        return Decimal(x).quantize(Decimal('.001'), rounding=ROUND_HALF_UP).quantize(Decimal('.1'), rounding=ROUND_HALF_UP)
    
    def __roundInteger(self, x):
        return Decimal(x).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
    
    def __getDataArrangement(self):
        self.__data_arrangement =  numpy.zeros(shape=(self.numberModes(), 2), dtype=numpy.int)
        self.__data_arrangement[:, 0] = numpy.argsort(ACSPlots.localModeFrequencies(self))
        self.__data_arrangement[:, 1] = numpy.argsort(GaussianLocalModeAnalysis.localModeFrequencies(self))
        self.__data_arrangement = self.__data_arrangement[numpy.argsort(self.__data_arrangement[:, 0])]
        
    def analysisTable(self):
        acs_table_file = open(str(self.__file_name_root) + ".tex", 'w')
        acs_table_file.write("\\documentclass{article}\n\\usepackage{amsmath}\n\n\\begin{document}\n\n")
        acs_table_file.write("\\begin{table}\n")
        acs_table_file.write("\\begin{tabular}{l l r r l r r r}\n")
        acs_table_file.write("\\hline\\hline\\\\\n")
        acs_table_file.write("\\(\\mu\\) & Sym. & \\(\\omega_{\\mu}\\) & \\# & Param. & \\(k^{a}\\) & \\(\\omega^{a}\\) & \\(\\omega_{\\text{coup}}\\) \\\\ & & [cm\\textsuperscript{-1}] & & & [mdyn \\AA\\textsuperscript{-1}]\\textsuperscript{a} & [cm\\textsuperscript{-1}] & [cm\\textsuperscript{-1}] \\\\\n")
        acs_table_file.write("\\\\\\hline\\\\\n")
        for i in range(self.numberModes() - 1, -1, -1):
            n = self.__data_arrangement[i][1]
            text = (str(i + 1) + " & " + str(latexSymmetry(self.normalModeSymmetries()[i])) + " & " +
                '{0:.0f}'.format(self.normalModeFrequencies()[i]) + " & " +
                str(n + 1) + " & " +
                str(self.localModeLabels()[n]) + " & " +
                '{0:.3f}'.format(self.localModeForceConstants()[n]) + " & " +
                '{0:.0f}'.format(self.__roundInteger(self.localModeFrequencies()[i])) + " & " +
                '{0:.0f}'.format(self.__roundInteger(couplingFrequency(self.normalModeFrequencies()[i], self.localModeFrequencies()[i]))) + " \\\\\n")            
            acs_table_file.write(text)
        acs_table_file.write("\\\\\\hline\\\\\n")
        acs_table_file.write("\\multicolumn{2}{l}{ZPE [kcal/mol]:} & " + '{0:.2f}'.format(zpe(self.normalModeFrequencies())) + " & & & & " + '{0:.2f}'.format(zpe(self.localModeFrequencies())) + " & " + '{0:.2f}'.format(couplingFrequency(zpe(self.normalModeFrequencies()), zpe(self.localModeFrequencies()))) + " \\\\\n")
        acs_table_file.write("\\\\\\hline\\hline\\\\\n")
        acs_table_file.write("\\end{tabular}\n")
        acs_table_file.write("\\end{table}\n")
        acs_table_file.write("\n\\end{document}\n")
        acs_table_file.close()
    
    def acsPlots(self):
        for plot_number in range(1, self.numberFrequencyGroups() + 1):
            
            matplotlib.rcParams['xtick.direction'] = 'out'
            matplotlib.rcParams['ytick.direction'] = 'out'
            figure = matplotlib.pyplot.figure(1, figsize=(10,6))
            acs = figure.add_subplot(111)

            for i in range(0, self.numberModes()):
                if self.frequencyGroups()[i][1] == plot_number:
                    acs.plot(numpy.arange(0, 1 + self.stepSize(), self.stepSize()), numpy.transpose(self.data())[i], linewidth=1., color=self.normalModeSymmetryColors()[i])
            acs.set_xlabel("Scaling Factor \(\lambda\)")
            acs.set_ylabel("Local Mode Frequenices \(\omega_{a}\)[cm\(^{-1}\)]")
            acs.text(1.01, ((matplotlib.pyplot.ylim()[1] - matplotlib.pyplot.ylim()[0]) / 2) + matplotlib.pyplot.ylim()[0],
                "Normal Mode Frequencies \(\omega_{\mu}\)[cm\(^{-1}\)]", rotation='vertical', verticalalignment='center')
            figure.suptitle(str(self.__file_name_root).replace('_', '\_'))

            # Generate local mode labels
            deltaValue = 0.06
            i = 0
            while i < self.numberModes():
                delta = 0.
                average = 0.
                text = ""
                j = 0
                while delta <= deltaValue:
                    if j >= 1:
                        text = text + ","
                    text = text + "\(\omega_{a}\)(" + str(self.__data_arrangement[i + j][1] + 1) + ")"
                    average += self.localModeFrequencies()[i + j]
                    j += 1
                    if j + i >= self.numberModes():
                        break
                    else:
                        delta = ((self.localModeFrequencies()[i + j] -  self.localModeFrequencies()[i]) /
                            (matplotlib.pyplot.ylim()[1] - matplotlib.pyplot.ylim()[0]))
                average = average / j
                if self.frequencyGroups()[i][1] == plot_number:
                    # if (i + 1) == (i + j):
                    #     text = text = "\(\omega_{a}\)(" + str(i + 1) + ")"
                    # else:
                    #     text = "\(\omega_{a}\)(" + str(i + 1) + "-" + str(i + j) + ")"
                    acs.text(-0.14, average, text, verticalalignment='center', horizontalalignment='right')
                i = i + j

            # Generate normal mode labels
            i = 0
            while i < self.numberModes():
                delta = 0.
                average = 0.
                text = ""
                j = 0
                while delta <= deltaValue:
                    if j >= 1:
                        text = text + ","
                    text = text + "\(\omega_{" + str(i + j + 1) + "}\)(" + latexSymmetry(self.normalModeSymmetries()[i + j]) + ")"
                    average += self.normalModeFrequencies()[i + j]
                    j += 1
                    if j + i >= self.numberModes():
                        break
                    else:
                        delta = ((self.normalModeFrequencies()[i + j] -  self.normalModeFrequencies()[i]) /
                            (matplotlib.pyplot.ylim()[1] - matplotlib.pyplot.ylim()[0]))
                average = average / j
                if self.frequencyGroups()[i][1] == plot_number:
                    acs.text(1.06, average, text, verticalalignment='center', horizontalalignment='left')
                i = i + j
            
            matplotlib.pyplot.xlim([0,1])
            acs.xaxis.set_major_locator(MaxNLocator(10))
            acs.xaxis.set_minor_locator(MaxNLocator(100))
            acs.yaxis.set_major_locator(MaxNLocator(10))
            acs.yaxis.set_minor_locator(MaxNLocator(100))
            acs.yaxis.set_major_formatter(FormatStrFormatter('%0.0f'))

            sizeOfFont = 18
            fontProperties = {'family' : 'sans-serif', 'sans-serif':['Helvetica'], 'weight' : 'normal', 'size' : sizeOfFont}
            matplotlib.rc('font', **fontProperties)
            matplotlib.rc('text', usetex=True)
            a = matplotlib.pyplot.gca()
            a.set_xticklabels(a.get_xticks(), fontProperties)
            #a.set_yticklabels(a.get_yticks(), fontProperties)

            figure.savefig(str(self.__file_name_root) + "-" +str(plot_number)+".pdf", bbox_inches='tight')
            matplotlib.pyplot.close()
    
