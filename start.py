#import sys
#import pymongo
#import bson.objectid
#pymongo.objectid = bson.objectid
#sys.modules["pymongo.objectid"] = bson.objectid
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.python.log import err
from api import UrlStore
from gui import UrlDispatcher
from gui import StaticResource
from gui import FormResponder
from gui import FailurePage
from gui import ResultPage
from pymongo import Connection


formfile = open("form.html","r")
formcode = formfile.read()

con = Connection()
urlstore = UrlStore(con.prod.urls, con.prod.seqs)


urldispatcher = UrlDispatcher(urlstore)
formpage = StaticResource(formcode)
formresult = FormResponder(urlstore)
failure = FailurePage()
result = ResultPage()

root = Resource()
root.putChild("l",urldispatcher)
root.putChild("addurl",formpage)
root.putChild("result",formresult)
root.putChild("failure",failure)
root.putChild("resultpage",result)
factory = Site(root)

reactor.listenTCP(9090,factory)
reactor.run()
