import os
import csv
import sys

def auth():
	from pydrive.auth import GoogleAuth
	from pydrive.drive import GoogleDrive

	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()

	return GoogleDrive(gauth)

def cmd_list():
	drive=auth()
	for f in drive.ListFile({"q":"title contains 'G&S Soc'"}).GetList():
		print(f['id']+" "+f['title'])

def cmd_fetch():
	drive=auth()
	# File to view. Use cmd_list() to figure out what file.
	id = "0AkDXTfWtDy1VdFY1Wm84OGJGanp0WTM4ek1aMnBnZkE"

	file = drive.CreateFile({'id': id})
	print file['title']
	print file['mimeType']
	if u'text/csv' not in file.metadata['exportLinks']:
		# Current versions of PyDrive don't provide CSV download links, but it seems quite functional
		file.metadata['exportLinks'][u'text/csv'] = file.metadata['exportLinks'][u'application/pdf'][:-3]+u"csv"
	# Current versions of PyDrive don't support GetContentString() with a mimetype parameter, but the Python
	# 'csv' module doesn't support reading from a string anyway, so we dump out to a file.
	file.GetContentFile("membership.csv",mimetype="text/csv")

# If error, throw exception. Bahahaha.
globals()["cmd_"+sys.argv[1]]()
