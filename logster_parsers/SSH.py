#Monitors ssh login failures from /var/log/auth.log
from logster_parsers.BaseParsers import BaseParser

class FailedPassword(BaseParser):
    def __init__(self, option_string=None):
        self.reg = r".*sshd.*Failed password for.*"
        self.name = "ssh.invalid_user"
        self.description = "Failed SSH login for an invalid user"
        super(FailedPassword, self).__init__()

class PortScan(BaseParser):
    def __init__(self, option_string=None):
        self.reg = r".*sshd.*(Did not receive identification|Connection closed by).*"
        self.name = "ssh.port_scan"
        self.description = "Did not receive identification or connection closed"
        super(PortScan, self).__init__()
