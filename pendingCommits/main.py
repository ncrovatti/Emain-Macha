#!/usr/bin/env pytho 
import os
import sys
import time

import kewego.vcsClient
import pysvn
from optparse import OptionParser

def parseOptions():
	parser = OptionParser()
	parser.add_option("-f" , "--start"       , type="string" , default="", dest="firstShipping"  , help="Shipping start date"     , metavar="START_DATE")
	parser.add_option("-l" , "--end"         , type="string" , default="", dest="lastShipping"   , help="Shipping end date"       , metavar="END_DATE")
	parser.add_option("-c" , "--contributor" , type="string" , default="", dest="developperName" , help="Developer name"          , metavar="DEVELOPER")
	parser.add_option("-s" , "--subtree"     , type="string" , default="", dest="customDir"      , help="Custom directory (kewego, pj, ...)" , metavar="CUSTOM_DIR")
	(options, args) = parser.parse_args()
	return options

def getLogs():
	revhead = pysvn.Revision( pysvn.opt_revision_kind.head )
	lastShipping = pysvn.Revision( pysvn.opt_revision_kind.date, time.time() )
	firstShipping = pysvn.Revision( pysvn.opt_revision_kind.date,  )
	log_messages = log(
		url_or_path,
		revision_start=pysvn.Revision( opt_revision_kind.head ),
		revision_end=pysvn.Revision( opt_revision_kind.number, 0 ),
		discover_changed_paths=False,
		strict_node_history=True,
		limit=0,
		peg_revision=pysvn.Revision( opt_revision_kind.unspecified ),
		include_merged_revisions=False,	
		revprops=list_of_revprop_names 
	)

if __name__ == "__main__":
	options = parseOptions()
	client  = vcsClient()
	workDir = u"/home/nico/workspace/pulse3/%s" % options.customDir
	print("%s" % client.ok)

