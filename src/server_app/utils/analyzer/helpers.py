from bdb import Bdb


class RecursionDetected(Exception):
    pass


class RecursionDetector(Bdb):
    def do_clear(self, arg):
        pass

    def __init__(self, *args):
        Bdb.__init__(self, *args)
        self.stack = set()

    def user_call(self, frame, argument_list):
        code = frame.f_code
        if code in self.stack:
            raise RecursionDetected
        self.stack.add(code)

    def user_return(self, frame, return_value):
        self.stack.remove(frame.f_code)
