class Suitcase(object):
	def __init__(self, entity=None):
		super(Suitcase, self).__init__()
		self.entity = entity
		self.items = []

	def package_item(self, handler, url, content, **kwargs):
		it = Item(handler, url, content, **kwargs)
		self.items.append(it)

	def __iter__(self):
		for _ in self.items:
			yield _


class Item(object):
	def __init__(self, handler, url, content, **kwargs):
		self.handler = handler
		self.url = url
		self.content = content
		self.params = kwargs



