import re

class HtmlView:
	def __init__(self, options):
		print '''<html>
			<head>
				<style>
					.added    { color: #AAFFAA; }
					.removed  { color: #FFAAAA; }
				</style>
			</head>
		<body style="background:#424242;color:#e7e7e7;font-family:monospace;">'''
		self.options = options
		self.rootDir = False
		self.newLine = '<br/>'
		self.colors = {
			'reset'   : '</span>',
			'shipped' : '<span style="color:green;">',
			'ready'   : '<span style="color:#df8e00;">',
			'stashed' : '<span style="color:red;">',
		}

	def htmlEscape(self, text):
		html_escape_table = {
			"&": "&amp;",
			'"': "&quot;",
			"'": "&apos;",
			">": "&gt;",
			"<": "&lt;",
		}

		return "".join(html_escape_table.get(c,c) for c in text)
	
	def displayLegend(self):
		pass

	def addLogLine(self, message, revisions, author, paths):

		print '- ' + message + ' ' + revisions,
		print '(%s) <br/>' % author

		if self.options.showPaths is True:
			for path in paths: 
				print "[%s] %s <br/>" % (path.action, path.path)

				if path.action == 'M':
					print '<pre>'
					for line in path.diff.split('\n'):
						line = self.htmlEscape(line)
						p = re.compile('\t')
						line = p.sub('&nbsp;&nbsp;&nbsp;&nbsp;', line)
						p = re.compile('\s')
						line = p.sub('&nbsp;', line)


						p = re.compile('^\+\+\+')
						if p.match(line):
							print p.sub('<span class="added">+++', line) + "</span>"
						else:
							p = re.compile('^---')
							if p.match(line):
								print p.sub('<span class="removed">---', line) + "</span>"
							else:
								p = re.compile('^\+\s*')
								if p.match(line):
									print p.sub('<span class="added">+ ', line) + "</span>"
								else:
									p = re.compile('^-\s*')
									if p.match(line):
										print p.sub('<span class="removed">- ', line) + "</span>"
									else:
										print '&nbsp;' + line 


					#	print line.replace('+ ', '<span class="added">+ ') + '</span><br/>'
					#	print line.replace('- ', '<span class="removed">- ') + '</span><br/>'
#					print '<pre>' + path.diff.replace('\n', '<br/>') + '</pre>'
					print '</pre>'
			print "<br/>"

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


