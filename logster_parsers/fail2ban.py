#Monitors fail2ban bans from /var/log/fail2ban.log
from logster_parsers.BaseParsers import BaseParser, IncrementDecrementBaseParser

class Ban(BaseParser):
    def __init__(self, option_string=None):
        self.reg = r".*WARNING.* Ban .*"
        self.name = "fail2ban.ban"
        self.description = "IP address banned."
        super(Ban, self).__init__()

class Unban(BaseParser):
    def __init__(self, option_string=None):
        self.reg = r".*WARNING.* Unban .*"
        self.name = "fail2ban.unban"
        self.description = "IP address removed from ban list."
        super(Unban, self).__init__()

class Banned(IncrementDecrementBaseParser):
    def __init__(self, option_string=None):
        self.reg_inc = r".*WARNING.* Ban .*"
        self.reg_dec = r".*WARNING.* Unban .*"
        self.name = "fail2ban.banned"
        self.description = "IP addresses currently on the ban list."

        super(Banned, self).__init__()
