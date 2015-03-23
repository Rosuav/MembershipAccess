import os
import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

if False:
	for f in drive.ListFile({"q":"title contains 'G&S Soc'"}).GetList():
		print(f['id']+" "+f['title'])

# File to view. Use the above to figure out what file.
id = "0AkDXTfWtDy1VdFY1Wm84OGJGanp0WTM4ek1aMnBnZkE"

file = drive.CreateFile({'id': id})
print file['title']
print file['mimeType']
if u'text/csv' not in file.metadata['exportLinks']:
	# Current versions of PyDrive don't provide CSV download links, but it seems quite functional
	file.metadata['exportLinks'][u'text/csv'] = file.metadata['exportLinks'][u'application/pdf'][:-3]+u"csv"
# Current versions of PyDrive don't support GetContentString() with a mimetype parameter, but the Python
# 'csv' module doesn't support reading from a string anyway, so we dump out to a file.
fn="/tmp/membership.csv"
file.GetContentFile(fn,mimetype="text/csv")
with open(fn) as f:
	for row in csv.DictReader(f):
		print(row)
		break
os.remove(fn)
