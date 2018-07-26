from paramiko import SSHClient, AutoAddPolicy, RSAKey
import time
from os import path
from config import Config


class SSH(object):

    def __init__(self,**kwargs):
        self._host = kwargs.pop('host')
        self._key = RSAKey.from_private_key_file(Config.key)
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self._host, username=Config.username, password=self._key)
    
    def close(self):
        self.ssh.close()
        
    def exec_command(self, command):
        """
        Execute command on remote server
        """
        outdata, errdata = '', ''
        ssh_transp = self.ssh.get_transport()
        chan = ssh_transp.open_session()
        chan.setblocking(0)
    
        chan.exec_command(command)
        while True:  # monitoring process
            # Reading from output streams
            while chan.recv_ready():
                outdata += chan.recv(1000)
            while chan.recv_stderr_ready():
                errdata += chan.recv_stderr(1000)
            if chan.exit_status_ready():  # If completed
                break
            time.sleep(1)
        retcode = chan.recv_exit_status()
        #ssh_transp.close()
        return retcode, outdata, errdata
        
    def send_file(self, src, dest):
        """
        Copy file to remote server
        """
        file_name = self._get_src_file_name(src)
        if self._check_dest_type(dest) == 0:
            full_dest_path = dest + "/" + file_name
        else:
            full_dest_path = dest
            
        ftp_client=self.ssh.open_sftp()
        ftp_client.put(src, full_dest_path)
        ftp_client.close()
        
        #check if file copied successfully
        retcode, outdata, errdata = self.exec_command("[ -f " + full_dest_path + " ]")
        if retcode == 0:
            return True, full_dest_path
        else:
            return False, None
        
    def _get_src_file_name(self, src):
        """
        Extract source file name from path
        """
        return path.basename(src)
        
    def _check_dest_type(self, dest):
        """
        check dest is file or folder
        """
        if dest[-1] == "/":
            return 0
        else:
            retcode, outdata, errdata = self.exec_command("[ -d " + dest + " ]")
            return retcode