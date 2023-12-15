import sys
import traceback


class MathError(Exception):
    def myexcepthook(type, value, tb):
        msg = ''.join(traceback.format_exception(type, value, tb))
        print(msg)
    
    sys.excepthook = myexcepthook