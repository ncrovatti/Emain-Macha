# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Personnel/pending.commits.ui'
#
# Created: Tue Jul 12 17:46:18 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PendingCommits(object):
    def setupUi(self, PendingCommits):
        PendingCommits.setObjectName("PendingCommits")
        PendingCommits.resize(691, 482)
        self.centralwidget = QtGui.QWidget(PendingCommits)
        self.centralwidget.setObjectName("centralwidget")
        self.commitsList = QtGui.QTreeWidget(self.centralwidget)
        self.commitsList.setGeometry(QtCore.QRect(0, 0, 691, 461))
        self.commitsList.setMinimumSize(QtCore.QSize(691, 0))
        self.commitsList.setAlternatingRowColors(True)
        self.commitsList.setObjectName("commitsList")
        PendingCommits.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(PendingCommits)
        self.statusbar.setObjectName("statusbar")
        PendingCommits.setStatusBar(self.statusbar)

        self.retranslateUi(PendingCommits)
        QtCore.QMetaObject.connectSlotsByName(PendingCommits)

    def retranslateUi(self, PendingCommits):
        PendingCommits.setWindowTitle(QtGui.QApplication.translate("PendingCommits", "Pending Commits", None, QtGui.QApplication.UnicodeUTF8))
        self.commitsList.headerItem().setText(0, QtGui.QApplication.translate("PendingCommits", "Message", None, QtGui.QApplication.UnicodeUTF8))
        self.commitsList.headerItem().setText(1, QtGui.QApplication.translate("PendingCommits", "Revisions", None, QtGui.QApplication.UnicodeUTF8))
        self.commitsList.headerItem().setText(2, QtGui.QApplication.translate("PendingCommits", "Author", None, QtGui.QApplication.UnicodeUTF8))

