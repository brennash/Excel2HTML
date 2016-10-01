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
from bs4 import BeautifulSoup
from src.DataMart import DataMart
from src.ReadExcelFile import ReadExcelFile
from src.Calendar import Calendar
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
	remoteIPAddress = request.remote_addr
	app.logger.info('HTTP GET Request from IP Address {0}'.format(remoteIPAddress))
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
	f = request.files['selectFile']
	app.logger.info('Read in the following file - {0}'.format(f.filename))
	saveName = datetime.datetime.now().strftime('Input_data_%Y%m%d_%H%M%S.xlsx')
        f.save("data/"+saveName)
	app.logger.info('Saved locally as - {0}'.format(saveName))

	# Extract the data from the Excel
	excel           = ReadExcelFile("data/"+saveName)

	trainerList     = excel.getList('Trainer')
	fieldRepList    = excel.getList('Field Rep')
	inductionList   = excel.getList('Induction')
	trainerDays     = excel.getTotalDaysWorked('Trainer')
	trainerSalary   = excel.getTotalBasicSalary('Trainer')
	fieldRepDays    = excel.getTotalDaysWorked('Field Rep')
	fieldRepSalary  = excel.getTotalBasicSalary('Field Rep')
	inductionDays   = excel.getTotalDaysWorked('Induction')
	inductionSalary = excel.getTotalBasicSalary('Induction')
	trainerDays     = excel.getTotalDaysWorked('Trainer')
	trainerSalary   = excel.getTotalBasicSalary('Trainer')

	numTrainers     = len(trainerList)
	numFRs          = len(fieldRepList)
	numInductions   = len(inductionList)

	salesChannel    = excel.getSalesChannel()
	salesWeek       = excel.getSalesWeek()
        salesWeekStr     = salesWeek.replace(':',' ')
        salesWeekStr     = salesWeekStr.replace('k',' ')
        salesWeekStr     = salesWeekStr.replace('K',' ')
        salesWeekNumList = re.findall('\d+', salesWeekStr)
        salesWeekNum     = salesWeekNumList[0]

	app.logger.info('Excel file parsed for {0} and {1}'.format(salesWeek, salesChannel))

	# Insert the timesheets into the DataMart
	dataMart       = DataMart()
	dataMart.cleanTimesheet(salesChannel, salesWeek)
	trainerTotal   = dataMart.addTimesheetData(salesChannel, salesWeek, trainerList)
	fieldRepTotal  = dataMart.addTimesheetData(salesChannel, salesWeek, fieldRepList)
	inductionTotal = dataMart.addTimesheetData(salesChannel, salesWeek, inductionList)
	app.logger.info('Inserted {0}/{1} Trainers into GW.SFA_TSL_Timesheets for Week {2} on Channel {3}'.format(trainerTotal, numTrainers, salesWeek, salesChannel))
	app.logger.info('Inserted {0}/{1} Field Reps into GW.SFA_TSL_Timesheets for Week {2} on Channel {3}'.format(fieldRepTotal, numFRs, salesWeek, salesChannel))
	app.logger.info('Inserted {0}/{1} Inductions into GW.SFA_TSL_Timesheets for Week {2} on Channel {3}'.format(inductionTotal, numInductions, salesWeek, salesChannel))

	dataMart.closeConnection()

	calendar = Calendar()
	startDateStr = calendar.getStartDate(salesWeek).strftime('%d %B %Y')
        endDateStr   = calendar.getEndDate(salesWeek).strftime('%d %B %Y')

	# Set the session data
	session['trainerList']    = trainerList
	session['fieldRepList']   = fieldRepList
	session['inductionList']  = inductionList
	session['salesWeek']      = salesWeek
	session['salesWeekNum']   = salesWeekNum
	session['salesChannel']   = salesChannel
	session['startDate']      = startDateStr
	session['endDate']        = endDateStr



	return render_template('submit.html', 
		salesWeek=salesWeekNum,
		salesChannel=salesChannel,
		startDate=startDateStr,
		endDate=endDateStr,
		totalReps=("{:,d}".format(int(numFRs+numInductions+numTrainers))),
		totalDays=("{:,d}".format(int(trainerDays+fieldRepDays+inductionDays))),
		totalSalary=("{:,d}".format(int(trainerSalary+fieldRepSalary+inductionSalary))),
		trainerList=trainerList, trainerDays="{:,d}".format(int(trainerDays)), trainerSalary="{:,d}".format(int(trainerSalary)), numTrainers=numTrainers,
		fieldRepList=fieldRepList, fieldRepDays="{:,d}".format(int(fieldRepDays)), fieldRepSalary="{:,d}".format(int(fieldRepSalary)), numFRs=numFRs,
		inductionList=inductionList, inductionDays="{:,d}".format(int(inductionDays)), inductionSalary="{:,d}".format(int(inductionSalary)), numInductions=numInductions)

		return redirect(url_for('weekly_sales'))


if __name__ == '__main__':
	handler = RotatingFileHandler('log/excel2html.log', maxBytes=50000, backupCount=1)
	format = "%(asctime)s %(levelname)-8s %(message)s"
	handler.setFormatter(logging.Formatter(format))
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host='0.0.0.0', port=1798, debug=True)
