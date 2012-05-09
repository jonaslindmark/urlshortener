import sys
import pymongo
import bson.objectid
pymongo.objectid = bson.objectid
sys.modules["pymongo.objectid"] = bson.objectid

import unittest
from pymongo import Connection
from pymongo.objectid import ObjectId

from api import *
from gui import *

from mock import MagicMock

class TestGui(unittest.TestCase):
	#def setUp(self):
		
	#def tearDown(self):
	
	def test_dispatcher(self):
		d = UrlDispatcher("")
		testcode = "asdlkjjlk3jkklk"
		redirecter = d.getChild(testcode,"")
		self.assertEqual(testcode,redirecter.urlid)
	
	def test_redirecterfailure(self):
		d = UrlRedirecter("","")
		mock = MagicMock()
		d.handleFailure("",mock)
		mock.cancel.assert_called_with()
	def test_redirects_on_ok_url(self):
		urlstore = MagicMock()
		urlid = "hai"
		url = "asdlkjsdlkfj"
		urlstore.getUrlById.return_value = url
		r = UrlRedirecter(urlid,urlstore)
		request = MagicMock()
		r.redirectToSavedUrl(request)
		request.redirect.assert_called_with(url)
		request.finish.assert_called_with()
	def test_returns_correct_on_bad_url(self):
		urlstore = MagicMock()
		urlid = "hai"
		url = "asdlkjsdlkfj"
		urlstore.getUrlById.return_value = None	
		r = UrlRedirecter(urlid,urlstore)
		request = MagicMock()
		r.redirectToSavedUrl(request)
		request.write.assert_called_with("No link attached to that code")
		request.finish.assert_called_with()
if __name__ == '__main__':
	unittest.main()
