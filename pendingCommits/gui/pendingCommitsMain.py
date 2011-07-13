# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Personnel/Emain-Macha/pending.commits.ui'
#
# Created: Wed Jul 13 14:14:49 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PendingCommits(object):
    def setupUi(self, PendingCommits):
        PendingCommits.setObjectName("PendingCommits")
        PendingCommits.resize(692, 483)
        self.centralwidget = QtGui.QWidget(PendingCommits)
        self.centralwidget.setObjectName("centralwidget")
        self.commitsList = QtGui.QTreeWidget(self.centralwidget)
        self.commitsList.setGeometry(QtCore.QRect(0, 0, 691, 461))
        self.commitsList.setMinimumSize(QtCore.QSize(691, 0))
        self.commitsList.setAlternatingRowColors(True)
        self.commitsList.setObjectName("commitsList")
        PendingCommits.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(PendingCommits)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setObjectName("statusbar")
        PendingCommits.setStatusBar(self.statusbar)

        self.retranslateUi(PendingCommits)
        QtCore.QMetaObject.connectSlotsByName(PendingCommits)

    def retranslateUi(self, PendingCommits):
        PendingCommits.setWindowTitle(QtGui.QApplication.translate("PendingCommits", "Pending Commits", None, QtGui.QApplication.UnicodeUTF8))
        self.commitsList.headerItem().setText(0, QtGui.QApplication.translate("PendingCommits", "Message", None, QtGui.QApplication.UnicodeUTF8))
        self.commitsList.headerItem().setText(1, QtGui.QApplication.translate("PendingCommits", "Revisions", None, QtGui.QApplication.UnicodeUTF8))
        self.commitsList.headerItem().setText(2, QtGui.QApplication.translate("PendingCommits", "Author", None, QtGui.QApplication.UnicodeUTF8))

