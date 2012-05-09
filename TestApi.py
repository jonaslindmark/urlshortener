import sys
import pymongo
import bson.objectid
pymongo.objectid = bson.objectid
sys.modules["pymongo.objectid"] = bson.objectid

import unittest
from pymongo import Connection
from pymongo.objectid import ObjectId

from api import UrlStore

class TestApi(unittest.TestCase):
	def setUp(self):
		connection = Connection('localhost',27017)
		db = connection.test
		db.urltest.drop()
		db.sequencestest.drop()
		self.urls = db.urltest
		self.sequences = db.sequencestest
		self.sequences.insert({"name":"postid","id":0})
		self.store = UrlStore(self.urls,self.sequences)
	
	def tearDown(self):
		self.urls.drop()
		self.sequences.drop()
				
	def test_newid(self):
		for i in range(1,10):
			self.assertEqual(str(i),self.store._getNewId())
	def test_hexrepresentation(self):
		self.assertEqual('A',self.store._getHexRepresentation(10))
		
	def test_saveandretrieve(self):
		url = "http://haid00ds.se/"
		id = self.store.storeUrl(url)
		retrieved_url = self.store.getUrlById(id)
		self.assertEqual(url,retrieved_url)
if __name__ == '__main__':
	unittest.main()