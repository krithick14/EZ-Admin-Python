import os
from datetime import datetime
class Backup:
    def backup(self):
        now = datetime.now()
        file = open('logs.txt', 'a+')
        try:
            backup_command = "mkdir -p /home/$USER/backup_server && cd /var/www/html &&  sudo tar -cpf /home/$USER/backup_server/backup_$(date +%F).tar.gz ./* && sudo chown $USER /home/$USER/backup_server/backup_$(date +%F).tar.gz > /dev/null"
            exit_code = os.system(backup_command)
            if exit_code != 0:
                raise Exception
        except Exception:
            return 1
        else:
            file.write("Server Files Backed up by " +os.environ['USER'].strip()+" on " + now.strftime('%Y-%m-%d %H:%M:%S')+".\n")
        file.close()
        return 0
