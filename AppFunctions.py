import DBMethods as DB
from ConfigParserM import logging
import GeneralFunctions as GF
from decimal import Decimal
import numpy as np

from math import pi


####### Plotting Parameters

# rcParams['mathtext.fontset'] = 'stix'
# rcParams['font.family'] = 'STIXGeneral'


##############################


def toSaveHistogram(Folder, Name, Array, Figure_DPI=400):
    try:
        Arr = []
        for i in range(len(Array)):
            Arr.append(float(Array[i]))
        n, bins, patches = plt.hist(Arr, 50, density=True, facecolor='b', alpha=0.75)
        plt.ylabel('Probability')
        plt.title('Histogram of ' + str(Name))
        plt.grid(True)
        Address = GF.getAddressTo(Folder, None, Name, "jpg")
        plt.savefig(Address, format='jpg', dpi=Figure_DPI, bbox_inches='tight')
        plt.clf()
        plt.close()

    except Exception as e:
        logging.exception(e)
        raise


def isNewInputDB(INFO, TableName, InputDictionary):
    try:

        # DB.createTable(INFO=INFO, TableName=TableName, arrHeaderNamesInput=InputHeader, arrHeaderNamesOutput=OutputHeader)
        hash_Database = DB.getHashofRow(INFO=INFO, TableName=TableName, ValuesDictionary=InputDictionary)
        ID_Database, rowCount_Database = DB.checkHashValue(INFO=INFO, TableName=TableName, Hash=hash_Database)

        return ID_Database, rowCount_Database

    except Exception as e:
        logging.exception(e)
        raise


def isNewArrayDB(INFO, TableName, Header, Array):
    try:
        hash_array = DB.getHashofArray(INFO=INFO, TableName=TableName, Header=Header, Array=Array)
        Hashes = DB.checkHashArray(INFO=INFO, TableName=TableName, HashArray=hash_array)
        return Hashes

    except Exception as e:
        logging.exception(e)
        raise


def uniqueList(list1):
    try:
        unique_list = []
        for x in list1:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    except Exception as e:
        logging.exception(e)
        raise


def uniqueEntry(Array):
    try:
        col = len(Array[0])
        ranges = []
        for k in range(col):
            ranges.append(uniqueList(GF.selectColumnsList(ColumnIndex=[k], List=Array)))

        return ranges
    except Exception as e:
        logging.exception(e)
        raise


def findNearest(Array, input):
    try:
        inp = Decimal(input)
        A = min(Array, key=lambda x: abs(x - inp))
        return A

    except Exception as e:
        logging.exception(e)
        raise


def findIndexNearest(Array, input):
    try:
        inp = Decimal(input)
        A = min(range(len(Array)), key=lambda i: abs(Array[i] - inp))
        return A

    except Exception as e:
        logging.exception(e)
        raise


def checkIndex(tolerance, MainIndex, max):
    try:
        up = MainIndex + tolerance
        down = MainIndex - tolerance
        if down < 0:
            down = 0
        if up > max:
            up = max
        return [up, down]


    except Exception as e:
        logging.exception(e)
        raise


def createRandomNormalArr(Center, Width, Number, digit=3):
    try:
        A = np.random.normal(Center, Width, int(Number))
        length = len(A)
        B = []
        for i in range(length):
            B.append(round(Decimal(A[i]), digit))
        return B

    except Exception as e:
        logging.exception(e)
        raise


def calcMonomerParameter(dpArray, WaveLengthArray):
    try:
        rows = len(dpArray)
        A = []
        for i in range(rows):
            A.append(Decimal(pi) * dpArray[i] / WaveLengthArray[i])

        return A

    except Exception as e:
        logging.exception(e)
        raise


def createRandomNormalArrINT(Center, Width, Number):
    try:
        A = np.random.normal(Center, Width, int(Number))
        length = len(A)
        B = []
        for i in range(length):
            B.append(round(Decimal(A[i]), 0))
        return B

    except Exception as e:
        logging.exception(e)
        raise


def findCommonIndex(*args):
    try:
        A = len(args)
        C = args[0]
        for i in range(1, A):
            C = set(args[i]) & set(C)
        return list(C)

    except Exception as e:
        logging.exception(e)
        raise


def checkRDGDBforIndexes(*args):
    try:
        A = len(args)
        C = args[0]
        for i in range(1, A):
            C = set(args[i]) & set(C)
        return list(C)

    except Exception as e:
        logging.exception(e)
        raise


def TMatrixOutputDictoArray(Dictionary):
    try:
        A = []
        A.append(Dictionary['TMatrix_ABS_CRS'])
        A.append(Dictionary['TMatrix_SCA_CRS'])
        return A

    except Exception as e:
        logging.exception(e)
        raise


def Fig_Plot_Save_Scatter_X_Linear_Y_Linear(Address, X_Array, Y_array, tickLabelStyle='sci', X_Min=None, X_Max=None, Y_Min=None, Y_Max=None, X_Label=None, Y_label=None, Plot_Title=None, label_font_size=12, Plot_Title_Size=12, Figure_DPI=1000, alpha_Y=0.3, Marker_Size=3):
    try:

        fig, ax1 = plt.subplots()
        plt.ticklabel_format(style=tickLabelStyle, axis='x', scilimits=(0, 0))
        plt.ticklabel_format(style=tickLabelStyle, axis='y', scilimits=(0, 0))

        if X_Min == None:
            X_Min = float(min(X_Array))
            X_Min = X_Min - (abs(X_Min) * 0.2)
        if X_Max == None:
            X_Max = float(max(X_Array))
            X_Max = X_Max + (abs(X_Max) * 0.2)
        if Y_Min == None:
            Y_Min = float(min(Y_array))
            Y_Min = Y_Min - (abs(Y_Min) * 0.2)
        if Y_Max == None:
            Y_Max = float(max(Y_array))
            Y_Max = Y_Max + (abs(Y_Max) * 0.2)

        ax1.scatter(X_Array, Y_array, s=7, alpha=alpha_Y)
        if X_Label != None:
            ax1.set_xlabel(X_Label, fontsize=label_font_size)
        if Y_label != None:
            ax1.set_ylabel(Y_label, fontsize=label_font_size)
        ax1.set_xlim(X_Min, X_Max)
        ax1.set_ylim(Y_Min, Y_Max)
        ax1.grid(True, which='major', axis="both", alpha=0.5)
        if Plot_Title != None:
            plt.title(Plot_Title, fontsize=Plot_Title_Size, y=1.0)
        plt.savefig(Address, format='jpg', dpi=Figure_DPI, bbox_inches='tight')
        plt.clf()
        plt.close()

    except Exception as e:
        logging.exception(e)
        raise


def corrDots(*args, **kwargs):
    corr_r = args[0].corr(args[1], 'pearson')
    corr_text = f"{corr_r:2.2f}".replace("0.", ".")
    ax = plt.gca()
    ax.set_axis_off()
    marker_size = abs(corr_r) * 10000
    ax.scatter([.5], [.5], marker_size, [corr_r], alpha=0.95, cmap="coolwarm", vmin=-1, vmax=1, transform=ax.transAxes)
    font_size = abs(corr_r) * 40 + 5
    ax.annotate(corr_text, [.5, .5, ], xycoords="axes fraction", ha='center', va='center', fontsize=font_size)


def Fig_Plot_Save_Scatterplot_Matrix(Address, Dataframe, Figure_DPI=1000):
    try:
        sns.set(style='white')
        g = sns.pairplot(Dataframe)
        g.map_lower(sns.kdeplot, cmap="GnBu", shade=True)
        g.map_diag(plt.hist, edgecolor="b")
        g.map_upper(corrDots)

        xlabels, ylabels = [], []
        for ax in g.axes[-1, :]:
            xlabel = ax.xaxis.get_label_text()
            xlabels.append(xlabel)
        for ax in g.axes[:, 0]:
            ylabel = ax.yaxis.get_label_text()
            ylabels.append(ylabel)
        for i in range(len(xlabels)):
            for j in range(len(ylabels)):
                g.axes[j, i].xaxis.set_label_text(xlabels[i])
                g.axes[j, i].yaxis.set_label_text(ylabels[j])

        plt.savefig(Address, format='jpg', dpi=Figure_DPI)
        plt.clf()
        plt.close()

    except Exception as e:
        logging.exception(e)
        raise


def checkMethodDBforTMatrixIndexes(INFO, TableName, Header, Array):
    try:

        Found = isNewArrayDB(INFO=INFO, TableName=TableName, Header=Header, Array=Array)
        Newinput = []
        OldOutput = []
        OldInput = []
        Indexes = []
        for i in range(len(Found)):
            if Found[i] == -1:
                Newinput.append(Array[i][:])
                Indexes.append(-1)
            else:
                OldOutput.append(TMatrixOutputDictoArray(DB.getOutputRowByHash(INFO=INFO, TableName=TableName, Hash=Found[i])))
                OldInput.append(Array[i][:])
                Indexes.append(1)

        return OldInput, OldOutput, Newinput, Indexes

    except Exception as e:
        logging.exception(e)
        raise


def RDGOutputDictoArray(Dictionary):
    try:
        A = []
        A.append(Dictionary['RDG_ABS_CRS'])
        A.append(Dictionary['RDG_SCA_CRS'])
        return A

    except Exception as e:
        logging.exception(e)
        raise


def checkMethodDBforRDGIndexes(INFO, TableName, Header, Array):
    try:

        Found = isNewArrayDB(INFO=INFO, TableName=TableName, Header=Header, Array=Array)
        Newinput = []
        OldOutput = []
        OldInput = []
        Indexes = []
        for i in range(len(Found)):
            if Found[i] == -1:
                Newinput.append(Array[i][:])
                Indexes.append(-1)
            else:
                OldOutput.append(RDGOutputDictoArray(DB.getOutputRowByHash(INFO=INFO, TableName=TableName, Hash=Found[i])))
                OldInput.append(Array[i][:])
                Indexes.append(1)

        return OldInput, OldOutput, Newinput, Indexes

    except Exception as e:
        logging.exception(e)
        raise


def joinArray(*args):
    try:
        rows = len(args[0])
        Arr = []
        for i in range(rows):
            A = []
            for j in range(len(args)):
                A.append(args[j][i])
            Arr.append(A)
        return Arr

    except Exception as e:
        logging.exception(e)
        raise


def joinColumnsToArray(Array, ArrtobeJoined, ColumnIndexes):
    try:
        arr = []
        rows = len(Array)
        cols = len(Array[0])
        for i in range(rows):
            A = []
            A.append(Array[i][0])
            A.append(Array[i][1])
            A.append(Array[i][2])
            A.append(Array[i][3])
            A.append(Array[i][6])
            A.append(Decimal(pi) * Array[i][5] / Array[i][4])
            for k in ColumnIndexes:
                A.append(ArrtobeJoined[i][k])
            arr.append(A)

        Name = ['Df', 'kf', 'Real_RI', 'Imag_RI', 'Np', 'Monomer_Parameter']
        return arr, Name




    except Exception as e:
        logging.exception(e)
        raise


def CreateConstantArray(Number, HowMany):
    try:
        B = []
        for i in range(HowMany):
            B.append(round(Decimal(Number), 1))
        return B

    except Exception as e:
        logging.exception(e)
        raise


def createIndexArray(start, len):
    try:
        B = []
        for i in range(start, len):
            B.append(int(i))
        return B

    except Exception as e:
        logging.exception(e)
        raise


def getPossibleArray(Array, Indexes):
    try:
        B = []
        for i in Indexes:
            B.append(Array[i])
        return B

    except Exception as e:
        logging.exception(e)
        raise


def getRandomFromArr(Array, Number):
    try:
        # uniform choice
        A = np.random.choice(Array, size=int(Number), replace=False)
        return A

    except Exception as e:
        logging.exception(e)
        raise


def getGoodIndexes(Array, Bound):
    try:
        min = Bound[0]
        max = Bound[1]
        Index = []
        rows = len(Array)
        for i in range(rows):
            if (Array[i] >= min) and (Array[i] <= max):
                Index.append(i)
        return Index

    except Exception as e:
        logging.exception(e)
        raise


def addMlinkToArray(Array, LastID):
    try:
        arrLen = len(Array)
        arrCol = len(Array[0])
        MainArr = []
        Mlink = list(range(LastID, arrLen + LastID))
        for i in range(arrLen):
            A = []
            for j in range(arrCol):
                A.append(Array[i][j])
            A.append(Mlink[i])
            MainArr.append(A)
        return MainArr

    except Exception as e:
        logging.exception(e)
        raise


def getToleratedArray(Array, Input, Tolerance, uniques):
    try:
        B = []
        index = []
        rows = len(Array)
        col = len(Array[0])
        nearest = []
        nearest_Index = []
        accepted_Index = []

        for i in range(col):
            nearest.append(findNearest(uniques[i], Input[i]))
            nearest_Index.append(findIndexNearest(uniques[i], Input[i]))

        for i in range(col):
            accepted_Index.append(checkIndex(Tolerance[i], nearest_Index[i], len(uniques[i]) - 1))

        for i in range(rows):
            k = 0
            for j in range(col):
                if (Array[i][j] >= uniques[j][accepted_Index[j][1]]) and (Array[i][j] <= uniques[j][accepted_Index[j][0]]):
                    k += 1
            if k == col:
                B.append(Array[i][:])
                index.append(i)

        return B, index
    except Exception as e:
        logging.exception(e)
        raise
