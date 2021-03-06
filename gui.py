from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor
from twisted.python.log import err
from twisted.internet import defer
from twisted.web.util import Redirect
from twisted.web.error import NoResource
import cgi

'''
Dispatches this/[somecode] to a 
UrlRedirector with [somecode]
'''
class UrlDispatcher(Resource):

	def __init__(self,mongostore):
		Resource.__init__(self)
		self.mongostore = mongostore
		
	def getChild(self, name, request):
		return UrlRedirecter(name,self.mongostore)

	
'''
Renders GET and redirects to the
url stored for its urlid in a UrlStore

redirects to a generic failure page if
not url was associated with that urlid
'''
class UrlRedirecter(Resource):
	def __init__(self,urlid,store):
		Resource.__init__(self)
		self.urlid = urlid
		self.store = store
	
	def handleFailure(self,failure,call):
		err(failure,"fail")
		call.cancel()
		
		
	def redirectToSavedUrl(self,request):
		url = self.store.getUrlById(self.urlid)
		if (url == None):
			request.setResponseCode(404)
			request.write("No link attached to that code")
		else:
			request.redirect(url)
		request.finish()
		
	def render_GET(self,request):
		call = defer.succeed(self.redirectToSavedUrl(request))
		request.notifyFinish().addErrback(self.handleFailure,call)
		return NOT_DONE_YET


'''
Generic static resource that
displays its htmlcode upon request
'''
class StaticResource(Resource):
	def __init__(self,htmlcode):
		self.htmlcode = htmlcode

	def render_GET(self,request):
		return self.htmlcode


'''
The resource that will be posted to
from the form.html
'''
class FormResponder(Resource):
	def __init__(self, urlstore):
		self.urlstore = urlstore

	def parse_request(self,request):
		host = str(request.getHeader("host"))
		url_to_save = request.args["long-url"][0]
		if (host in url_to_save):
			request.redirect("/failure?msg=Dont redirect to me please..")
		else:
			newid = self.urlstore.storeUrl(url_to_save)
			request.redirect("/resultpage?urlid="+newid)
		request.finish()

	def handleFailure(self,request,call):
		err(failure,"Failed to parse form post")
		call.cancel()

	def render_POST(self,request):
		call = defer.succeed(self.parse_request(request))
		request.notifyFinish().addErrback(self.handleFailure,call)
		return NOT_DONE_YET

class ResultPage(Resource):
	def __init__(self):
		response_file = open("response.tmpl","r")
		responsetemplate = response_file.read()
		response_file.close()
		self.template = responsetemplate

	def render_GET(self,request):
		urlid = cgi.escape(request.args["urlid"][0])
		host = str(request.getHeader("host"))
		result = self.template
		if (not urlid == None):
			result = result.replace("[URL]",urlid)
			result = result.replace("[root]",host)
		return result


class FailurePage(Resource):
	def __init__(self):
		tmpl_file = open("failure.tmpl","r")
		self.failure = tmpl_file.read()
		tmpl_file.close()
	def render_GET(self,request):
		message = cgi.escape(request.args["msg"][0])
		result = self.failure
		if (not message == None):
			result = result.replace("[MSG]",message)
		return result
