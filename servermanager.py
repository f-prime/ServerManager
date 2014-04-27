#!/usr/bin/python

import os
import cmd
import landerdb

class SM(cmd.Cmd):
    prompt = "> "
    intro = "Type `help` for a list of commands"
    global db
    db = landerdb.Connect("/home/frankie/Dropbox/Python_Projects/ServerManager/servers.db")
    
    def do_help(self, line):
        print """


            servers - Lists servers and their passwords
            add <ip> <password> <descrition>
            connect <username> <number>
            edit <number> <password>
            delete <number> 

        """

    def do_servers(self, line):
        data = db.find("servers", "all")
        for num, x in enumerate(data):
            print str(num)+") "+x['ip'], x['password'], x['description']

    def do_add(self, line):
        line = line.split()
        db.insert("servers",{"ip":line[0], "password":line[1], "description":' '.join(line[2:])})
        db.save()
    
    def do_connect(self, line):
        out = db.find("servers", "all")
        line = line.split()
        password = out[int(line[1])]['password']
        ip = out[int(line[1])]['ip']
        ssh = "sshpass -p {0} ssh {1}@{2}".format(password, line[0], ip)
        os.system(ssh)

    def do_edit(self, line):
        line = line.split()
        all_ = db.find("servers", "all")
        all_ = all_[int(line[0])]
        db.update("servers", all_, {"password":line[1]})
        db.save()

    def do_delete(self, line):
        line = line.split()
        check = db.find("servers", "all")
        db.remove("servers", check[int(line[0])])
        db.save()

if __name__ == "__main__":
    sm = SM()
    sm.cmdloop()

