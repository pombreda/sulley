import os
import re
import sys
import zlib
import time
import socket
import threading

from sulley import sex
import fuzzExecutor

try:
        import ssl
        ssl_loaded = True
except ImportError:
        ssl_loaded = False

"""
Base class used to executed a fuzzed data set
Used by sessions.fuzz, default arguement is this class
To define non-socket type fuzzers derive from this class and change the sessions.fuzz arg

Exception note: throw a sex.error with retry set to True if a retry is wanted
Throw a normal exception or something else to fail without retry
"""

class fuzzExecuteSock (fuzzExecutor.fuzzExecute):
	def __init__(self, host, port, proto="tcp", bind=None, timeout=5.0):
		self.proto = proto
		self.bind = bind
                self.timeout = timeout
                self.host = host
                self.port = port

                if self.proto == "ssl" and ssl_loaded == False:
                    raise sex.error("SSL not available on this system")
                elif self.proto == "tcp":
                    self.proto = socket.SOCK_STREAM

                elif self.proto == "ssl":
                    self.proto = socket.SOCK_STREAM
                    self.ssl   = True

                elif self.proto == "udp":
                    self.proto = socket.SOCK_DGRAM

                else:
                    raise sex.error("INVALID PROTOCOL SPECIFIED: %s" % self.proto)

        #close any open fd/socks and clean up any mess
        def destroy(self):
                if self.sock:
                        self.sock.close()

        def initFuzz(self):
                # establish a connection to the target.
                self.sock = socket.socket(socket.AF_INET, self.proto)

                if self.bind:
                        self.sock.bind(self.bind)

                try:
                        self.sock.settimeout(self.timeout)
                        self.sock.connect((self.host, self.port))
                except Exception, e:
                        raise sex.error( repr(e) + "failed connecting on socket" + self.host, True) #retry

                # if SSL is requested, then enable it.
                if self.ssl:
                      try:
                              self.sock = ssl.wrap_socket(self.sock)
                      except Exception, e:
                              raise sex.error(repr(e) + "failed ssl setup" + self.host, True) #retry

                # if the user registered a pre-send function, pass it the sock and let it do the deed.
                try:
                        self.pre_send()
                except Exception, e:
                        raise sex.error(repr(e) + "pre_send() failed" + self.host, True) #retry

        #to allow buffering in writeFuzz, we signal end of nodes by calling flush
        def flushFuzz(self):
                pass

        #This may buffer it or write it out, depends on the fuzzExecute class
        def writeFuzz(self, data):
                # if data length is > 65507 and proto is UDP, truncate it.
                # XXX - this logic does not prevent duplicate test cases, need to address this in the future.
                if self.proto == socket.SOCK_DGRAM:
                    # max UDP packet size.
                    # XXX - anyone know how to determine this value smarter?
                    MAX_UDP = 65507

                    if os.name != "nt" and os.uname()[0] == "Darwin":
                        MAX_UDP = 9216

                    if len(data) > MAX_UDP:
                        print("Too much data for UDP, truncating to %d bytes" % MAX_UDP)
                        data = data[:MAX_UDP]

                try:
                    self.sock.send(data)
                except Exception, inst:
                    print("Socket error, send: %s" % inst[1])

                last_recv = ""
                if self.proto == socket.SOCK_STREAM or socket.SOCK_DGRAM:
                    # XXX - might have a need to increase this at some point. (possibly make it a class parameter)
                    try:
                        last_recv = self.sock.recv(10000)
                    except Exception, e:
                        last_recv = ""

                return last_recv

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


