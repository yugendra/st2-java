from st2common.runners.base_action import Action
from ssh_client.ssh import SSH

class downloadFile(Action):
    def run(self, host=None, downloadURL=None):
        self.host = host
        self.downloadURL = downloadURL
        
        exit_status, stderr = self._downloadFile()
        if exit_status != 0:
            return(False, stderr)

        return True
            
    def _downloadFile(self):
        """
        Download file on remote server
        """
        #cmd = "wget " + self.downloadURL + " -P " + self.downloadPath
        cmd = "curl -o /tmp/java.rpm " + self.downloadURL
        _conn = SSH(host=self.host)
        exit_status, stdout, stderr=_conn.exec_command(cmd)
        _conn.close()
        return exit_status, stderr