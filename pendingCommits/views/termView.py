class TermView:
	def __init__(self, options):
		self.options = options
		self.rootDir = False
		self.newLine = ''
		self.colors = {
			'reset'   : '\033[0m',
			'shipped' : '\033[38;1;46m',
			'ready'   : '\033[38;5;208m',
			'stashed' : '\033[38;5;196m',
		}

	def displayLegend(self):
		print '\nLegend:\n    ' + self.colors['stashed'] + 'Stashed ' +  self.colors['reset'] + self.colors['ready'] + 'Ready ' +  self.colors['reset'] + self.colors['shipped'] + 'Shipped' + self.colors['reset']

	def addLogLine(self, message, revisions, author, paths):
		print '- ' + message + ' ' + revisions,
		print '(%s)' % author

		if self.options.showPaths is True:
			for path in paths: 
				print "   [%s] %s" % (path.action, path.path)
				if path.action == 'M':
					print path.diff
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


