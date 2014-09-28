import re
import socket

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
