#!/usr/bin/python

from sulley   import *
from requests import http
import os

#Single threaded file fuzzing example

executor = executors.fuzzExecutorFileNix.fuzzExecuteFileNix("./fuzz",
"od FUZZED_INPUT_FILE >RANDOM_STR.out")
sess                   = sessions.session(executor, session_filename="audits/file_sample.session")
target                 = sessions.target("localhost")

sess.add_target(target)
sess.connect(sess.root, s_get("HTTP HEADERS"))
sess.fuzz()

