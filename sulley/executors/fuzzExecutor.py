import os
import re
import sys
import zlib
import time
import socket
import threading

from sulley import sex

"""
Base class used to executed a fuzzed data set
Used by sessions.fuzz, default arguement is this class
To define non-socket type fuzzers derive from this class and change the sessions.fuzz arg

Exception note: throw a sex.error with retry set to True if a retry is wanted
Throw a normal exception or something else to fail without retry
"""

class fuzzExecute:
	def __init__(self):
                pass

        def destroy(self):
                pass

        def initFuzz(self):
                pass

        def flushFuzz(self):
                pass

        def writeFuzz(self, data):
                pass

        ####################################################################################################################
        def post_send (self):
                '''
                Overload or replace this routine to specify actions to run after to each fuzz request. The order of events is
                as follows::

                    pre_send() - req - callback ... req - callback - post_send()

                When fuzzing RPC for example, register this method to tear down the RPC request.

                @see: pre_send()

                @type  sock: Socket
                @param sock: Connected socket to target
                '''

                # default to doing nothing.
                pass

        ####################################################################################################################
        def pre_send (self):
                '''
                Overload or replace this routine to specify actions to run prior to each fuzz request. The order of events is
                as follows::

                    pre_send() - req - callback ... req - callback - post_send()

                When fuzzing RPC for example, register this method to establish the RPC bind.

                @see: pre_send()

                @type  sock: Socket
                @param sock: Connected socket to target
                '''

                # default to doing nothing.
                pass


