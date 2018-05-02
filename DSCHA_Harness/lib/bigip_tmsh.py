import logging
import signal
import re
import prctl
from threading import Thread
from subprocess import Popen, PIPE

log = logging.getLogger("TMSH Utils")

SSH_CMD = ("ssh -q -n -o StrictHostKeyChecking=no -o CheckHostIP=no "
           "-o UserKnownHostsFile=/dev/null -o ConnectionAttempts=15 ")
ANSI_ESCAPE = re.compile(r"(\x1b\[|\x9b)[0-?]*[ -\/]*[@-~]|\x0f", re.I)


def add_return_attrs(fn):
    """Decorator to add helpful attributes to the returned tuple.

    Example:
        stdout = runcmd_ssh(<bigip>, <cmd>).stdout
    """
    def wrapped(*args, **kwargs):
        class ret_tuple(tuple):
            rc = 2
            stdout = "ERROR: not set."
            stderr = "ERROR: not set."
            actual_time = -1

        ret = ret_tuple(fn(*args, **kwargs))
        ret.rc = ret[0]
        ret.stdout = ret[1]
        ret.stderr = ret[2]
        if len(ret) == 4:
            ret.actual_time = ret[3]

        return ret

    return wrapped


@add_return_attrs
def runcmd(cmd, raise_err=False, log=None):
    """Run given command.

    Return tuple of (RC, stdout, stderr)."""
    execprocess = Popen([cmd],
                        stdout=PIPE,
                        stderr=PIPE,
                        # if parent process dies, child procs do also
                        preexec_fn=lambda: prctl.set_pdeathsig(signal.SIGKILL),
                        shell=True)
    (stdout, stderr) = execprocess.communicate()
    returncode = execprocess.returncode
    stdout = ANSI_ESCAPE.sub('', stdout.decode('utf-8'))
    stderr = ANSI_ESCAPE.sub('', stderr.decode('utf-8'))

    # Start from new line for easy reading of the log output:
    msg = ("\nCOMMAND: %s\nSTDOUT: %s\nSTDERR: %s\nRETURNCODE=%d" %
           (cmd, stdout or "",
            stderr or "",
            returncode)).replace(SSH_CMD, "ssh")

    if raise_err and execprocess.returncode:
        err = "Command failed: {}".format(msg)
        raise Exception(err)

    if log:
        log.debug(msg)

    return (returncode, stdout, stderr)


def _process_stream(stream, func):
    """Supplimentary thread function for runcmd_live().
    """
    for line in iter(stream.readline, b''):
        func(line.rstrip())
    stream.close()


def runcmd_live(cmd, stdout=log.info, stderr=log.error, raise_err=False):
    """Run given command and pass stdout and stderr lines immediately
    to provided functions (one call per one line.)
    """
    execprocess = Popen([cmd],
                        stdout=PIPE,
                        stderr=PIPE,
                        bufsize=1,
                        close_fds=True,
                        shell=True)
    stdout_thread = Thread(target=_process_stream,
                           args=(execprocess.stdout, stdout))
    stderr_thread = Thread(target=_process_stream,
                           args=(execprocess.stderr, stderr))
    stdout_thread.start()
    stderr_thread.start()
    stdout_thread.join()
    stderr_thread.join()

    rc = execprocess.wait()

    if raise_err and rc:
        err = "Command `%s' failed (status=%d)" % (cmd, rc)
        raise Exception(err)

    return rc


def runcmd_ssh(address, cmd, username='root', password='default', log=log, raise_err=False,
               delim='"', verbose=False, force_tty=False, extra_opts=''):
    """Run command via ssh given username and remote address.

    Return tuple of (RC, stdout, stderr)."""
    sshpass_cmd = 'sshpass -p "%s" ' % password
    sshcmd = SSH_CMD
    if force_tty:
        # Force pseudo-tty allocation:
        sshcmd += "-tt "
    sshcmd += extra_opts

    cmd = '%s@%s %s%s%s' % (username, address, delim, cmd, delim)
    if log:
        log.info("Running ssh command:")
        log.info("ssh " + cmd)

    return runcmd(
        "{} {}".format(sshpass_cmd + sshcmd, cmd), raise_err, log if verbose else None)