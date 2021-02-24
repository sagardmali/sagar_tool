"""
Methods for  ssh operations
"""
import re
from SSHLibrary import SSHLibrary

class Sshoperation(object):
    """
    Sshoperation class
    """
    def __init__(self, timeout=60, newline='LF', prompt='#'):
        """
        Constructor
        """
        self.ssh_agent = SSHLibrary(timeout, newline, prompt)
        self.prompt = prompt

    def ssh_login(self, host, username='root', password='P@ssw0rd'):
        """
        Login wrapper
        """
        self.ssh_agent.open_connection(host)
        self.ssh_agent.login(username, password)

    def ssh_logout(self):
        """
        Logout wrapper
        """
        self.ssh_agent.close_connection()

    def ssh_write(self, text):
        """
        Builtin write wrapper
        """
        return self.ssh_agent.write(text)

    def ssh_read_until_prompt(self):
        """
        Read until prompt wrapper
        """
        return self.ssh_agent.read_until_regexp(self.prompt)

    def ssh_read_until_regexp(self, regexp):
        """
        Read until regex wrapper
        """
        return self.ssh_agent.read_until_regexp(regexp)

    def issue_system_cmd(self, system, cmd, check_ret=1):
        """
        Execute a system command and verify 0 status with $?
        `cmd` : a complete ssh command
        `params`:
            - 'cmd', the command string to execute
        Example:
        | Issue System Cmd | mkdir /tmp/tmp_folder |
        """
        self.ssh_login(system)
        self._write(cmd)
        self.read_until_prompt()
        if check_ret == 1:
            self._write("echo $?")
            output = self.read_until_prompt()
        self.ssh_logout()

    def check_is_regex_match(self, value, output):
        """
        Validate match, and return the match
        """
        match_obj = re.search(r'(%s)(\s|$)' %value, output)
        if match_obj:
            self._log("Found match for %s in output" %value)
            return match_obj.group(1)
        return None

    def change_prompt(self, new_prompt):
        """
        Change current prompt
        """
        self.prompt = new_prompt
