#################################################################################################x
# Excel2HTML provides a handy way of converting a provided CSV or Excel file into a NVD3.js 	#
# graph. The graph data itself is completely inline and links to publicly available JS 		#
# and CSS libraries. 										#
#												#
#												#
#												#
# Author: Shane Brennan										#
# Date: 20160926										#
# Version: 0.1											#
#################################################################################################


#!/usr/bin/env python
import csv
import sys
import os
import datetime
import re
import datetime
import openpyxl
from optparse import OptionParser

class Excel2HTML:

	def __init__(self, verbose, inputFilename):
		self.verbose = verbose
		
		if '.csv' in inputFilename[-4:].lower():
			return self.processCSV(inputFile)
		elif '.xls' in inputFilename[-4:].lower():
			return self.processExcel(inputFile)
		elif '.xlsx' in inputFilename[-5:].lower():
			return self.processExcel(inputFile)
		else:
			print 'Require valid Excel or CSV input File'
			return None

	def processCSV(self, inputFile):
		return 'test'

	def processExcel(self, inputFile):
		return 'test'

def main(argv):
	parser = OptionParser(usage="Usage: Excel2HTML <input-filename>")

        parser.add_option("-v", "--verbose",
                action="store_true",
                dest="verboseFlag",
                default=False,
                help="Verbose output from the script")

	(options, filename) = parser.parse_args()

	if len(filename) != 1 or not os.path.isfile(filename[0]) :
		print parser.print_help()
		exit(1)

	excel2HTML = Excel2HTML(options.verboseFlag, filename[0])
	print excel2HTML
		
if __name__ == "__main__":
    sys.exit(main(sys.argv))
