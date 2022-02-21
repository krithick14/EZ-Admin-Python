import os
import subprocess as sp
from datetime import datetime
import tkinter as tk
from tkinter import *
from sys import exit
from tkinter import messagebox, Tk, simpledialog

from Backup import *
from Servers import *
from Util import *

now = datetime.now()
time = now.strftime("%d/%m/%Y %H:%M:%S")
now = datetime.now()

util=Util()
server=Server()
backup=Backup()

def status():
    stat = os.system("pgrep apache2 > /dev/null")
    if stat == 0:
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
        return True
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")
    return False

def get_status():
    stat = os.system("pgrep apache2 > /dev/null")
    if stat==0:
            return "Server Status : Active"
    else:
        return "Server Status : Inactive"

def start():
    if server.start()==0:
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
    else:
        messagebox.showerror('Something went wrong','Error in apache2')
    server_status.configure(text=get_status())

def stop():
    if server.stop()==0:
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")
    else:
        messagebox.showerror('Something went wrong','Error in apache2')
    server_status.configure(text=get_status())

def restart():
    if server.restart()==0:
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
    else:
        messagebox.showerror('Something went wrong','Error in apache2')
    server_status.configure(text=get_status())

def do_backup():
    if backup.backup() == 0:
        messagebox.showinfo("Backup", "Backup Saved at " + os.environ['HOME'].strip()+"/backup_server/")
    else:
        messagebox.showerror('Something went wrong :', 'Error in Taking Backup')

def view_logs():
    file = open('logs.txt', 'r')
    log_window = Toplevel(root)
    log_window.title("Server-Logs")
    log_window.geometry("800x800")
    data = file.read()
    txtarea = Text(log_window, width=750, height=750)
    if len(data)==0:
        txtarea.insert(END, sp.getoutput("figlet -c Server-Logs")+"\n\n"+"No Logs Found")
    else:
        txtarea.insert(END, sp.getoutput("figlet -c Server-Logs")+"\n\n"+data)
    txtarea.pack(pady=20)

def clear_logs():
    file=open('logs.txt','w');
    messagebox.showinfo("Clear-Logs", "Logs Cleared Sucessfully !!!")
    file.close()

def open_search_window():
    global search_window
    search_window=Toplevel(root)
    search_window.title("Search Client Logs")
    search_window.geometry("400x400")
    search_window.resizable(width=False, height=False)
    search_window.configure(bg='white')
    logo = Label(search_window, text="Search Menu", font=("courier", 30))
    logo.pack(padx=20, pady=50)
    logo.configure(bg='white', fg='black')
    frame = tk.Frame(search_window)
    frame.configure(bg='white')
    frame.pack()
    ip_search_btn = tk.Button(frame,
                      text="SEARCH WITH IP",
                      command=search_ip,
                      fg="black", bg='white',
                      activebackground='black',
                      activeforeground='white')
    ip_search_btn.pack(fill=tk.X, pady=15,)

    date_search_btn = tk.Button(frame,
                      text="SEARCH WITH DATE",
                      command=search_date,
                      fg="black", bg='white',
                      activebackground='black',
                      activeforeground='white')
    date_search_btn.pack(fill=tk.X, pady=15,)

    month_search_btn = tk.Button(frame,
                     text="SEARCH BY MONTH",
                     command=search_month,
                     fg="black", bg='white',
                      activebackground='black',
                      activeforeground='white')
    month_search_btn.pack(fill=tk.X, pady=15)

    exit_search_btn = tk.Button(frame,
                     text="EXIT",
                     command=search_window.destroy,
                     fg="black", bg='white',
                      activebackground='black',
                      activeforeground='white')
    exit_search_btn.pack(fill=tk.X, pady=15)


def search_ip():
    search_window.destroy()
    ip_search = simpledialog.askstring(title="Enter IP",prompt="Enter IP Address to Search : ")
    if ip_search==None:
        return
    if util.validate_ip_address(ip_search):
        result=sp.getoutput("cat /var/log/apache2/access.log | grep " + ip_search + " | awk \'{print \"\\t\" NR \"\\t\"$1 \"\\t\" $4 \" \" $5 }\' ")
        ip_window = Toplevel(root)
        ip_window.title("Logs")
        ip_window.geometry("800x800")
        txtarea = Text(ip_window, width=750, height=750)
        txtarea.pack()
        if len(result)==0:
            txtarea.insert(END,sp.getoutput("figlet -c LOGS")+ "\nNo Entry Found with IP : " + ip_search)
        else:
            txtarea.insert(END, sp.getoutput("figlet -c LOGS")+ "\n"+result)
    else:
        messagebox.showerror("Invalid IP","Invalid IP : "+ip_search)

def search_date():
    search_window.destroy()
    date_search = simpledialog.askstring(title="Enter Date",prompt="Enter Date in (10/Jan/2022) format to Search : ")
    if date_search==None:
        return

    if util.validate_date(date_search):
        result=sp.getoutput("cat /var/log/apache2/access.log | grep " + date_search + " | awk \'{print \"\\t\" NR \"\\t\"$1 \"\\t\" $4 \" \" $5 }\' ")
        date_search_window = Toplevel(root)
        date_search_window.title("Logs")
        date_search_window.geometry("800x800")
        txtarea = Text(date_search_window, width=750, height=750)
        if len(result)==0:
            txtarea.insert(END,sp.getoutput("figlet -c LOGS")+ "\nNo Entry Found on Date : " + date_search)
        else:
            txtarea.insert(END, sp.getoutput("figlet -c LOGS")+ "\n"+result)
        txtarea.pack()
    else:
        messagebox.showerror("Invalid Date","Invalid Date : "+date_search)

def search_month():
    search_window.destroy()
    month_search = simpledialog.askstring(title="Enter Month",prompt="Enter Month to Search (E.g: Jan,Sep): ")
    if month_search==None:
        return

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    if month_search.capitalize() in months:
        result=sp.getoutput("cat /var/log/apache2/access.log | grep " + month_search.capitalize() + " | awk \'{print \"\\t\" NR \"\\t\"$1 \"\\t\" $4 \" \" $5 }\' ")
        month_search_window = Toplevel(root)
        month_search_window.title("Logs")
        month_search_window.geometry("800x800")
        txtarea = Text(month_search_window, width=750, height=750)
        txtarea.pack()
        if len(result)==0:
            txtarea.insert(END,sp.getoutput("figlet -c LOGS")+ "\nNo Entry Found in Month : " + month_search)
        else:
            txtarea.insert(END, sp.getoutput("figlet -c LOGS")+ "\n"+result)
    else:
        messagebox.showerror("Invalid Month","Invalid Month : "+month_search)


def do_exit():
    os.system("killall xterm  2> /dev/null")
    exit(0)

root = Tk()
root.geometry('550x750')
root.resizable(width=False, height=False)
root.wm_title("EZ_ADMIN")
root.title("EZ_ADMIN")
root.configure(bg='black')

logo = Label(root, text="EZ-ADMIN", font=("courier", 40, "underline"))
logo.pack(padx=20, pady=30)
logo.configure(bg='black', fg='white')

ip = Label(root, text="Local IP : " + sp.getoutput("hostname -I | awk '{ printf $1 }' "), font=("courier", 20))
ip.pack(padx=20, pady=10)
ip.configure(bg='black', fg='white')

server_status = Label(root, text=get_status(), font=("courier", 20))
server_status.pack(padx=20, pady=10)
server_status.configure(bg='black', fg='white')

frame = tk.Frame(root)
frame.pack()
frame.configure(bg="black")

start_btn = tk.Button(frame,
                      text="START",
                      command=start,
                      bg="black", fg='white',
                      activebackground='white',
                      activeforeground='black')
start_btn.pack(fill=tk.X, pady=15)

stop_btn = tk.Button(frame,
                     text="STOP",
                     command=stop,
                     bg="black", fg='white',
                     activebackground='white',
                     activeforeground='black')
stop_btn.pack(fill=tk.X, pady=15)

restart_btn = tk.Button(frame,
                        text="RESTART",
                        command=restart,
                        bg="black", fg='white',
                        activebackground='white',
                        activeforeground='black')
restart_btn.pack(fill=tk.X, pady=15)


backup_btn = tk.Button(frame,
                       text="BACKUP",
                       command=do_backup,
                       bg="black", fg='white',
                       activebackground='white',
                       activeforeground='black')
backup_btn.pack(fill=tk.X, pady=15)

search__btn = tk.Button(frame,
                       text="SEARCH CLIENT LOGS",
                       command=open_search_window,
                       bg="black", fg='white',
                       activebackground='white',
                       activeforeground='black')
search__btn.pack(fill=tk.X, pady=15)

view_logs__btn = tk.Button(frame,
                       text="VIEW SERVER LOGS",
                       command=view_logs,
                       bg="black", fg='white',
                       activebackground='white',
                       activeforeground='black')
view_logs__btn.pack(fill=tk.X, pady=15)


clear_logs__btn = tk.Button(frame,
                       text="CLEAR SERVER LOGS",
                       command=clear_logs,
                       bg="black", fg='white',
                       activebackground='white',
                       activeforeground='black')
clear_logs__btn.pack(fill=tk.X, pady=15)

exit_btn = tk.Button(frame,
                     text="EXIT",
                     command=do_exit,
                     bg="black", fg='white',
                     activebackground='white',
                     activeforeground='black')
exit_btn.pack(fill=tk.X, pady=15)

os.system("sudo echo Welcome Admin > /dev/null ")

status()

root.mainloop()
