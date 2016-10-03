#################################################################################################
#												#
#												#
# Author: Shane Brennan										#
# Date: 20160928										#
# Version: 0.1											#
#################################################################################################


#!/usr/bin/env python
import csv
import sys
import os
import datetime
import random
import re
import datetime
import logging
import json

class GraphGenerator:

	def __init__(self, rowSize, colSize, header, dataList, chartType, chartColourList):
		self.rowSize         = rowSize
		self.colSize         = colSize
		self.header          = header
		self.dataList        = dataList
		self.chartType       = chartType
		self.chartColourList = chartColourList

	def getHTML(self):
		for index, seriesName in enumerate(self.header):
			# Ignore the x-axis series
			if index > 0:
				print self.getJSON(seriesName)

	def getJSON(self, seriesName):
		seriesIndex          = self.getSeriesIndex(seriesName)
		seriesColour         = self.chartColourList[seriesIndex]
		outputList           = []
		newListDict          = {}
		newListDict['key']   = seriesName
		newListDict['color'] = '#{0}'.format(seriesColour)
		newListValues        = []
		for row in self.dataList:
			element      = {}
			element['x'] = row[0]
			element['y'] = row[seriesIndex]
			newListValues.append(element)
		newListDict['values'] = newListValues
		jsonStr = json.dumps(newListDict, sort_keys=True, indent=4, separators=(',', ': '))
		return jsonStr
	
	def getSeriesIndex(self, seriesName):
		for index,element in enumerate(self.header):
			if element == seriesName:
				return index
		return -1

	def getRandomColour(self):
		digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
		randomColour = ''
		for x in xrange(0,6):
			index = random.randint(0,15)
			randomColour += digits[index]
		return randomColour


def main(argv):
	header   = ['Date','Series1','Series2']
	row1     = [ 20161001, 100.32, 79.3]
	row2     = [ 20161002, 97.42, 75.9]
	row3     = [ 20161003, 105.85, 64.4]
	dataList = []
	dataList.append(row1)
	dataList.append(row2)
	dataList.append(row3)
	colourList = ['8a8a8a','434343']
	grapher = GraphGenerator(3,3,header,dataList,'stackedBarChart',colourList)
	print grapher.getHTML()
		
if __name__ == "__main__":
    sys.exit(main(sys.argv))
