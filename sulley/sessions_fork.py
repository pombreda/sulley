import os
import re
import sys
import time
import socket
import cPickle
import threading
import copy

import sessions
import pedrpc
import sex
from executors import * 

########################################################################################################################
class session_fork:
    def __init__ (self, session_orig):
        self.session_orig = session_orig
        if not isinstance(self.session_orig, sessions.session):
               raise sex.error("session_orig is not of type session")

    def fuzz(self, number_procs=4):
        print "Initializing child processes"
	child_pids = []
        for childId in range(number_procs):
                self.session_orig.percent_start = (1.0/number_procs) * childId
                self.session_orig.percent_end = (1.0/number_procs) * (childId+1)
                self.session_orig.session_filename = self.session_orig.session_filename + "_ChildID%d" % childId
		pid = os.fork() #not available on windows
		if pid != 0:
	                child_pids.append(pid)
		else:
			self.session_orig.fuzz()
			sys.exit(0)

        print "Initialized %d child procs..." % number_procs

        for pid in child_pids:
		os.waitpid(pid, 0)
                print "Child with pid: %d ended" % pid

        print "All procs finished\n"


    ####################################################################################################################
    def log (self, msg, level=1):
        '''
        If the supplied message falls under the current log level, print the specified message to screen.

        @type  msg: String
        @param msg: Message to log
        '''

        if self.log_level >= level:
            print "[%s] %s" % (time.strftime("%I:%M.%S"), msg)


