from concurrent import futures

__copyright__ = '''
Copyright 2018 the original author or authors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
__author__ = 'David Turanski'

import os, sys

sys.path.insert(0, os.path.abspath('.'))

import grpc
import time
import function_pb2_grpc as function
import function_pb2 as message
import json


def run(func, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    function.add_MessageFunctionServicer_to_server(MessageFunctionServicer(func), server)
    server.add_insecure_port('%s:%s' % ('[::]', os.environ.get("GRPC_PORT", "10382")))

    server.start()

    while True:
        time.sleep(10)


class MessageFunctionServicer(function.MessageFunctionServicer):

    def __init__(self, func):
        self.func = func

    def Call(self, request_iterator, context):
        for request in request_iterator:
            result = self.func(self.convertRequestPayload(request))

            reply = message.Message()
            reply.payload = self.convertReplyPayload(request.headers['Accept'].values, result)

            reply.headers['correlationId'].values[:] = request.headers['correlationId'].values[:]
            yield reply

    def convertRequestPayload(self, request):
        if 'application/json' in request.headers['Content-Type'].values:
            return self.byteify(json.loads(request.payload))
        else:
            return request.payload

    def convertReplyPayload(self, accepts, val):

        if len(accepts) == 0 or 'text/plain' in accepts or "*/*" in accepts:
            if type(val) is dict:
                return json.dumps(val)
            else:
                return str(val)

        if 'application/json' in accepts:
            if type(val) is dict:
                return json.dumps(val)
            else:
                raise RuntimeError('Cannot convert type %s to JSON' % type(val))
        else:
            raise RuntimeError('Unsupported Accept header type %s' % accepts)


    def byteify(self, val):
        if isinstance(val, dict):
            return {self.byteify(key): self.byteify(value)
                    for key, value in val.iteritems()}
        elif isinstance(val, list):
            return [self.byteify(element) for element in val]
        elif isinstance(val, unicode):
            return val.encode('utf-8')
        else:
            return val
