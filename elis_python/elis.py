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


def PlotGraph(firstChannel, secondChannel, metaData):

    return None

def GetFilename(dirPath):
    filename = ''
    return filename

def ParseChannelDataFromString(datastring):
    firstChannelItem = 0
    secondChannelItem = 0

    #Delimeters indexes
    firstDelimeterIndex = datastring.find('\t')
    secondDelimeterIndex = datastring.find('\t', firstDelimeterIndex + 1)

    firstChannelItem = int(datastring[0 : firstDelimeterIndex])
    secondChannelItem = int(datastring[firstDelimeterIndex + 1 : secondDelimeterIndex])

    return firstChannelItem, secondChannelItem

def ImportDataFromFile(filename):
    buffer = []
    firstChannel = []
    secondChannel = []
    metaData = {}

    #Open file
    datafile = open(filename, 'r')

    #Read file to buffer list
    for line in datafile:
        buffer.append(line)

    # from buffer[12] starts data lines
    for dataStringIndex in range(12, len(buffer) - 2):
        first, second = ParseChannelDataFromString(buffer[dataStringIndex])
        firstChannel.append(first)
        secondChannel.append(second)

    return firstChannel, secondChannel, metaData

def main():
    f, s, m = ImportDataFromFile(GetFilename(''))
    print m

    return None

if __name__ == '__main__':
    main()
