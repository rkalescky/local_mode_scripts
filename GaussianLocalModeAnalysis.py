import numpy
import matplotlib.pyplot
import math
from GeneralSupport import *
from GaussianLocalModeLogFile import GaussianLocalModeLogFile
from LatexSupport import *
from mimic_alpha import colorAlpha_to_rgb
from subprocess import call

class GaussianLocalModeAnalysis(GaussianLocalModeLogFile):

    def __init__(self, input_file):
        GaussianLocalModeLogFile.__init__(self, input_file)
        self.__file_name_root = getFileNameRoot(input_file)

    def localModeDecompositionPlot(self, highlight = numpy.array([-1, -1])):
        
        # Red, Green, Blue, Purple, Cyan, OrangeRed, SlateGray, Pink, Brown, DarkGreen, DarkBlue, Orange
        colors = [(1.,0.,0.),(0.,1.,0.),(0.,0.,1.),(0.414,0.,0.430),(0.211,0.727,0.727),(0.684,0.156,0.),
                  (0.281,0.332,0.375),(0.363,0.168,0.09),(0.938,0.,0.324),(0.324,0.145,0.),
                  (0.047,0.152,0.),(0.,0.,0.328),(0.938,0.109,0.)]
        
        alpha = []
        for i in range(0, self.numberModes()):
            count = 0
            for j in range(0, i):
                if self.elementConnectivity()[i] == self.elementConnectivity()[j]:
                    count += 1
            alpha.append((1. - (float(count) / float(self.connectivityTypeCounts()[self.connectivityTypesInverse()[i]]) / 2.),))
        
        if self.numberModes() >= 50:
            sizeOfFont = 12
            labelFontSize = 18
        elif self.numberModes() >= 60:
            sizeOfFont = 9
            labelFontSize = 12
        else:
            sizeOfFont = 18
            labelFontSize = 24
        
        legendFont = matplotlib.font_manager.FontProperties(family='Helvetica', style='normal', size=sizeOfFont,
            weight='normal', stretch='normal')
        fontProperties = {'family' : 'sans-serif', 'sans-serif':['Helvetica'], 'weight' : 'normal', 'size' : sizeOfFont}
        matplotlib.rc('font', **fontProperties)
        matplotlib.rc('text', usetex=True)
        matplotlib.rcParams['text.latex.preamble']=[r'\usepackage{color}', r'\boldmath']
        figure = matplotlib.pyplot.figure(1, figsize=(20,12))
        decomposition_plot = figure.add_subplot(111)
        indices = numpy.arange(self.numberModes())
        width = 0.9
        plotPart = []
        plotPartBottom = numpy.zeros(shape=(self.numberModes()))
        firstStretch = True
        firstBend = True
        firstTorsion = True
        fade = 1.25
        for i in range(0, self.numberModes()):
            if i > 0:
                plotPartBottom = plotPartBottom + self.localModeCharacter()[i - 1]
            
            color = colorAlpha_to_rgb(colors[self.connectivityTypesInverse()[i]], alpha[i])
            
            if highlight.all() != -1:
                for j in range(0,len(highlight)):
                    if i == highlight[j] - 1:
                        color = (1.,1.,0.)
                        break

            plotPart.append(decomposition_plot.bar(indices, self.localModeCharacter()[i], width,
                color=(color), bottom=plotPartBottom))
        decomposition_plot.tick_params(direction='out')
        decomposition_plot.xaxis.set_tick_params(labeltop='on', labelbottom='off')
        plotAxis = [-0.25,float(self.numberModes())+0.25,0,100]
        decomposition_plot.axis(plotAxis)
        decomposition_plot.set_yticks(numpy.arange(0,100.1,10))
        decomposition_plot.set_ylabel('Local Mode Character [\%]', size=labelFontSize, weight='bold')
        if self.numberModes() <= 20:
            decomposition_plot.text(float(self.numberModes())/2.,-15,'Normal Mode $\mu$',horizontalalignment='center', size=labelFontSize, weight='bold')
        else:
            decomposition_plot.text(float(self.numberModes())/2.,-17,'Normal Mode $\mu$',horizontalalignment='center', size=labelFontSize, weight='bold')
        # figure.suptitle(str(self.__file_name_root).replace('_', '\_'))
        legendColumnsToHave = int(math.ceil(float(self.numberModes()) / 40.))
        decomposition_plot.legend(self.localModeLabels(), loc=2, bbox_to_anchor=(1.0, 1.0), labelspacing=0.01,
            handlelength=1,handletextpad=0.25, ncol=legendColumnsToHave)
        plotPartBottom = numpy.zeros(shape=(self.numberModes()))
        for i in range(0, self.numberModes()):
            if i > 0:
                plotPartBottom = plotPartBottom + self.localModeCharacter()[i - 1]
            for j in range(0, self.numberModes()):
                if self.localModeCharacter()[i][j] >= 5.0:
                    color = 'w'
                    if highlight.all() != -1:
                        for k in range(0,len(highlight)):
                            if i == highlight[k] - 1:
                                color = 'k'
                                break
                    decomposition_plot.text(j+0.45,plotPartBottom[j]+(self.localModeCharacter()[i][j]/2),str(self.localModeCharacter()[i][j]),horizontalalignment='center',verticalalignment='center',color=color)
        for i in range(0, self.numberModes()):
            if self.numberModes() <= 20:
                decomposition_plot.text(i+0.5, -4.0, latexSymmetry(self.normalModeSymmetries()[i]),
                   size=(labelFontSize - 3),horizontalalignment='center', weight='bold')
                decomposition_plot.text(i+0.3,-7.0,str(int(round(self.normalModeFrequencies()[i]))),
                    horizontalalignment='left',rotation=-45., size=labelFontSize, weight='bold')
            else:
                decomposition_plot.text(i+0.1,-4.0,latexSymmetry(self.normalModeSymmetries()[i], 'blue') + " " + str(int(round(self.normalModeFrequencies()[i]))),
                    horizontalalignment='left',rotation=-45., size=labelFontSize, weight='bold')
        a = matplotlib.pyplot.gca()
        a.set_xticklabels(a.get_xticks(), fontProperties, size=labelFontSize, weight='bold')
        a.set_yticklabels(a.get_yticks(), fontProperties, size=labelFontSize, weight='bold')
        matplotlib.pyplot.xticks(indices+width/2., numpy.arange(1,self.numberModes()+1,1))
        figure.savefig(str(self.__file_name_root) + ".eps", bbox_inches='tight')
        matplotlib.pyplot.close()
        try:
            call("ps2pdf -dEPSCrop " + str(self.__file_name_root) + ".eps", shell=True)
        except:
            print "Decomposition bar diagram file could not automatically be converted from EPS to PDF."
            print "Preview on a Mac will automatically make a PDF."
            print "ps2pdf -dEPSCrop file.eps can be used to make a PDF."
        return None
    
    def decompositionTable(self):
        
        decomposition_table_file = open(self.__file_name_root + "_Decomposition" + ".tex", 'w')
        decomposition_table_file.write("\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{lscape}\n\n\\begin{document}\n\n")
        decomposition_table_file.write("\\begin{landscape}\n")
        decomposition_table_file.write("\\begin{table}\n")
        decomposition_table_file.write("\\begin{tabular}{l l}\n")
        decomposition_table_file.write("\\hline\\hline\\\\\n")
        decomposition_table_file.write("\\(\\mu\\) & Characterization of modes \\(\\omega_{\\mu}\\) in terms of modes \\(\\omega^{a}\\)  \\\\\n")
        decomposition_table_file.write("\\\\\\hline\\\\\n")
        for i in range(self.numberModes() - 1, -1, -1):
            temp = []
            temp_index = []
            for j in range(0, self.numberModes()):
                if self.localModeCharacter()[j, i] >= 5.:
                    temp.append(self.localModeCharacter()[j, i])
                    temp_index.append([self.localModeCharacter()[j, i], j])
            temp, temp_inverse = numpy.unique(temp, return_inverse=True)
            temp_count = numpy.bincount(temp_inverse)
            temp_index = sorted(temp_index[:])
            total_percentages = []
            line = []
            index = 0
            for k in range(0, len(temp)):
                total_percentages.append(temp[k] * float(temp_count[k]))
                string_temp = '{0:.1f}'.format(temp[k] * float(temp_count[k])) + "\% "
                for l in range(0, temp_count[k]):
                    if temp_count[k] > 1 and l == 0:
                        string_temp += "("
                    string_temp += self.localModeLabels()[temp_index[index][1]]
                    if temp_count[k] > 1 and l == temp_count[k] - 1:
                        string_temp += ")"
                    string_temp += ", "
                    index += 1
                line.append(string_temp)
            order = numpy.argsort(total_percentages)
            line_ordered = str(i + 1) + " & "
            for i in range(len(line) - 1, -1, -1):
                line_ordered += line[order[i]]
            line_ordered = line_ordered[:-2] + " \\\\\n"
            decomposition_table_file.write(line_ordered)
        decomposition_table_file.write("\\\\\\hline\\hline\\\\\n")
        decomposition_table_file.write("\\end{tabular}\n")
        decomposition_table_file.write("\\end{table}\n")
        decomposition_table_file.write("\\end{landscape}\n")
        decomposition_table_file.write("\n\\end{document}\n")
        decomposition_table_file.close()
