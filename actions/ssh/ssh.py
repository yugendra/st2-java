import paramiko
import time
import io
class SSH(object):

    def __init__(self,**kwargs):
        self._host = kwargs.pop('host')
        self._method = kwargs.pop('method', 'telnet')
        self._auth = kwargs.pop('auth', (None, None))
        self._enable = kwargs.pop('enable', None)
        self._port = kwargs.pop('port',22)
        self._client=None
        self._args={}
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:

            self._client.connect(self._host, username=self._auth[0], password=self._auth[1], look_for_keys=False, allow_agent=False,port=self._port,timeout=15)

            self._client_conn = self._client.invoke_shell()
            print ("Connection established to the host:%r"%self._host)
            time.sleep(0.5)
            self.output = self.recv()
            #print "initial out print\n"
            #print self.output

            if ">" in self.output:
                self._client_conn.send("en\n")
                self.output = self.recv()
                self._client_conn.send(self._args['enable'] + "\n")
                self.output = self.recv()

            while True:
                if "Network OS is not ready" in self.output:
                    #print ("SSH network not ready output\n")
                    #print self.output
                    print ("SSH:Waiting till Network OS is ready")
                    time.sleep(30)
                    self._client_conn.send("\n")

                    self.output = self.recv()
                    #print ("outptut in ssh os not ready\n")
                    #print self.output
                else:
                    break




            # Check for error
            if "incorrect" in self.output:
                raise Exception('Incorrect authentication details')

            # We should be in enable at this point
            if "#" in self.output:
                self._client_conn.send("\n")
                self.output = self.recv()
                self._hostname = self.output.translate(None, '\r\n')
                self._client_conn.send("terminal length 0\r\n")
                self.output = self.recv()
            else:
                self._client_conn.send("\n")
                self.output = self.recv()
                self._hostname = self.output.translate(None, '\r\n')
                self._client_conn.send("terminal length 0\r\n")
                self.output = self.recv()

            #print "output in hostanme\n"
            #print self.output
            #print("hostname\n")
            #print self._hostname

        except Exception, err:

            print ('ERROR for host %s - %s\n:' % (self._host, err))
            return

    def send(self,command):
        self._output = ''
        #print "in send"
        #print self.connected
        if self.connected:
            self._client_conn.send("\r\n")
            # print("DEBUG: Hostname is \n%s" % self._hostname)
            self.recv('#')
            self._client_conn.send("%s\r\n" % command)

            self._temp_line = self.recv("#")
            self._response = self._temp_line
            self._temp_data = io.BytesIO(self._response)
            self._output = self._temp_data.readlines()


        else:
            print "Channel is not open"
        return self._output

    @property
    def connected(self):
        if self._client.get_transport().is_active() and \
                        self._client.get_transport() is not None:

            return True
        else:
            return False


    def recv(self,*args):
        _output = ""
        _block = True
        _count = 1

        while _block:
            if not args:
                _block = False

            if _count >= 2:
                _block = False


            while not self._client_conn.recv_ready():
                time.sleep(0.1)
            while self._client_conn.recv_ready():
                time.sleep(0.3)
                _output += self._client_conn.recv(1000000)
                _count += 1
            if args:
                for _arg in args:
                    if _arg or "[y/n]" or "y" in _output:
                        _block = False
        return _output

    def read(self,command):

        _returnlist = []
        self._client_conn.send(command + "\n")
        time.sleep(3)
        self.output = self.recv(self._hostname)
        stream = io.BytesIO(self.output)
        self.count = 0
        #print "in the read funftion"
        #print self.output
        while self.count < 1:
            stream.readline()
            self.count += 1

        _lines = stream.readlines()
        for line in _lines:
            if line != '\r\n' and line != self._hostname:
                line = line.translate(None, '\r\n')
                if line != command:
                    _returnlist.append(line)
        return _returnlist

    @property
    def hostname(self):
        return self._hostname

