"""
This is a class for running command/function for hosts
"""
import logging
import os
import time
import command
import flex_env

class host(object):

    """Host class represent node.
    Attributes:
    hostname: name of node
    If this information could not be obtained, system_information may be None
    """

    def __init__(self, hostname, username=flex_env.ROOT_USER,
                 password=flex_env.ROOT_PWD, get_sys_info=True):

        self.logging = logging.getLogger('host')
        self.logging.addHandler(logging.NullHandler())

        self.system_information = None
        self.nic_list = None

        if not hostname:
            raise Exception('Host argument is not passed')

        self.hostname = hostname.strip()
        self.root_user = username
        self.root_password = password
        self.ipaddr = None

        if get_sys_info:
            self.get_system_information()
            if self.system_information != None:
                self.nodename = self.system_information['node']

    def run_cmd(self, cmd, cmd_args, stdin=None,
                timeout=180, ignore_failure=False, background=False):

        """Runs the given command on this host.
        @params:
            - cmd: command to run
            - cmd_args (list): arguments to pass to command to run
            - username: username to log to host, by default root will be used
            - password: password to log to host (this is optional)
            - pkey_filename: public key filename (this is optional)
            - stdin: stdin to pass to command ( this is optional )
            - timeout: timeout set for command, this is set to 3mns by default
            - ignore_failure: if set to True, exception will not be raised
                               when command return non-zero)
            - background: if set to True, command will be left running in the
                               background
        @Returns: a dictionary with following keys:
            - returncode,
            - stdout,
            - stderr
        @Raises: raise VXCTFException, Exception to caller
        """

        if cmd:
            cmd = cmd.strip()
            if len(cmd) > 0:
                try:
                    return command.run_cmd(
                        host=self.hostname,
                        cmd=cmd, cmd_args=cmd_args,
                        username=self.root_user, password=self.root_password,
                        timeout=timeout, stdin=stdin,
                        ignore_failure=ignore_failure,
                        background=background)
                except Exception as exc:
                    self.logging.error(str(exc))
                    raise
        else:
            self.logging.error('Command is an empty string!')

    def reboot(self, graceful=True, wait=True):
        '''
        This function will reboot the host
        :param self:
        :param graceful: Set to true if the reboot need to be graceful.
        :param wait: Set to True if we need to wait for machine to come up after reboot.
        :return: Returns True if reboot successfully done.
        '''

        if graceful:
            self.run_cmd('reboot', [], background=True, ignore_failure=True)
        else:
            self.logging.info('Non-Graceful reboot of host')
            self.run_cmd('reboot', ['-f'], background=True, ignore_failure=True)
        if wait:
            rflag = False
            self.logging.info('Waiting for some time for reboot to happen')
            time.sleep(60)
            count = 0
            self.logging.info('Will do 10 attempts after each minute before reboot check terminate')
            while count < 10:
                count += 1
                pingok = os.system("/bin/ping -c 1 " + self.hostname + " >/dev/null")
                if pingok == 0:
                    try:
                        self.run_cmd("/bin/hostname", [], timeout=10)
                        self.logging.info('Successfully did SSH to machine')
                        rflag = True
                        break
                    except:
                        pass
                time.sleep(60)
            return rflag
        else:
            self.logging.info('Reboot without waiting for machine to come up')
            return True
