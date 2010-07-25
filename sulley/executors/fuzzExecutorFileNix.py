import os
import re
import sys
import zlib
import time
import socket
import threading
import signal
import os

from sulley import sex
import tempfile
import random
import fuzzExecutor
import subprocess
import shutil

"""
Executor class that will can be used to fuzz a file parsing binary
TODO: extend this class if pipes and interaction with the child proc are necessary
"""

#corresponding cmdFormatStr: "/bin/targetbin -switch FUZZED_INPUT_FILE /outfilebasepath/RANDOM_STR.gif -switch2"
RANDOM_STR = "RANDOM_STR"
FUZZED_INPUT_FILE = "FUZZED_INPUT_FILE"

class fuzzExecuteFileNix (fuzzExecutor.fuzzExecute):
	def __init__(self, tmpdir, cmdStr, timeout=10, crashsaves="/crash_inputs/", sleepinterval=.1 ):
                self.timeout = timeout
		self.sleepinterval = sleepinterval
                self.cmdStr = cmdStr
                self.tmpdir = tmpdir
                self.tmpname = None
                self.file = None
                self.pid = None
                self.crashsaves = tmpdir + crashsaves
		try:
	                os.makedirs(self.crashsaves)
		except:
			print "mkdir failed ", self.crashsaves
                random.seed()

        #close any open fd/socks and clean up any mess
        def destroy(self):
                if self.file:
                        self.file.close()
                if self.tmpname:
                        os.remove(self.tmpname)
                if self.pid:
                        os.kill(self.pid, signal.SIGKILL)

        def initFuzz(self):
                (fd, self.tmpname) = tempfile.mkstemp(suffix="fuzzy", dir=self.tmpdir)
                self.file = os.fdopen(fd, "wr") 

        #flush the file and execute
        def flushFuzz(self):
                self.file.flush()
                self.file.close()
                self.file = None
                rand = "%f" % random.random()
                cmd = self.cmdStr
                cmd = str.replace(cmd, RANDOM_STR, rand)
                cmd = str.replace(cmd, FUZZED_INPUT_FILE, self.tmpname)
                print "CMDSTR: ", cmd 
                p = subprocess.Popen(['/bin/sh', '-c', cmd])
                x = 0
                while x < self.timeout :
                        x += self.sleepinterval
                        if p.poll() ==  None:
                                time.sleep(self.sleepinterval)
                        else:
                                break
                if x >= self.timeout and p.returncode == None:
			print "Timeout detected, killing process"
                        p.kill()
                elif p.returncode != 0: #todo allow user to set what signals, not just all
                        print "Crash by signal detected, returncode: ", p.returncode
                        shutil.copyfile(self.tmpname, self.crashsaves)
                else:
			print "return code: ", p.returncode        
                        
        #This buffers 
        def writeFuzz(self, data):
                self.file.write(data)
                return ""
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


