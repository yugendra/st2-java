from st2common.runners.base_action import Action
from ssh import SSH

class downloadFile(Action):
    def run(self, host=None, username=None, password=None, downloadURL=None, downloadPath=None):
        self.host = host
        self.auth = (username, password)
        self.downloadURL = downloadURL
        self.downloadPath = downloadPath
        
        exit_status, stderr = self._downloadFile()
        if exit_status != 0:
            return(False, stderr)

        return True
            
    def _downloadFile(self):
        """
        Download file on remote server
        """
        cmd = "wget " + self.downloadURL + " -P " + self.downloadPath
        _conn = SSH(host=self.host,auth=self.auth)
        exit_status, stdout, stderr=_conn.exec_command(cmd)
        return exit_status, stderr