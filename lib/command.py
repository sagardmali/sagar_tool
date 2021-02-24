"""
This module provides library to execute commands on a given host
"""
import datetime
import logging
import os
import socket
import subprocess
import paramiko
import flex_env

logger = logging.getLogger('command')
logger.addHandler(logging.NullHandler())

def run_cmd(host, cmd, cmd_args=None, username=flex_env.ROOT_USER,
            password=None, pkey_filename=None,
            stdin=None, timeout=300, ignore_failure=False, background=False, log=True):

    """Runs the given command on give host.

    Connection to remote host can be done via:
    - username/password authentication or
    - public key authentication

    @Arguments:
        - <host>:Host object: host to run command on.
        - <cmd>:str: command to run.
        - [cmd_args]:list|str: command arguments if any.
        - [stdin]:str: input to stdin if required.
        - [username]:str: username to access to remote host,
                          by default root user will be used
        - [password]:str: password to access to remote host.
        - [pkey_filename]:str: a private key filename to authenticate with
          If neither password of private key provided,
          Attempts to connect without any authentication, if failed
          Attempts to authenticate with all files in <user_home>/.ssh

        - [timeout]:int: set timeout for command ( default value is 120 seconds )
        - [ignore_failure]:boolean: flag to indicate whether or
                                    not to ignore failure.

    @Returns: a dictionary with following keys:
        - returncode:int: return code of executed command
        - stdout:str
        - stderr:str
        None if connection failed

    @Raises: raise Exception incase of connection fails
                  unless ignore_failure flag is set
    @Examples:
        run_cmd(cmd='umount', cmd_args=['-f', '/mnpt1'], host='myhostname')

    """

    if not host:
        raise Exception("Hostname is required!")

    if not cmd:
        logger.error("Command is an empty string!")
        raise Exception("Command is an empty string!")

    res = {
        'returncode:wq': -1,
        'stdout': '',
        'stderr': '',
        'logstr': ''}

    log_str = ''
    try:
        res['host'] = host
        res['username'] = username
        log_str = ''.join([log_str, "\nHostname: ", str(host), "\n"])
        log_str = ''.join([log_str, "User: ", username, "\n"])

        if cmd_args is not None:
            if isinstance(cmd_args, list):
                for arg in cmd_args:
                    cmd = ' '.join([cmd, str(arg)])
            else:
                cmd = ' '.join([cmd, str(cmd_args)])
        res['cmd'] = cmd
        log_str = ''.join([log_str, 'Command: ', cmd, "\n"])
        transport = connect_to_host(host=str(host), username=username,
                                    password=password,
                                    pkey_filename=pkey_filename)
        total_time = None

        if transport:
            session = transport.open_session()
            if session:
                try:
                    time_start = datetime.datetime.now()
                    session.exec_command(cmd.encode())
                    if stdin is not None:
                        if isinstance(stdin, bytes):
                            session.send(stdin)
                        else:
                            session.send(str(stdin).encode())

                    session.shutdown_write()
                    session.settimeout(timeout)

                except Exception as exc:
                    log_str = ''.join([log_str, 'Error', str(exc), '\n'])
                    if log:
                        logger.error(log_str)
                    raise

                else:
                    if not background:
                        exit_status = session.recv_exit_status()
                    time_end = datetime.datetime.now()
                    total_time = str(time_end - time_start)

    except Exception as exc:
        log_str = ''.join([log_str, 'Error', str(exc), '\n'])
        if log:
            logger.error(log_str)
            raise

    if background:
        return {'session' : session, 'transport' : transport}

    stdout_data = []
    stderr_data = []
    nbytes = 204800000000000000000

    while True:
        data = session.recv(nbytes)
        if not data:
            break
        stdout_data.append(data.decode('utf-8'))
    stdout_data = "". join(stdout_data)

    while True:
        err_str = session.recv_stderr(nbytes)
        if len(err_str) == 0:
            break
        stderr_data.append(err_str.decode('utf-8'))
    stderr_data = "". join(stderr_data)

    session.close()
    transport.close()

    log_str = ''.join([log_str, "Stdout:\n", stdout_data, "Stderr:\n", stderr_data])

    log_str = ''.join([log_str, "Return: ", str(exit_status), "\n"])
    if total_time is not None:
        log_str = ''.join([log_str, str("\nTime taken: " + total_time)])

    res['returncode'] = exit_status
    res['stdout'] = stdout_data
    res['stderr'] = stderr_data

    if log:
        logger.info(log_str)

    if exit_status != 0:
        if ignore_failure:
            if log:
                logger.warning('Command execution returns non-zero '
                               'exit code: %d, ignoring failure...',
                               exit_status)
            return res

        raise Exception('Command execution returns non-zero exit code: %d'
                        % (exit_status,))
    return res

def run_cmd_locally(cmd, cmd_args=None, stdin=None):
    """Runs command on localhost.

    @Arguments:
        - <cmd>:str: command to run
        - [cmd_args]:list|str: arguments to pass to command
                    (as a list of string consist of command and its argument)
        - [stdin]:str: input to command in case it needs from stdin

    @Returns: a tuple of:
        - popen:Popen object: resulting from command execution
        - output:str: command output
        - error:str: command error output
        None in case of exception occur

    @Raises: exception incase of error

    @Examples:

    """

    if isinstance(cmd, list):
        cmds = cmd
    elif isinstance(cmd, str):
        cmds = [cmd]

    if cmd_args is not None:
        if isinstance(cmd_args, list):
            cmds.extend(cmd_args)
        elif isinstance(cmd_args, str):
            cmds.append(cmd_args)

    popen = subprocess.Popen(cmds,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)

    if stdin is not None:
        popen.stdin.write(stdin.encode())

    (output, error) = popen.communicate()

    str_ = """
Host: %s
Command: %s

Stdout:
%s
Stderr:
%s
Returncode: %d
""" % (socket.gethostname(), ' '.join(cmds),
       output.decode(), error.decode(), popen.returncode)
    logger.info(str_)

    return (popen, output, error)

def connect_to_host(host, username=flex_env.ROOT_USER,
                    password=None, pkey_filename=None):

    """Return a transport object attached to a stream (mostly socket)

    @Arguments:
        - host
    @params: keyword arguments with folloing keys:
        username: username to connect to host,\
                  by default root user predefine in vxctf.constant will be used
        password: if provided, try to authenticate with password
        pkey_filename: if provided, try to authenticate with private key
        if neither of password, pkey_filename provided, try to authenticate
              - with no-authentication at all
              - if failed, try authenticate with private keys in home user

    @returns: Transport object
        None if authentication failed

    """

    if not host:
        logger.error("Host name is required")
        return None

    transport = None
    transport = paramiko.Transport((host, env.PORT))
    transport.connect(username=username)
    auth = False
    if password is not None:
        try:
            transport.auth_password(
                username=username,
                password=password,
                fallback=True)
        except Exception as exc:
            logger.error("Authentication failed. %s" %str(exc))
            return None

    elif pkey_filename is not None:
        return auth_with_pkey(transport, username, pkey_filename)

    else:
        try:
            transport.auth_none(username)
        except Exception:
            user_home = os.path.expanduser('~')
            if not os.path.exists(os.path.join(user_home, '.ssh')):
                return None

            for filename in os.listdir(os.path.join(user_home, '.ssh')):
                filename = os.path.join(user_home, '.ssh', filename)
                if auth_with_pkey(transport, username, filename):
                    auth = True
                    break
        if not auth:
            return None

    return transport

def _connect_to_host(host, username=flex_env.ROOT_USER, password=None,
                     pkey_filename=None, port=flex_env.PORT):

    """Return a transport object attached to a stream (mostly socket)

    @params: host
    @params: keyword arguments with folloing keys:
        username: username to connect to host,\
                  by default root user predefine in vxctf.constant will be used
        password: if provided, try to authenticate with password
        pkey_filename: if provided, try to authenticate with private key
        if neither of password, pkey_filename provided, try to authenticate
              - with no-authentication at all
              - if failed, try authenticate with private keys in home user

    @returns: Transport object
        None if authentication failed

    """

    if not host:
        logger.error("Host name is required")
        return None

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port,
                   username=username, password=password,
                   key_filename=pkey_filename)

    return client.get_transport()

def reboot(host, username, password,
           timeout=300, mount_lib=True):
    """Reboot a given host

    @params:
        - host: host to be rebooted
        - username: username to connect to host
        - password: password to access to remote host
        - pkey_filename: a private key filename to authenticate with
        If neither password of private key provided,
        Attempts to authenticate with all file in <user_home>/.ssh

        - timeout: timeout set for reboot command
        (the defaults value is 180seconds, on top of 120 seconds in run_cmd)

    """

    if not host:
        logger.error("Host name is required, provide with 'host' keyword")
        return None

    last_system_boot_time = get_last_system_boot_time(host=host,
                                                      username=username,
                                                      password=password,
                                                      pkey_filename=pkey_filename,
                                                      timeout=timeout)

    logger.debug('System last boot time: ', last_system_boot_time)
    logger.info('Start executing: reboot')

    res = run_cmd(host=host, cmd='reboot', cmd_args=None, username=username,
                  password=password,
                  timeout=timeout, ignore_failure=True)

    curr_boot_time = last_system_boot_time
    counter = (timeout / 60)

    while ((curr_boot_time == last_system_boot_time) and (counter > 0)):
        try:
            curr_boot_time = get_last_system_boot_time(host=host,
                                                       username=username,
                                                       password=password,
                                                       pkey_filename=pkey_filename,
                                                       timeout=timeout)
            logger.info("System is not yet Up.. Waiting for 1 min more..")
            time.sleep(60)
            counter = counter - 1
        except Exception:
            time.sleep(60)

    logger.info('System is rebooted, system last boot time: %s', curr_boot_time)

    return res


def get_last_system_boot_time(host, username, password,
                              pkey_filename, timeout):
    """
    Get last system boot time of given host.  Returns the last system
    boot time.
    """
    if not host:
        logger.error("Hostname is required")
        return None

    last_boot = ''
    res = run_cmd(host=host, cmd='who', cmd_args=['-b'],
                  username=username, password=password,
                  pkey_filename=pkey_filename,
                  ignore_failure=True)

    if res['returncode'] == 0:
        last_boot = res['stdout'].strip()

    return last_boot
