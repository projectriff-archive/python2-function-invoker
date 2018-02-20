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
import sys
import unittest
import subprocess
import os
import time
import signal

from invoker import function_pb2_grpc as function
from invoker import function_pb2 as message
from invoker import funcrunner


PORT=10382
#TODO: Make this portable
PYTHON2 = "~/miniconda2/bin/python"


class GrpcFunctionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #TODO: Make this portable
        workingdir = os.path.abspath("../invoker")
        command =  "%s funcrunner.py" % PYTHON2
        cls.process = subprocess.Popen(command,
            shell=True,
            env=None,
            cwd=workingdir,
            preexec_fn=os.setsid,
        )
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        try:
            os.killpg(cls.process.pid, signal.SIGTERM)
        except:
            print("ERROR: Unable to kill PID %d" % cls.process.pid)

    def test_upper(self):
        pass

# def run():
#   channel = grpc.insecure_channel('localhost:50051')
#   stub = function.MessageFunctionStub(channel)
#   responses = stub.Call(generate_messages())
#   for response in responses:
#       print("Received message %s at %s" % (response.message,
#                                            response.location))
#
#
# def generate_messages():
#     messages = [
#         message.Message(payload="hello",headers=None),
#     ]
#     for msg in messages:
#         print("Sending %s at %s" % (msg.message, msg.location))
#         yield msg
