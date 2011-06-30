#!/usr/bin/env python

import pysvn
import string
import time
import urllib
import re
import hashlib
import operator
from optparse import OptionParser
from datetime import datetime

class Repository:
	def __init__(self):
		self.options                   = self.parseArgs()
		self.limit                     = 0
		self.noRevision                = pysvn.Revision(pysvn.opt_revision_kind.unspecified)
		self.headRevision              = pysvn.Revision(pysvn.opt_revision_kind.head)
		self.user                      = "nicolas.crovatti"
		self.password                  = "Wx8V41p7"
		self.rootDir                   = u"/home/nico/workspace/pulse3/%s" % self.options.customDir
		self.client                    = pysvn.Client()
		self.client.commit_info_style  = 1
		self.client.callback_notify    = self.notify
		self.client.callback_get_login = self.credentials
		self.shippedRevisions          = self.getShippedItemList();

	def parseArgs(self):
		parser = OptionParser()
		parser.add_option("-s" , "--start"       , type="string"       , default=""                 , dest="firstShipping" , help="Shipping start date"   , metavar="START_DATE")
		parser.add_option("-e" , "--end"         , type="string"       , default=""                 , dest="lastShipping"  , help="Shipping end date"     , metavar="END_DATE")
		parser.add_option("-u" , "--user"        , type="string"       , default="nicolas.crovatti" , dest="developerName" , help="Developer name"        , metavar="DEVELOPER")
		parser.add_option("-d" , "--subtree"     , type="string"       , default="kewego"           , dest="customDir"     , help="Custom directory"      , metavar="CUSTOM_DIR")
		parser.add_option("-p" , "--paths"       , action="store_true" , default=False              , dest="showPaths"     , help="Display modifed paths" , metavar="SHOW_PATHS")
		(options, args) = parser.parse_args()
		return options

	def notify(event_dict):
		print event_dict
		return

	def credentials(realm, username, may_save):
		return True, self.user, self.password, True

	def getShippedItemList(self):
		try:
			f = urllib.urlopen("http://wiki.kewego.int/wakka.php?wiki=WebShippingChangeLog")
		except Exception, e:
			print "[SocketWarning] Could not fetch latest revisions. All revisions will be considered as unshipped."
			return []

		p = re.compile('r\d{5,}')
		return p.findall(f.read())

	def getRevisionFromDate(self, date, format='%Y-%m-%d'):
		if date is not '':
			formatedTime = time.strptime(date, format);
			return pysvn.Revision(pysvn.opt_revision_kind.date, time.mktime(formatedTime))

	
	def buildRevisionList(self, revisionList, color):
		colorReset = '\033[0m'

		if len(revisionList) == 0:
			return '';

		buff = '('
		for rev in revisionList:
			buff += color + 'r' + str(rev)
			if rev != revisionList[-1]:
				buff += colorReset + ', '

		buff += colorReset + ')'
		return buff
	
	def sortLogs(self, logs):

		groupedLogs = {}
		for log in logs:
			if self.options.developerName is '' or self.options.developerName == log.author:
				groupId = hashlib.md5(log.message + log.author).hexdigest()
				
				if groupId not in groupedLogs:
					groupedLogs[groupId] = {
						'revisions' : {
							'shipped' : [],
							'stashed' : [],
							'all'     : []
						},
						'author'    : log.author,
						'date'      : time.ctime(log.date),
						'message'   : log.message.replace('\t','').replace('\n', ''),
						'paths'     : log.changed_paths
					}

					groupedLogs[groupId]['revisions']['all'].append(log.revision.number)

					if u"r%s" % log.revision.number in self.shippedRevisions:
						groupedLogs[groupId]['revisions']['shipped'].append(log.revision.number)
					else:
						groupedLogs[groupId]['revisions']['stashed'].append(log.revision.number)

		states = {
			'shippedItems'           : {},
			'stashedItems'           : {},
			'shippedAndStashedItems' : {}
		}

		for groupId in groupedLogs:
			if len(groupedLogs[groupId]['revisions']['stashed']) > 0 and len(groupedLogs[groupId]['revisions']['shipped']) == 0:
				states['stashedItems'][groupId] = groupedLogs[groupId]
				continue
				
			if len(groupedLogs[groupId]['revisions']['shipped']) > 0 and len(groupedLogs[groupId]['revisions']['stashed']) == 0:
				states['shippedItems'][groupId] = groupedLogs[groupId]
				continue

			states['shippedAndStashedItems'][groupId] = groupedLogs[groupId]
				
		return states

	def getLogs(self):
		lastShipping  = self.getRevisionFromDate(self.options.lastShipping)
		firstShipping = self.getRevisionFromDate(self.options.firstShipping) 
		
		try:
			logs  = self.client.log(self.rootDir, firstShipping, lastShipping, True, True, self.limit, self.noRevision, False, None)
		except Exception, e:
			try:
				logs  = self.client.log(self.rootDir, self.headRevision, lastShipping, True, True, self.limit, self.noRevision, False, None)
			except Exception, e:
				print '[ArgumentError] Invalid argument. lastShipping is required'
				return -1

		groupedLogs = self.sortLogs(logs)

		for group in groupedLogs:
			if len(groupedLogs[group]) == 0:
				continue

			print group + ":" 
			for logId in groupedLogs[group]:
				print '- ' + groupedLogs[group][logId]['message'],
				
				stashedRevisions = self.buildRevisionList(groupedLogs[group][logId]['revisions']['stashed'], '\033[38;1;46m')
				shippedRevisions = self.buildRevisionList(groupedLogs[group][logId]['revisions']['shipped'], '\033[38;5;208m')
				revisions = shippedRevisions + ' ' +  stashedRevisions

				print revisions, 
				print '(%s)' % groupedLogs[group][logId]['author']

				if self.options.showPaths is True:
					for path in groupedLogs[group][logId]['paths']:
						print "   [%s] %s" % (path.action, path.path)
					print ''
			
		if len(groupedLogs) > 0:
			print ''
			print 'Legend:'
			print '  \033[38;1;46m Stashed\033[0m,\033[38;5;208m Shipped\033[0m'

if __name__ == "__main__":
	repo = Repository()
	repo.getLogs();

