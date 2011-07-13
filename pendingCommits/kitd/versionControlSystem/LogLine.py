

class LogLine():
	def __init__(self, message, revisions, author, paths):
		self.message = message
		self.revisions = revisions
		self.author = author
		for path in paths:
			self.paths.append(Path(path.action, path.path))
