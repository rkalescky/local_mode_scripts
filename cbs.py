from sys          import argv
from math         import exp
from numpy        import loadtxt, arange, array, dot
from numpy.linalg import inv

def printHelp():
    instructions = ("Usage     : cbs n data_file m\n"
                    "n         : \"2\" or \"3\" for two- or three-point CBS respectively\n"
                    "data_file : Input file with each line having values of increasing basis set quality\n"
                    "             e.g. VDZ VTZ VQZ values\n"
                    "m         : Cardinal number of the lowest quality basis set\n"
                    "             e.g. \"2\" for VDZ or \"3\" for VTZ\n"
                   )
    print instructions

def twoPointCBS(file, m0):
    M   = loadtxt(file)
    pm0 = pow(m0    , 3)
    pm1 = pow(m0 + 1, 3)

    for i in range(0, M.shape[0]):
        print '{0:.6f}'.format((pm0 * M[i][0] - pm1 * M[i][1]) / (pm0 - pm1))

def threePointCBS(file, m0):
    M     = loadtxt(file)
    m     = arange(m0, m0 + 3)
    A_Inv = inv(array([(1, exp(-m[0]), exp(-pow(m[0], 2))),
                       (1, exp(-m[1]), exp(-pow(m[1], 2))),
                       (1, exp(-m[2]), exp(-pow(m[2], 2)))]))

    for i in range(0, M.shape[0]):
        print '{0:.6f}'.format(dot(A_Inv, M[i,:])[0])

if len(argv) == 4:
    if argv[1] == "2":
        twoPointCBS(argv[2], int(argv[3]))
    elif argv[1] == "3":
        threePointCBS(argv[2], int(argv[3]))
    else:
        printHelp()
else:
    printHelp()