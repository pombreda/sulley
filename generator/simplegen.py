#!/usr/bin/python

import binascii
from struct import *

f = open("test.ppt")
out = open("outgen.py", "w")
data = f.read()

out.write("""from sulley import *
s_initialize(\"gen\")
""")

i = len(data)
x = 0
while (x < i) :
        slice = data[0:calcsize('i')]
        data = data[calcsize('i'):]
        (value) = unpack('i', slice)
        out.write("s_int(%d)\n" % value)
        x += calcsize('i')

