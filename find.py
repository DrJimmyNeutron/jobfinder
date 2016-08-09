#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import json
import sys
import re

reportfile = 'report.txt'

htmlfile = 'diary'

if len(sys.argv) > 1:
	cmd_gethtml = 'wget http://eltiempo.com.ve/diarios/%s -O %s' % (sys.argv[1], htmlfile)
else:
	cmd_gethtml = 'wget http://eltiempo.com.ve/diarios -O %s' % htmlfile

print 'Searching %s' % cmd_gethtml

cmd_catportadas = 'cat %s | grep portada' % htmlfile
cmd_getpdf = "wget %s -O %s/%s"

pdffolder = 'pdf'
cmd_createpdffolder = 'mkdir %s' % pdffolder
cmd_clearpdffolder = 'rm -rf %s/*' % pdffolder
cmd_rmreport = 'rm %s' % reportfile


cmd_pdftotext = 'pdftotext %s'



keywords = [
	'informático',
	'informatico',
	'programador',
	'visual studio',
	'electricista',
]

#'0.pdf': {'kws': [], 'err': False},
results = {}



def extractpdfurl(line):
	href = line.split()[3]
	return href.split('"')[1]

def getpdf(pdfurl, output):
	os.system(cmd_getpdf % (pdfurl, pdffolder, output))


def findkeywordsinline(pline, pdfname):
	line = pline.lower()
	line = re.sub(' +', ' ', line.strip())

	for k in keywords:
		if line.find(k) > 0:
			results[pdfname]['kws'].append(k)


def findkeywordsinpdf(index):
	pdfname = str(index) + '.pdf'
	txt = '%s/%s.txt' %(pdffolder, str(index))

	path = '%s/%s' % (pdffolder, pdfname)
	print cmd_pdftotext % path
	os.system(cmd_pdftotext % path)

	file = open(txt, 'r')
	results[pdfname] = {'kws': []}

	while True:
		line = file.readline()
		if not line: break
		findkeywordsinline(line, pdfname)

	print results
	rfile = open(reportfile, 'w')
	for r in results: 
		rfile.write(json.dumps(r) + '\n\t')
		for kw in results[r]['kws']: rfile.write(kw)
		if len(results[r]['kws']) <= 0: rfile.write('No results')
		rfile.write('\n\n')
	rfile.close()




def delfiles():
	os.system(cmd_gethtml)
	os.system(cmd_createpdffolder)
	os.system(cmd_clearpdffolder)
	os.system(cmd_rmreport)

def init():
	delfiles()

	rfile = open(reportfile, 'w')
	rfile.close()

def clean():
	delfiles()



if __name__ == '__main__':
	init()

	htmlfile = open(htmlfile, 'r')
	
	cc = 0
	while True:
		line = htmlfile.readline()
		if not line: break

		if line.find('portada') > 0:
			print ('\n'*10) + '%s' % cc
			
			pdfurl = extractpdfurl(line)
			pdfoutput = str(cc) + '.pdf'

			getpdf(pdfurl, pdfoutput)
			findkeywordsinpdf(cc)
			cc += 1














































