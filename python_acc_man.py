# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 15:27:16 2015

@author: lkonis
"""

import datetime
import time


name = "account 1"
ins_date = datetime.date.today()
mod_date = datetime.date.today()
user  = "lkonis"
passw = "1234"
comment = ""
accounts_db = list()

def load_data():
    filename = "acc_db.db"
    fi = open(filename,'rb')
    print "database file: " + filename
    all_lines = fi.readlines()
    fi.close()
    ts = time.time()
    for line in all_lines:
        new_rec = line.split()
        if len(new_rec)<4:
            print "record that starts with " + new_rec[0] + " has not enough details"
            continue
        new_rec_with_time = [new_rec[0], ts, ts, new_rec[1], new_rec[2], " ".join(new_rec[3:])]
        accounts_db.append(new_rec_with_time)
def import_new_rec(*new_rec_argv):
    N=len(new_rec_argv)
    user = passw = comment = ""
    if N==0:
        print "empty record"
        return
    new_rec_argv = new_rec_argv[0]
    N=len(new_rec_argv)
    if N>=1:
        name=new_rec_argv[0]
    if N>=2:
        user=new_rec_argv[1]
    if N>=3:
        passw=new_rec_argv[2]
    if N>=4:
        comment=new_rec_argv[2]
    
    ts = time.time()
    new_rec_with_time = [name, ts, ts, user, passw, comment]
    # test if this is new or existing one
    exist_already=0
    for indx, account in enumerate(accounts_db):
        existing_name = account[0]
        if name==existing_name:
            exist_already=1
            accounts_db[indx][2]=ts
            if user:
                accounts_db[indx][3]=user
            if passw:
                accounts_db[indx][4]=passw
            if comment:
                accounts_db[indx][5]=comment
            
    if not(exist_already):
        accounts_db.append(new_rec_with_time)
        print "New record added: " + name
    else:
        print "updated existing record: " + name
    

if __name__ == '__main__':
  load_data()

  import_new_rec() 
  new_rec =['gmail','lko']
  import_new_rec(new_rec)
  