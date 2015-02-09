# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 15:27:16 2015

@author: lkonis
"""

#import datetime
import time
import re

accounts_db = list()
textfilename = "my_accounts.txt"
outfilename = "out_test.db"
filename = "acc_db.db" #outfilename
def load_data():
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
    if (N<1) | (len(new_rec.strip())==0):
        print "empty record"
        return
    new_rec_argv = new_rec_argv[0]
    if type(new_rec_argv) is str:
        # remove end-of-line
        new_rec_argv = str.strip( new_rec_argv)
        # try split line in two
        new_rec_argv = re.compile(",\s*").split(new_rec_argv)
        # if succeeded, combine again
        if len(new_rec_argv)==2:
            name = new_rec_argv[0]
            new_rec_argv = new_rec_argv[1].split(' ')
            new_rec_argv.insert(0, name)
        else:
            new_rec_argv = re.compile("\s*").split(new_rec_argv[0])
    N=len(new_rec_argv)
    if N>=1:
        name=new_rec_argv[0]
    if N>=2:
        user=new_rec_argv[1]
    if N>=3:
        passw=new_rec_argv[2]
    if N>=4:
        comment=' '.join(new_rec_argv[3:])
    
    ts = time.time()
    new_rec_with_time = [name, ts, ts, user, passw, comment]

    # remove empty strings
    new_rec_with_time = filter(None, new_rec_with_time)
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

def save_data():
    fi = open(outfilename,'w')
    for line in accounts_db:
        print line
        fi.write(', '.join(map(str, line)) + "\n")
    fi.close()

    

if __name__ == '__main__':
    # load the data base - do we need it?
    # why not loading data base just when we want to update?
    #  i.e. inside import_new_rec
    load_data()
    #load lines from existing account file'
    fi = open(textfilename,'rb')
    if (fi):
        print "file: " + textfilename + " is loaded"
        lines = fi.readlines()
        fi.close()
    # import new records to the database
    for new_rec in lines:
        import_new_rec(new_rec)

    save_data()
      
      
      
      
      
      