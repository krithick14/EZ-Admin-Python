import os
from datetime import datetime



class Server:
    def status(self):
        self.stat = os.system("pgrep apache2 > /dev/null")
        if self.stat == 0:
            return True
        return False

    def start(self):
        now = datetime.now()
        file = open('logs.txt', 'a+')
        if not self.status():
            try:
                exit_code = os.system("sudo service apache2 start 2> /dev/null")
                if exit_code != 0:
                    raise Exception
            except Exception:
                file.write("Server Start Failed by " +
                os.environ['USER'].strip()+" on " + now.strftime('%Y-%m-%d %H:%M:%S')+".\n")
                return 1
            else:
                os.system("killall xterm  2> /dev/null")
                os.system("xterm -T Client_logs -fa 'Monospace' -fs 12 -e  watch \"tail -n 15 /var/log/apache2/access.log | cut -d \' \'  -f 1,4,5  | tr -s ' ' '\t'  \" & ")
                file.write("Server Started by " +
                os.environ['USER'].strip()+" on " + now.strftime('%Y-%m-%d %H:%M:%S')+".\n")
        file.close()
        return 0

    def stop(self):
        now = datetime.now()
        file = open('logs.txt', 'a+')
        if self.status():
            try:
                exit_code = os.system("sudo service apache2 stop 2> /dev/null")
                if exit_code != 0:
                    raise Exception
            except Exception:
                file.write("Server Stop Failed by " +
                os.environ['USER'].strip()+" on " + now.strftime('%Y-%m-%d %H:%M:%S')+".\n")
                return 1
            else:
                os.system("killall xterm  2> /dev/null")
                file.write("Server Stopped by " +
                os.environ['USER'].strip()+" on " + now.strftime('%Y-%m-%d %H:%M:%S')+".\n")
        file.close()
        return 0

    def restart(self):
        now = datetime.now()
        file = open('logs.txt', 'a+')
        try:
            exit_code = os.system("sudo service apache2 restart 2> /dev/null")
            if exit_code != 0:
                raise Exception
        except Exception:
            file.write("Server Restart Failed by " +
            os.environ['USER'].strip()+" on " + now.strftime('%Y-%m-%d %H:%M:%S')+".\n")
            return 1
        else:
            os.system("killall xterm  2> /dev/null")
            os.system("xterm -T Client_logs -fa 'Monospace' -fs 12 -e  watch \"tail -n 15 /var/log/apache2/access.log | cut -d \' \'  -f 1,4,5  | tr -s ' ' '\t'  \" & ")
            file.write("Server Restarted by " +
            os.environ['USER'].strip()+" on " +now.strftime('%Y-%m-%d %H:%M:%S')+".\n")
        file.close()
        return 0