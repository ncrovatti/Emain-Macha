from PyQt4 import QtGui
from gui.pendingCommitsMain import Ui_PendingCommits

class QtView(QtGui.QMainWindow):
	def __init__(self, options):
		QtGui.QMainWindow.__init__(self)
		self.options = options
		self.ui = Ui_PendingCommits()
		self.ui.setupUi(self)

	def resizeEvent(self, event):
		window = event.size()
		self.ui.commitsList.resize(window.width(), window.height() - self.ui.statusbar.height())

	def addLogLine(self, message, revisions, author, paths):
		line = QtGui.QTreeWidgetItem([message, revisions, author])
		self.ui.commitsList.addTopLevelItem(line)

	def buildRevisionList(self, revisionList, color):
		if len(revisionList) == 0:
			return '';

		buff = ''	
		for rev in revisionList:
			buff += 'r' + str(rev)
			if rev != revisionList[-1]:
				buff += ', '

		return buff
