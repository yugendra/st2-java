from st2common.runners.base_action import Action
from ssh_client.ssh import SSH

class sendFile(Action):
    def run(self, host=None, source=None, destination=None):
        self.host = host
        self.source = str(source)
        self.destination = destination
        
        #exit_status, stderr = self._sendFile()
        status, file = self._sendFile()
        if status:
            return True, file
        else:
            return False, None
            
    def _sendFile(self):
        """
        Copy file to remote server
        """
        _conn = SSH(host=self.host)
        status, file = _conn.send_file(self.source, self.destination)
        _conn.close()
        return status, file