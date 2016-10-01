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
	# Get the start and end dates for the week
	#startDateStr = str(request.form.get('start_date'))
	#endDateStr   = str(request.form.get('end_date'))
	#startDate    = datetime.datetime.strptime(startDateStr, '%d %B, %Y')
	#endDate      = datetime.datetime.strptime(endDateStr, '%d %B, %Y')

	# Save and then process the Excel
	#f = request.files['selectFile']
	#app.logger.info('Read in the following file - {0}'.format(f.filename))
	#saveName = datetime.datetime.now().strftime('Input_data_%Y%m%d_%H%M%S.xlsx')
        #f.save("data/"+saveName)
	#app.logger.info('Saved locally as - {0}'.format(saveName))

	# Extract the data from the Excel
	#excel           = ReadExcelFile("data/"+saveName)

	#app.logger.info('Excel file parsed for {0} and {1}'.format(salesWeek, salesChannel))

	#return render_template('submit.html', 
	#	return redirect(url_for('weekly_sales'))
	return render_template('index.html')


if __name__ == '__main__':
	handler = RotatingFileHandler('log/excel2html.log', maxBytes=50000, backupCount=1)
	format = "%(asctime)s %(levelname)-8s %(message)s"
	handler.setFormatter(logging.Formatter(format))
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host='0.0.0.0', port=1798, debug=True)
