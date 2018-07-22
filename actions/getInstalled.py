from st2common.runners.base_action import Action
from ssh import SSH

class getInstallJavaVersions(Action):
    def run(self, host=None, username=None, password=None):
        """
        Install the JAVA
        """
        self._conn = SSH(host=host,auth=(username, password))
        exit_status, stdout, stderr=self._conn.exec_command("rpm -qa | grep java.*openjdk | grep -v headless | sort -r")
        output = []
        for version in stdout.split():
            output.append(version)
        
        if exit_status != 0:
            return(False, stderr)
        else:
            return(True, output)