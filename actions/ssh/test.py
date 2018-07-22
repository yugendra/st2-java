from ssh import SSH

_conn =  SSH(host="192.168.137.104",auth=("root", "devops123"))
print(_conn.send("ls"))