from flask import render_template
from flask import session
from flask import make_response, send_from_directory, redirect, url_for
from flask import Flask, request, Response
from functools import wraps
import io
import os
import csv
import datetime
import re
import random
import json
import smtplib
import logging
import pickle
from src.GraphExcel import GraphExcel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import text
from sqlalchemy import exc
from logging.handlers import RotatingFileHandler

# The application setup
app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')

# The main index page
@app.route('/')
def index():
	ipAddr = request.remote_addr
	app.logger.info('HTTP GET Request from IP Address {0}'.format(ipAddr))
	return render_template('index.html')

# The route used to submit the Excel or CSV data as a file
@app.route('/submit/', methods=['POST'])
def submit():
	""" The submit function is called once the excel file has been submitted. The session
            functionality is used to pass data between pages. 
	"""
	# Save and then process the Excel
	f = request.files['selectFile']
	app.logger.info('Read in the following file - {0}'.format(f.filename))
	fileNameTokens = f.filename.split('.')
	prefix   = fileNameTokens[-1]
	hexName  = ''.join([random.choice('0123456789ABCDEF') for x in range(12)])
	fileDate = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
	saveName = '{0}_{1}.{2}'.format(hexName,fileDate,prefix)

        f.save("data/"+saveName)
	app.logger.info('Saved input file as - {0}'.format(saveName))

	# Extract the data from the Excel
	graphExcel = GraphExcel("data/"+saveName)

	rowSize = graphExcel.getRows()
	colSize = graphExcel.getCols()
	header  = graphExcel.getHeader()
	data    = graphExcel.getData()

	session['rowSize'] = rowSize 
	session['colSize'] = colSize
	session['header']  = header
	session['data']    = data

	app.logger.info('{0} rows parsed from {1}'.format(rowSize, saveName))
	# return redirect(url_for('configure'))
	return render_template('configure.html', headerList=header) 


if __name__ == '__main__':
	handler = RotatingFileHandler('log/graph_excel.log', maxBytes=50000, backupCount=1)
	format = "%(asctime)s %(levelname)-8s %(message)s"
	handler.setFormatter(logging.Formatter(format))
	handler.setLevel(logging.INFO)
	logger = logging.getLogger('graph_excel')
	app.logger.addHandler(handler)
	app.run(host='0.0.0.0', port=1798, debug=True)
