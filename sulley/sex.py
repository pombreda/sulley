# Sulley EXception Class
"""
Dont over use this exception class
Current usage includes: signaling to caller that a retry is acceptable
"""


class error (Exception):
    def __init__ (self, message, retry=False):
        self.value = message
        self.retry = retry

    def __str__ (self):
        return repr(self.value)

    def __repr__(self):
        return "value " +self.value + " retry: " + repr(self.retry)
