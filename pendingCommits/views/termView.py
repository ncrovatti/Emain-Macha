class TermView:
	def __init__(self, options):
		self.options = options
		self.colors = {
			'reset'   : '\033[0m'
		}

	
	def addLogLine(self, message, revisions, author, paths):
		print '- ' + message + ' ' + revisions,
		print '(%s)' % author

		if self.options.showPaths is True:
			for path in paths: 
				print "   [%s] %s" % (path.action, path.path)
			print ""

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

