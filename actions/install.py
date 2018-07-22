from st2common.runners.base_action import Action
from ssh import SSH

class installJava(Action):
    def run(self, host=None, username=None, password=None, installed_versions=None, required_version="java-1.8.0"):
        """
        Install the JAVA
        """
        self.host = host
        self.auth = (username, password)
        self.installed_versions = installed_versions
        self.required_version = required_version
        
        if self._isReqVerInstalled():
            return(True, "JAVA is already at required version")
        
        exit_status, stderr = self._remove_older()
        if exit_status != 0:
            return(False, stderr)

        exit_status, stderr = self._install_java()
        if exit_status != 0:
            return(False, stderr)
        
        return True
            
    def _install_java(self):
        """
        Install latest version of JAVA
        """
        cmd = "yum install -y " + self.required_version
        _conn = SSH(host=self.host,auth=self.auth)
        exit_status, stdout, stderr=_conn.exec_command(cmd)
        return exit_status, stderr
        
    
    def _remove_older(self):
        """
        Keep one latest version and remove rest of JAVA installations.
        """
        _conn = SSH(host=self.host,auth=self.auth)
        for i in range(1,len(self.installed_versions)):
            cmd = "yum remove -y " + self.installed_versions[i]
            exit_status, stdout, stderr = _conn.exec_command(cmd)
            if exit_status != 0:
                return exit_status, stderr
        return 0, None
        
    def _isReqVerInstalled(self):
        if self.required_version in self.installed_versions[0]:
            return True
        else:
            return False