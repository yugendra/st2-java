from paramiko import SSHClient, AutoAddPolicy
import time


class SSH(object):

    def __init__(self,**kwargs):
        self._host = kwargs.pop('host')
        self._method = kwargs.pop('method', 'telnet')
        self._auth = kwargs.pop('auth', (None, None))
        self._enable = kwargs.pop('enable', None)
        self._port = kwargs.pop('port',22)
        self._client=None
        self._args={}
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self._host, username=self._auth[0], password=self._auth[1])
        self.sleeptime = 0.001
        self.outdata, self.errdata = '', ''
        self.ssh_transp = self.ssh.get_transport()
        self.chan = self.ssh_transp.open_session()
        self.chan.setblocking(0)
        
    def exec_command(self, command):
        self.chan.exec_command(command)
        while True:  # monitoring process
            # Reading from output streams
            while self.chan.recv_ready():
                self.outdata += self.chan.recv(1000)
            while self.chan.recv_stderr_ready():
                self.errdata += self.chan.recv_stderr(1000)
            if self.chan.exit_status_ready():  # If completed
                break
            time.sleep(1)
        retcode = self.chan.recv_exit_status()
        self.ssh_transp.close()
        return retcode, self.outdata, self.errdata
        