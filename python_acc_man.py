# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 15:27:16 2015

@author: lkonis
"""

#import datetime
import time
import re
import sys

#accounts_db = list()
# reach record of database contains initially:
#    name, 1, time of insertion, user name, password,comments
# if already exists, then it is updated but keeping all past records:
#    name, number of updates, [time1, user1, pass1], ..., comments
textfilename = "my_accounts.txt"
out_db_filename = "out_test.db"
init_db_filename = "acc_db.db" #out_db_filename
out_txt_filename = "out_test.txt"
def load_data(init_db_filename):
    fi = open(init_db_filename,'rb')
   # print "loading database file: " + init_db_filename
    all_lines = fi.readlines()
    fi.close()
    local_accounts_db = list()

    #ts = time.time()
    for line in all_lines:
        new_rec = re.compile(",\s*").split(line.strip())
        if len(new_rec)<4:
            print "record that starts with " + new_rec[0] + " has not enough details"
            continue
        if not(new_rec[1].replace(" ","").isdigit()):
            print "record must have integer as second arg " + new_rec[1] + " is not a digit"
            continue
        # extract comment
#        comment = new_rec[int(new_rec[1])*3+2:]
        
        # make number of updates digit
        new_rec[1] = int(new_rec[1])
        # convert all time fields to float
        for trec in range(new_rec[1]):
            new_rec[2+trec*3] = float(new_rec[2+trec*3])
#        new_rec_with_time = [new_rec[0], new_rec[1], new_rec[2], new_rec[3], new_rec[4], " ".join(comment)]
        local_accounts_db.append(new_rec)
    return(local_accounts_db)
def add_new_rec():
    if len(sys.argv) < 2:
        init_db_filename = "acc_db.db"
        an = raw_input("Enter account name: ")
        if an=="":
            return

        accounts_db = load_data(init_db_filename)
        # check if account exists already
        for indx, account in enumerate(accounts_db):
            exist_acc_name = account[0]
            if (an==exist_acc_name):
                aq = raw_input("\nAccount name \"" +an+"\" already exists in database\n\nDo you want to update it? [n for no or <enter> for accept]\n>")
                if (aq=="n"):
                    print("no updates")
                    return
                    
        aun = raw_input("Enter user name: ")
        aup = raw_input("Enter user password: ")
        acm = raw_input("Enter any comment: ")
        new_rec_argv = an +", "+aun+" "+aup+" "+acm
        accounts_db = import_new_rec(accounts_db, new_rec_argv)
        ret_str = "New account added to database: " + an
        save_db_data(accounts_db, init_db_filename)
        save_txt_data(accounts_db, out_txt_filename)
        print(ret_str)
        
def import_new_rec(accounts_db, new_rec_argv):
    save_db_when_done=0
    if len(sys.argv) > 1:
        # import database file
        new_rec_argv = ' '.join(sys.argv[2:])
        db_filename = sys.argv[1]
        accounts_db = load_data(db_filename)
        save_db_when_done=1
    new_rec_argv = re.compile(",\s*").split(new_rec_argv.strip())
    N=len(new_rec_argv)
    user = passw = comment = ""
    if (N<1) | (len(new_rec_argv)==0):
        print "empty record"
        return
    #if isinstance(new_rec_argv, tuple):
    #    new_rec_argv = new_rec_argv[0]
    #if type(new_rec_argv) is str:
    # remove end-of-line
    # new_rec_argv = str.strip( new_rec_argv)
    # try split line in two
    # new_rec_argv = re.compile(",\s*").split(new_rec_argv)
    # if succeeded, combine again
    if len(new_rec_argv)==2:
        name = new_rec_argv[0]
        new_rec_argv = new_rec_argv[1].split(' ')
        new_rec_argv.insert(0, name)
    else:
        new_rec_argv = re.compile("\s*").split(new_rec_argv[0])


    comment="no comment"
    N=len(new_rec_argv)
    if N<3:
        return
    if N>=1:
        name=new_rec_argv[0]
    if N>=2:
        user=new_rec_argv[1]
    if N>=3:
        passw=new_rec_argv[2]
    if N>=4:
        comment=' '.join(new_rec_argv[3:])
    
    ts = time.time()
    new_rec_with_time = [name, 1, ts, user, passw, comment]

    # remove empty strings
    new_rec_with_time = filter(None, new_rec_with_time)
    # test if this is new or existing one
    exist_already=0
    for indx, account in enumerate(accounts_db):
        existing_name = account[0]
        if name==existing_name:
            exist_already=1
            cur_db_rec = accounts_db[indx]
            # increase no of modifications
            cur_db_rec[1] = cur_db_rec[1] + 1
            # insert the new information (3 fields)
            mod_time = ts
            cur_db_rec.insert(2, mod_time)
            cur_db_rec.insert(3, user)
            cur_db_rec.insert(4, passw)
            # if not empty comments
            cur_db_rec[-1] = comment
            accounts_db[indx] = cur_db_rec
            
    if not(exist_already):
        accounts_db.append(new_rec_with_time)
        print "New record added: " + name
    else:
        print "updated existing record: " + name
        
    if save_db_when_done:
        save_db_data(accounts_db, db_filename)
    else:
        return(accounts_db)

def save_db_data(accounts_db, out_db_filename):
    fi = open(out_db_filename,'w')
    for line in accounts_db:
        #print line
        fi.write(', '.join(map(str, line)).strip() + "\n")
    fi.close()

def save_txt_data(accounts_db, out_txt_filename):
    import datetime
    fi = open(out_txt_filename,'w')
    now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') 
    fi.write('Account file auto-generated at: ' + now + '\n')
    fi.write('='*54 +'\n\n\n\n')

    for line in accounts_db:
        #print line
        if (line[1]==1):
            line.pop(1)
            fi.write(line[0] + ", modified: ")
            line.pop(0)
            line[0] = format(datetime.datetime.fromtimestamp(line[0]),'%d/%m/%Y')
            fi.write(', '.join(map(str, line)) + "\n")
        else:
            n = line.pop(1)
            fi.write(line[0] + ", modified: ")
            line.pop(0)
            line[0] = format(datetime.datetime.fromtimestamp(line[0]),'%d/%m/%Y')
            fi.write(', '.join(map(str, line[0:3])))
            if (len(line)>(3*n)):
                fi.write(", " + line[-1])
            fi.write("\n")
            
    fi.close()
    
    

if __name__ == '__main__':
    # load the data base - do I need it?
    # why not loading data base just when we want to update?
    #  i.e. inside import_new_rec
    add_new_rec()
    exit    
    accounts_db = load_data(init_db_filename)
    #load lines from existing account file'
    fi = open(textfilename,'rb')
    if (fi):
#        print "file: " + textfilename + " is loaded"
        lines = fi.readlines()
        fi.close()
    # import new records to the database
    #for new_rec in lines:
    #    import_new_rec(accounts_db, new_rec)

    #save_db_data(accounts_db, out_db_filename)
    save_txt_data(accounts_db, out_txt_filename)
      
      
      
      
      
      