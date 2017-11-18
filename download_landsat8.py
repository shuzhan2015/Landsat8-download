#!/usr/bin/env python

#Example Usage:
#           ./download_landsat8.py --path 22 --row 39 --date 20170401
# or        ./download_landsat8.py -p 22 -r 39 -d 20170401
# or   if path and row are specified in the config file, then ./download_landsat8.py -d 20170401
# or   if the date argument is omitted, the latest date available will be downloaded: ./download_landsat8.py -p 22 -r 39

#Written by Shuzhan Fan on 05/29/2016

import sys
import os
from ConfigParser import SafeConfigParser
from datetime import datetime
from subprocess import Popen, PIPE
import re
import logging
import tarfile
import glob
import argparse

def get_config(file_name):
	parser = SafeConfigParser()
	parser.read(file_name)
	return parser

def parse_path_row(path, row):
	if len(path) == 2:
		path = '0' + path
	if len(row) == 2:
		row = '0' + row
	return path, row

def search_latest(path, row):
	'''
		This method will search for the latest date available in the directory and return the latest date object.
	'''
	path, row = parse_path_row(path, row)
	path_str = 'gs://earthengine-public/landsat/L8/' + path + '/' + row
	p = Popen('gsutil ls '+path_str, stdout=PIPE, stderr=PIPE, shell=True)
	stdout = p.stdout.read()
	stderr = p.stderr.read()
	if stderr:
		logger.error(stderr)
		sys.exit()
	if stdout:
		data_path_list = stdout.split('\n')
		#the last item is an empty string
		data_path_latest = data_path_list[-2]
		#e.g. LC80220392016137LGN00.tar.bz
		data_latest = data_path_latest.split('/')[-1]
		#e.g. 2016137
		date_str = data_latest[9:16]
		dobj = datetime.strptime(date_str, '%Y%j')
		return dobj

def parse_date(date):
	'''
		This method will parse the user-specified date format
		(yyyymmdd, yyyyjjj, yymmdd, yyjjj, or mmdd) and return
		a date object.
	'''
	if len(date) == 8:
		dobj = datetime.strptime(date, '%Y%m%d')
	elif len(date) == 7:
		dobj = datetime.strptime(date, '%Y%j')
	elif len(date) == 6:
		dobj = datetime.strptime(date,'%y%m%d')
	elif len(date) == 5:
		dobj = datetime.strptime(date,'%y%j')
	elif len(date) == 4:
		today = datetime.today()
		year = str(today.year)
		d = year + date
		dobj = datetime.strptime(d,'%Y%m%d')
	logger.info('    Date: %s' % (dobj.strftime('%Y-%m-%d')))
	return dobj

def check_date(path, row, dobj):
	'''
		This method will check the date user types. If the date matches one file
		in the Google Cloud directory, then return the data path string. If not match,
		user needs to type a different matched date.
	'''
	path, row = parse_path_row(path, row)

	path_str = 'gs://earthengine-public/landsat/L8/' + path + '/' + row

	p = Popen('gsutil ls '+path_str, stdout=PIPE, stderr=PIPE, shell=True)
	stdout = p.stdout.read()
	stderr = p.stderr.read()
	if stderr:
		logger.error(stderr)
		sys.exit()
	if stdout:
		data_path_list = stdout.split('\n')
		date_str = dobj.strftime('%Y%j')
		data_str = 'LC8' + path + row + date_str
		regex = re.compile(data_str)
		for data in data_path_list:
			if regex.search(data):
				logger.info('%s is found in the directory.' % (data_str))
				return path_str + '/' + data_str + '*'
		logger.error("The data for the date you requested is not in the directory. Please type a different date!")
		sys.exit()

def download(path, row, date):
	path, row = parse_path_row(path, row)
	logger.info('You are requesting:')
	logger.info('    Path: %s     Row: %s' %(path, row))
	path_str = 'gs://earthengine-public/landsat/L8/' + path + '/' + row
	dobj = parse_date(date)
	data_path_str = check_date(path, row, dobj)
	if not os.path.isdir('./data'):
	os.mkdir('./data')
	logger.info('Downloading the data...')
	p = Popen('gsutil cp '+data_path_str+' ./data', stdout=PIPE, stderr=PIPE, shell=True)
	stdout = p.stdout.read()
	stderr = p.stderr.read()
	if stderr:
		logger.error(stderr)
	if stdout:
		logger.info(stdout)

def parse_command_line():
	DATE_str = '20000101'
	parser = get_config('config')
	path_config = parser.get('Path-Row','path')
	row_config = parser.get('Path-Row','row')
	path_default, row_default = parse_path_row(path_config, row_config)

	parser_cml = argparse.ArgumentParser(description='Script to download Landsat8 frame for a path and row and a given date')
	parser_cml.add_argument('-p','--path', type=str, help='The path of the frame to be downloaded', default=path_default)
	parser_cml.add_argument('-r', '--row', type=str, help='The row of the frame to be downloaded', default=row_default)
	parser_cml.add_argument('-d', '--date', type=str, help='The date of the frame to be downloaded', default=DATE_str)
	args = parser_cml.parse_args()
	path = args.path
	row = args.row
	DATE = search_latest(path, row)
	DATE_str = datetime.strftime(DATE, '%Y%m%d')
	parser_cml.set_defaults(date=DATE_str)
	args = parser_cml.parse_args()

	return args

def bunzip2_untar_file(path, row, date):
	'''
		This method will create the corresponding directory for the file and move the file to this directory.
		Then, it will unzip the bz file and untar the tar file.
	'''
	dobj = parse_date(date)
	path, row = parse_path_row(path, row)
	date_str = dobj.strftime('%Y-%m-%d')
	date_str1 = dobj.strftime('%Y%j')
	path_row = path + '-' + row

	if not os.path.isdir('./data/'+path_row):
		os.mkdir('./data/'+path_row)
	if not os.path.isdir('./data/'+path_row+'/'+date_str):
		os.mkdir('./data/'+path_row+'/'+date_str)
	f_list = glob.glob('./data/'+'*'+date_str1+'*')
	f = f_list[0]
	f = os.path.basename(f)
	os.rename('./data/'+f, './data/'+path_row+'/'+date_str+'/'+f)
	os.chdir('./data/'+path_row+'/'+date_str)
	tar = tarfile.open(f)
	logger.info('\nExtracting the data...')
	tar.extractall()
	tar.close()

def logger():
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler()
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter('%(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger

if __name__ == '__main__':
	logger = logger()

	opts = parse_command_line()
	path = opts.path
	row = opts.row
	date = opts.date

	download(path, row, date)
	logger.info('Download complete!\n')
	bunzip2_untar_file(path, row, date)
	logger.info('Extract complete!\n')
