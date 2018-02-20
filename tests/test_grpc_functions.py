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

import grpc
import unittest
import subprocess
import os
import uuid
import time

from invoker import function_pb2_grpc as function
from invoker import function_pb2 as message

PORT = 10382
# TODO: Make this portable
PYTHON2 = "~/miniconda2/bin/python"


class GrpcFunctionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: Make this portable
        cls.workingdir = os.path.abspath("../invoker")
        cls.command = "%s funcrunner.py" % PYTHON2

    def setUp(self):
        pass

    def tearDown(self):
        print("killing %s" % self.process.pid)
        self.process.kill()


    def test_upper(self):
        env = {
            'PYTHONPATH': '%s/functions:$PYTHONPATH' % os.getcwd(),
            'FUNCTION_URI': 'file://%s/functions/upper.py?handler=handle' % os.getcwd()
        }

        self.process = subprocess.Popen(self.command,
                                        cwd=self.workingdir,
                                        shell=True,
                                        env=env,
                                        preexec_fn=os.setsid,
                                        )
        time.sleep(0.5)

        channel = grpc.insecure_channel('localhost:%s' % PORT)
        self.stub = function.MessageFunctionStub(channel)

        def generate_messages():
            headers = {
                'Content-Type': message.Message.HeaderValue(values=['text/plain']),
                'correlationId': message.Message.HeaderValue(values=[str(uuid.uuid4())])
            }

            messages = [
                message.Message(payload="hello", headers=headers),
                message.Message(payload="world", headers=headers),
                message.Message(payload="foo", headers=headers),
                message.Message(payload="bar", headers=headers),
            ]
            for msg in messages:
                yield msg

        responses = self.stub.Call(generate_messages())
        expected = ['HELLO', 'WORLD', 'FOO', 'BAR']

        for response in responses:
            self.assertTrue(response.payload in expected)
            expected.remove(response.payload)

        self.assertEquals(0, len(expected))

    def test_concat(self):
        env = {
            'PYTHONPATH': '%s/functions:$PYTHONPATH' % os.getcwd(),
            'FUNCTION_URI': 'file://%s/functions/concat.py?handler=concat' % os.getcwd()
        }

        self.process = subprocess.Popen(self.command,
                                        cwd=self.workingdir,
                                        shell=True,
                                        env=env,
                                        preexec_fn=os.setsid,
                                        )
        time.sleep(1)

        channel = grpc.insecure_channel('localhost:%s' % PORT)
        self.stub = function.MessageFunctionStub(channel)

        def generate_messages():
            headers = {
                'Content-Type': message.Message.HeaderValue(values=['application/json']),
                'correlationId': message.Message.HeaderValue(values=[str(uuid.uuid4())])
            }

            messages = [
                message.Message(payload='{"foo":"bar","hello":"world"}', headers=headers),
            ]
            for msg in messages:
                yield msg

        responses = self.stub.Call(generate_messages())

        for response in responses:
           self.assertEquals('{"result": "foobarhelloworld"}',response.payload)