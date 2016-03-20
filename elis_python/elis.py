#-------------------------------------------------------------------------------
# Name:        elis
# Purpose:
#
# Author:      Danil Borchevkin
#              Olga Borchevkina
#
# Created:     20.03.2016
# Copyright:   (c) Danil&Olga Borchevkin 2016
# Licence:     BSD 2-clause
#-------------------------------------------------------------------------------

import logging
import os

DATAOFFSET = 12

def PlotGraph(firstChannel, secondChannel, metaData):
    import matplotlib.pyplot as plt

    x1 = firstChannel
    x2 = secondChannel
    check = []

    for index in range(len(x1)):
        check.append(x2[index] - x1[index])

    y = range(0,len(firstChannel))

    plt.plot(x1,y)
    plt.plot(x2,y)
    plt.plot(check,y)
    plt.show()

    return None

def PlotColorBar(firstChannelData, secondChannelData, metaData):
    """
    """
    import matplotlib.pyplot as plt
    import numpy as np


    fig = plt.figure()

    axdata = np.array(firstChannelData).T
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(axdata, aspect='auto', origin='lower')
    #ax.colorbar()
    '''
    ax2data = np.array(secondChannelData).T
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.imshow(ax2data)
    '''
    plt.show()

    return None

def GetFilename(dirPath):
    filename = '0000.dat'
    return filename

def GetMetadataItemFromString(string):
    return string[string.find("\t") + 1 : string.find("\n")].strip()

def ParseChannelDataFromString(datastring):
    firstChannelItem = 0
    secondChannelItem = 0

    logging.debug("Parse datastring >{0}".format(datastring))

    #Delimeters indexes
    firstDelimeterIndex = datastring.find('\t')
    secondDelimeterIndex = datastring.find('\t', firstDelimeterIndex + 1)

    try:
        firstChannelItem = int(datastring[0 : firstDelimeterIndex])
        secondChannelItem = int(datastring[firstDelimeterIndex + 1 : secondDelimeterIndex])
    except Exception as e:
        logging.error(e)

    return firstChannelItem, secondChannelItem

def ImportDataFromFile(filename):
    '''
    Import all data from datafile and return it into:
        - lists firstChannel and secondChannel
        - metadata in dictionary metaData

    (str) -> (firstChannel, secondChannel, metaData)
    '''
    buffer = []
    firstChannel = []
    secondChannel = []
    metaData = {"version" : "",
                   "type" : "",
                   "azimut" : 0,
                   "exceed" : 0,
                   "alpha" : 0,
                   "quantityOfCycles" : 0,
                   "quantityOfStrobes" : 0,
                   "strobe" : 0,
                   "delay" : 0,
                   "timeBegin" : "",
                   "timeEnd" : ""}

    #Open file
    datafile = open(filename, 'r')

    #Read file to buffer list
    for line in datafile:
        buffer.append(line)

    # from DATAOFFSET starts data lines. Read it into corresponding lists
    for dataStringIndex in range(DATAOFFSET, len(buffer)):
        if (buffer[dataStringIndex].startswith('\n')):
            break
        else:
            first, second = ParseChannelDataFromString(buffer[dataStringIndex])
            firstChannel.append(first)
            secondChannel.append(second)

    # Read metada from buffer
    metaData["version"] = GetMetadataItemFromString(buffer[0])
    metaData["type"] = GetMetadataItemFromString(buffer[1])
    metaData["azimut"] = int(GetMetadataItemFromString(buffer[2]))
    metaData["exceed"] = int(GetMetadataItemFromString(buffer[3]))
    metaData["alpha"] = int(GetMetadataItemFromString(buffer[4]))
    metaData["quantityOfCycles"] = int(GetMetadataItemFromString(buffer[5]))
    metaData["quantityOfStrobes"] = int(GetMetadataItemFromString(buffer[6]))
    metaData["strobe"] = int(GetMetadataItemFromString(buffer[7]))
    metaData["delay"] = int(GetMetadataItemFromString(buffer[8]))
    metaData["timeBegin"] = GetMetadataItemFromString(buffer[9])
    metaData["timeEnd"] = GetMetadataItemFromString(buffer[10])

    return firstChannel, secondChannel, metaData

def GetDataOfStrobeFromFile(filename, strobe):

    dataOfStrobe ={"firstChannel": 0,
                    "secondChannel": 0,
                    "timeBegin": 0,
                    "strobNo": strobe}

    strobe -= 1

    f, s, m = ImportDataFromFile(filename)

    dataOfStrobe["firstChannel"] = f[strobe]
    dataOfStrobe["secondChannel"] = s[strobe]
    dataOfStrobe["timeBegin"] = m["timeBegin"]
    dataOfStrobe["strobNo"] = strobe

    return dataOfStrobe

def GetListOfAllFilesInFolder(path):
    '''
    '''
    files = []

    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name.endswith(".dat"):
                files.append(name)

    return files

def main():

    logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)

    summaryFirstChannel = []
    summarySecondChannel = []
    summaryMetaData = []


    files = GetListOfAllFilesInFolder(".\\")

    for f in files:
        first, second, metadata = ImportDataFromFile(f)
        summaryFirstChannel.append(first)
        summarySecondChannel.append(second)
        summaryMetaData.append(metadata)

    #print summaryFirstChannel
    PlotColorBar(summaryFirstChannel, summarySecondChannel, summaryMetaData)

    #PlotGraph(f,s,m)

    return None

if __name__ == '__main__':
    main()
