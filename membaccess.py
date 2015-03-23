import os
import csv
import sys
import time

tempfn = "/tmp/membership.csv"

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
	# File to fetch. Use cmd_list() to figure out what file.
	id = "0AkDXTfWtDy1VdFY1Wm84OGJGanp0WTM4ek1aMnBnZkE"

	file = drive.CreateFile({'id': id})
	print file['title']
	print file['mimeType']
	if u'text/csv' not in file.metadata['exportLinks']:
		# Current versions of PyDrive don't provide CSV download links, but it seems quite functional
		file.metadata['exportLinks'][u'text/csv'] = file.metadata['exportLinks'][u'application/pdf'][:-3]+u"csv"
	# Current versions of PyDrive don't support GetContentString() with a mimetype parameter, but the Python
	# 'csv' module doesn't support reading from a string anyway, so we dump out to a file.
	file.GetContentFile(tempfn,mimetype="text/csv")

def get_file():
	# Freshen the file if it's more than an hour old, or doesn't exist.
	try:
		if time.time()-os.stat(tempfn).st_mtime > 3600: cmd_fetch()
	except OSError:
		cmd_fetch()
	# It should now be possible to read tempfn. (Should. It could still raise.)

def cmd_columns():
	get_file()
	with open(tempfn) as f:
		print(next(csv.reader(f)))

def generate_html():
	get_file()
	cols = ['Title', 'First Name', 'Surname', 'SortCode']
	yield "<!doctype html>"
	yield "<html>"
	yield "<head><title>G&S Society Membership</title></head>"
	yield "<body><table border>"
	yield "<tr><td>"+"</td><td>".join(cols)+"</td></tr>"
	with open(tempfn) as f:
		for row in csv.DictReader(f):
			yield "<tr><td>"+"</td><td>".join(row[col] for col in cols)+"</td></tr>"
	yield "</table></body>"
	yield "</html>"

def cmd_html():
	for line in generate_html(): print(line)

if __name__ == '__main__':
	# If error, throw exception. Bahahaha.
	globals()["cmd_"+sys.argv[1]]()
