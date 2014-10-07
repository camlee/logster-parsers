import re
import os
import socket
import pickle

from logster.logster_helper import MetricObject, LogsterParser, LogsterParsingException

class BaseParser(LogsterParser):
    """This class is intended to be inherited from. 
    self.reg, self.name, and self.description must be provided 
    by the child class.
    """

    def __init__(self, option_string=None):
        self.metric = 0
        self.reg_compiled = re.compile(self.reg)

    def parse_line(self, line):
        try:
            # Apply regular expression to each line and extract interesting bits.
            if self.reg_compiled.match(line):
                self.metric += 1

        except KeyboardInterrupt:
            raise
        except Exception as e:
            raise(LogsterParsingException(str(e)))


    def get_state(self, duration):
        return [
            MetricObject("%s.%s" % (socket.gethostname(), self.name), 
                         self.metric,
                         self.description),
        ]

class IncrementDecrementBaseParser(LogsterParser):
    """This class is intended to be inherited from. 
    self.reg_inc, self.reg_dec, self.name, and self.description 
    must be provided by the child class.

    This class will increment the metric upon finding a match for
    self.reg_inc and decrement it upon finding a match for self.reg_dec.
    """

    def __init__(self, option_string=None):
        self.state_file = "/var/lib/logster-parsers/IncrementParserState"
        if not os.path.exists(os.path.dirname(self.state_file)):
            os.makedirs(os.path.dirname(self.state_file))
        try:        
            with open(self.state_file, "rb") as f:
                state_dict = pickle.load(f)
        except (IOError, EOFError):
            state_dict = {}
            with open(self.state_file, "wb") as f:
                pickle.dump(state_dict, f)
        if self.name not in state_dict:
            self.metric = 0
        else:
            self.metric = state_dict[self.name]

        self.reg_inc_compiled = re.compile(self.reg_inc)
        self.reg_dec_compiled = re.compile(self.reg_dec)

    def parse_line(self, line):
        try:
            if self.reg_inc_compiled.match(line):
                self.metric += 1
            if self.reg_dec_compiled.match(line):
                self.metric -= 1
        except KeyboardInterrupt:
            raise
        except Exception as e:
            raise(LogsterParsingException(str(e)))

    def get_state(self, duration):
        with open(self.state_file, "rb") as f:
            state_dict = pickle.load(f)
        state_dict[self.name] = self.metric
        with open(self.state_file, "wb") as f:
            pickle.dump(state_dict, f)
        return [
            MetricObject("%s.%s" % (socket.gethostname(), self.name),
                         self.metric,
                         self.description),
        ]

   
