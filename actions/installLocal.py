from st2common.runners.base_action import Action
from ssh_client.ssh import SSH

class installJavaLocal(Action):
    def run(self, host=None, rpm_file=None, installed_versions=[]):
        """
        Install the JAVA
        """
        self.host = host
        self.rpm_file = rpm_file
        self.installed_versions = installed_versions
        
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
        cmd = "yum install -y " + self.rpm_file
        _conn = SSH(host=self.host)
        exit_status, stdout, stderr=_conn.exec_command(cmd)
        _conn.close()
        return exit_status, stderr
        
    
    def _remove_older(self):
        """
        Keep one latest version and remove rest of JAVA installations.
        """
        _conn = SSH(host=self.host)
        for i in range(0,len(self.installed_versions)):
            cmd = "yum remove -y " + self.installed_versions[i]
            exit_status, stdout, stderr = _conn.exec_command(cmd)
            if exit_status != 0:
                return exit_status, stderr
        _conn.close()
        return 0, None
        
    def _isReqVerInstalled(self):
        if self.required_version in self.installed_versions[0]:
            return True
        else:
            return False