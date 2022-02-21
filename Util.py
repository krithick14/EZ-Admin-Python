import os
import getpass
import pyfiglet
from datetime import datetime
import ipaddress

class Util:
    def __init__(self):
        now = datetime.now()
        self.time=now.strftime("%d/%m/%Y %H:%M:%S")
        self.now = datetime.now()
        self.file = open('logs.txt', 'r')

    def __del__(self):
            self.file.close()

    def validate_ip_address(self,address):
        try:
            self.ip = ipaddress.ip_address(address)
            return True;
        except ValueError:
            return False 

    def validate_date(self,date):
        try:
            day,month,year=date.split('/')
        except:
            return False
        else:
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

            if int(day) > 0 and int(day) <= 31:
                    if month.capitalize() in months:
                        if len(year) == 4:
                            return True
            return False;

    def view_logs(self):
        os.system("clear")
        os.system("figlet -c Server - Logs")
        lines = self.file.readlines()
        for line in lines:
            print("\t"+line)
        

    def clear_logs(self):
        self.attempt=0;
        while (self.attempt != 3):
            self.password="admin123"
            self.temp=""
            self.temp = getpass.getpass("\n\tEnter Password : ")
            if self.temp==self.password:
                self.file = open("logs.txt", "w")
                self.file.write("Server Logs Cleared by " + os.environ['USER'].strip()+" on "+ self.time+".\n")
                self.file.close()
                print("\n\tServer Logs Cleared Sucessfully")
                print("\n\tServer Logs Cleared by " + os.environ['USER'].strip()+" on "+ self.time+".\n")
                break
            else:
                self.attempt+=1;
                print("\n\tInvalid Password")
                if self.attempt == 3:
                    print("\n\n\tMAX ATTEMPTS REACHED\n")
                    exit(1)