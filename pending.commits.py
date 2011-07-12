#!/usr/bin/env python

import pysvn
import time
import urllib
import re
import hashlib
from PyQt4 import QtGui
from optparse import OptionParser
from pendingCommitsForm import *
import sys

class Repository:
	def __init__(self, window):
		self.ui                        = window.ui
		self.options                   = self.parseArgs()
		self.limit                     = 0
		self.noRevision                = pysvn.Revision(pysvn.opt_revision_kind.unspecified)
		self.headRevision              = pysvn.Revision(pysvn.opt_revision_kind.head)
		self.user                      = "nicolas.crovatti"
		self.password                  = "Wx8V41p7"
		self.rootDir                   = u"/home/nico/workspace/pulse3/%s" % self.options.customDir
		self.remoteDir                 = "https://svn.cardinet.kewego.int/svn/pulse3/"
		self.wikiBaseUrl               = "http://wiki.kewego.int/wakka.php?wiki="
		self.client                    = pysvn.Client()
		self.client.commit_info_style  = 1
		self.client.callback_notify    = self.notify
		self.client.callback_get_login = self.credentials
		self.shippedRevisions          = self.getShippedItemList()
		self.readyRevisions            = self.getReadyToShipItemList()

		self.colors = {
			'reset'   : '\033[0m',
			'shipped' : '\033[38;1;46m',
			'ready'   : '\033[38;5;208m',
			'stashed' : '\033[38;5;196m',
		}

		self.upToDate()
		print self.colors['reset']


	def upToDate(self):
		entry_list = self.client.info(self.rootDir)
		localRev = entry_list.revision.number;

		entry_list = self.client.info2(self.remoteDir, self.headRevision, self.noRevision, False)
		remoteRev = entry_list[0][1].last_changed_rev.number;

		if remoteRev > localRev: 
			print "%sWarning: you repository is behind by %s revisions" % (self.colors['ready'], remoteRev - localRev)

	def parseArgs(self):
		parser = OptionParser()
		parser.add_option("-s" , "--start"   , type="string"       , default=""                 , dest="firstShipping" , help="Shipping start date"    , metavar="START_DATE")
		parser.add_option("-e" , "--end"     , type="string"       , default=""                 , dest="lastShipping"  , help="Shipping end date"      , metavar="END_DATE")
		parser.add_option("-u" , "--user"    , type="string"       , default="nicolas.crovatti" , dest="developerName" , help="Developer name"         , metavar="DEVELOPER")
		parser.add_option("-d" , "--subtree" , type="string"       , default="kewego"           , dest="customDir"     , help="Custom directory"       , metavar="CUSTOM_DIR")
		parser.add_option("-t" , "--type"    , action="append"     , type="string"              , default=[]           , dest="revisionType"           , help="Restrict revision type" , metavar="TYPE")
		parser.add_option("-p" , "--paths"   , action="store_true" , default=False              , dest="showPaths"     , help="Display modifed paths"  , metavar="SHOW_PATHS")
		(options, args) = parser.parse_args()
		return options

	def notify(event_dict):
		print event_dict
		return

	def credentials(self, realm, username, may_save):
		return True, self.user, self.password, True

	def getReadyToShipItemList(self):
		try:
			f = urllib.urlopen(self.wikiBaseUrl + "WebShipping")
		except Exception, e:
			print "[SocketWarning] Could not fetch ready to ship revisions. All revisions will be considered as unshipped."
			return []

		p = re.compile('r\d{5,}')
		return p.findall(f.read())


	def getShippedItemList(self):
		try:
			f = urllib.urlopen(self.wikiBaseUrl + "WebShippingChangeLog")
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

		if len(revisionList) == 0:
			return '';
		
		buff = ' ('
		for rev in revisionList:
			buff += color + 'r' + str(rev)
			if rev != revisionList[-1]:
				buff += self.colors['reset'] + ', '

		buff += self.colors['reset'] + ')'
		return buff
	
	def sortLogs(self, logs):

		groupedLogs = {}

		for log in logs:
			if self.options.developerName is '' or self.options.developerName == log.author:
				message = log.message.replace('\t','').replace('\n', '')
				groupId = hashlib.md5(message + log.author).hexdigest()
				
				if groupId not in groupedLogs:
					groupedLogs[groupId] = {
						'revisions' : {
							'shipped' : [],
							'ready'   : [],
							'stashed' : [],
							'all'     : []
						},
						'author'    : log.author,
						'date'      : time.ctime(log.date),
						'message'   : message,
						'paths'     : log.changed_paths
					}

				groupedLogs[groupId]['revisions']['all'].append(log.revision.number)

				if u"r%s" % log.revision.number in self.shippedRevisions:
					groupedLogs[groupId]['revisions']['shipped'].append(log.revision.number)
				elif u"r%s" % log.revision.number in self.readyRevisions:
					groupedLogs[groupId]['revisions']['ready'].append(log.revision.number)
				else:
					groupedLogs[groupId]['revisions']['stashed'].append(log.revision.number)

		states = {
			'shipped' : {},
			'stashed' : {},
			'ready'   : {},
			'multi'   : {}
		}

		for groupId in groupedLogs:
			if len(groupedLogs[groupId]['revisions']['stashed']) > 0 and len(groupedLogs[groupId]['revisions']['shipped']) == 0:
				states['stashed'][groupId] = groupedLogs[groupId]
				continue
				
			if len(groupedLogs[groupId]['revisions']['shipped']) > 0 and len(groupedLogs[groupId]['revisions']['stashed']) == 0:
				states['shipped'][groupId] = groupedLogs[groupId]
				continue

			if len(groupedLogs[groupId]['revisions']['ready']) > 0:
				states['ready'][groupId] = groupedLogs[groupId]
				continue

			states['multi'][groupId] = groupedLogs[groupId]

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
			if len(self.options.revisionType) == 0 or group in self.options.revisionType:
				if len(groupedLogs[group]) == 0:
					if group in self.options.revisionType:
						print "No Match found for " + group
					continue

				print "\n" + group + ":" 
				for logId in groupedLogs[group]:
					
					stashedRevisions = self.buildRevisionList(groupedLogs[group][logId]['revisions']['stashed'], self.colors['stashed'])
					shippedRevisions = self.buildRevisionList(groupedLogs[group][logId]['revisions']['shipped'], self.colors['shipped'])
					readyRevisions   = self.buildRevisionList(groupedLogs[group][logId]['revisions']['ready'], self.colors['ready'])
					revisions        = shippedRevisions +  stashedRevisions +  readyRevisions

					print '- ' + groupedLogs[group][logId]['message'] + ' ' + revisions,
					print '(%s)' % groupedLogs[group][logId]['author']

					if self.options.showPaths is True:
						for path in groupedLogs[group][logId]['paths']:
							print "   [%s] %s" % (path.action, path.path)
						print ''
					self.ui.commitsList.addTopLevelItem(QtGui.QTreeWidgetItem([groupedLogs[group][logId]['message'], revisions, groupedLogs[group][logId]['author']]))

		if len(groupedLogs) > 0:
			print '\nLegend:\n    ' + self.colors['stashed'] + 'Stashed ' + self.colors['ready'] + 'Ready ' + self.colors['shipped'] + 'Shipped' + self.colors['reset']



# Create a class for our main window
class Main(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		# This is always the same
		self.ui = Ui_PendingCommits()
		self.ui.setupUi(self)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window=Main()
	window.show()

	repo = Repository(window)
	repo.getLogs();


	sys.exit(app.exec_())
	

