'''
Stores urls in MongoDB
'''
class UrlStore:
	'''
	Accepts two pymongo.Collection instances
	'''
	def __init__(self,urls,sequences):
		self.urls = urls
		self.sequences = sequences
	
	def _getDecimalNewId(self):
		previousId = self.sequences.find_and_modify({"name":"postid"},{'$inc':{"id":1}})
		return previousId['id']+1
	
	'''
	Returns the hex value without the '0x' part
	'''
	def _getHexRepresentation(self,decimal_id):
		return hex(int(decimal_id))[2:].upper()
		
	def _getNewId(self):
		new_dec_id = self._getDecimalNewId()
		return self._getHexRepresentation(new_dec_id)
		
	def storeUrl(self,url):
		url_id = self._getNewId()
		self.urls.save({"url":url,"id":url_id})
		return url_id
		
	def getUrlById(self,id):
		post = self.urls.find_one({"id":id})
		if (post == None):
			return None
		return post['url'].encode("utf-8")
		
