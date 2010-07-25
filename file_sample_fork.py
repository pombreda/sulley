#!/usr/bin/python

from sulley   import *
from requests import http
import os

#Multi threaded file fuzzing example

executor = executors.fuzzExecutorFileNix.fuzzExecuteFileNix("./fuzz",
"cat FUZZED_INPUT_FILE >RANDOM_STR.out")
sess                   = sessions.session(executor, session_filename="audits/file_sample_mt.session")
target                 = sessions.target("localhost")

sess.add_target(target)
sess.connect(sess.root, s_get("HTTP HEADERS"))

pool = sessions_fork.session_fork(sess)
pool.fuzz(2)

#sess.fuzz() <- dont do this for mt fuzzing
