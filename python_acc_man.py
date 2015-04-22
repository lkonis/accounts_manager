# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 15:27:16 2015

@author: lkonis
"""

#import datetime
import re
import sys
import time
import os
import cipher
import logging
import getopt

logger = logging.getLogger('acc_man_log')
logging.basicConfig()
logger.setLevel(logging.WARN)

def usage():
    """ Prints out usage information """
    print ""
    print
    print "Usage:"
    print "    --help -h:     This text"
    print "    --no-log:      don't print log"
    print "    --debug:       Print out extra debug information."
    print "    --change:      change an account name"
    print "    --pass:        Replace password"

def handle_args(argv):
    """ Handles arguments """
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "no-log", "debug", "change", "pass"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in "--change":
            logger.warn('changing account name')
        elif opt in "--pass":
            logger.warn('changing password')
        elif opt in "--debug":
            logger.setLevel(logging.DEBUG)
        elif opt in "--no-log":
            print(" *** no log printing ***")
            logger.setLevel(level=logging.ERROR)



class acc_main:
#accounts_db = list()
# reach record of database contains initially:
#    name, 1, time of insertion, user name, password,comments
# if already exists, then it is updated but keeping all past records:
#    name, number of updates, [time1, user1, pass1], ..., comments
    textfilename = "my_accounts.txt"
    internal_db_filename = "acc_db.db"
    out_txt_filename = "my_accounts.txt"
    def load_data(self, db_filename):

        fi = open(db_filename,'rb')
        all_lines = fi.readlines()
        fi.close()
        local_accounts_db = list()

        #ts = time.time()
        for line in all_lines:
            new_rec = re.compile(",\s*").split(line.strip())
            if len(new_rec)<4:
                if not('abcd1234' in new_rec):
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

    #    managing the whole command-line interface
    def add_new_rec(self):
        my_pass = raw_input("Enter your password (also if no .coded file exists): [<CR> to ignore password]")
        if my_pass=="":
            nopass=True
            nosavepass=True
            my_pass="nopass"
        else:
            nopass=False
            nosavepass=False

        if not(nopass):
            # use this for coded file name
            db_filename_cd = self.internal_db_filename + ".coded"
            if not(os.path.isfile(db_filename_cd)):
                if (os.path.isfile(self.internal_db_filename)):
                    print ("coded file " + db_filename_cd + " doesn't exist\nUsing the uncoded version " + self.internal_db_filename + " instead")
                    nopass=True
                else:
                    print ("coded file " + db_filename_cd + " and uncoded version " + self.internal_db_filename + " do not exist\n Exiting...")
                    sys.exit(1)

        if not(nopass):
            print "trying to decode data file " + db_filename_cd

            c = cipher.cipher()
            c.run_endec(db_filename_cd, my_pass)

            # read decoded file and remove 3 lines
            db_filename_dec = self.internal_db_filename + ".decoded"
            fi = open(db_filename_dec,'rb')
            all_lines = fi.readlines()
            fi.close()
#                all_lines = all_lines[3:] # remove header lines from decoding

            # detect whether decoding was successful
            if not('abcd1234' in all_lines[3]):
                print("unsuccessful decoding. probably password is wrong, quiting....")
                sys.exit(2)


            # write decoded data into file
            fi = open(self.internal_db_filename, 'w')
            fi.writelines(all_lines[4:]) # remove header lines and checksum line from decoding
            fi.close()
        else:
            if not(os.path.isfile(self.internal_db_filename)):
                print ("You either expect to find uncoded database file " + self.internal_db_filename + ", or didn't put any password, exiting....")
                sys.exit(1)
            if nosavepass:
                print "ignoring passwords...\n"
            else:
                print "using password to cipher output"

        # check correctness of data (that is, if passsword was correct)
        an = raw_input("Enter new or existing account name (<Enter> for decoding only): ")
        if an=="":
            print "not adding anything, just decoding into text"
            prepare_to_abandon=True
        else:
            prepare_to_abandon=False


        accounts_db = self.load_data(self.internal_db_filename)

        if prepare_to_abandon:
            print("\nsaving text file " + self.out_txt_filename)
            self.save_txt_data(accounts_db, self.out_txt_filename)
            os.remove(self.internal_db_filename)
            os.remove(db_filename_dec)
            return

        # check if account exists already
        for indx, account in enumerate(accounts_db):
            exist_acc_name = account[0]
            if (an==exist_acc_name):
                aq = raw_input("\nAccount name \"" +an+"\" already exists in database\n\nDo you want to update it? [n for no or <enter> for accept]: ")
                if (aq=="n"):
                    print("\nNo updates\n")
                    if not(nopass):
                        if (os.path.isfile(self.internal_db_filename)):
                            os.remove(self.internal_db_filename)
                        if (os.path.isfile(db_filename_dec)):
                            os.remove(db_filename_dec)
                    return

        aun = raw_input("Enter user name: ")
        aup = raw_input("Enter user password: ")
        acm = raw_input("Enter any comment: ")

        new_rec_argv = an +", "+aun+" "+aup+" "+acm
        accounts_db = self.import_new_rec(accounts_db, new_rec_argv)
        print("\nsaving db")
        self.save_db_data(accounts_db, self.internal_db_filename, my_pass)
        print("\nsaving text file " + self.out_txt_filename)
        self.save_txt_data(accounts_db, self.out_txt_filename)

    def import_new_rec(self, accounts_db, new_rec_argv):
        new_rec_argv = re.compile(",\s*").split(new_rec_argv.strip())
        N=len(new_rec_argv)
        user = passw = ""
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
            print "\nNew record added: " + name
        else:
            print "\nUpdated existing record: " + name

        return(accounts_db)

    def save_db_data(self, accounts_db, db_filename, my_pass):
        if my_pass=="nopass":
            nopass = True
        else:
            nopass = False
        fi = open(db_filename,'w')
        # first line used as checksum for successful decoding later
        fi.write('abcd1234\n')

        for line in accounts_db:
            #print line
            fi.write(', '.join(map(str, line)).strip() + "\n")
        fi.close()
        if not(nopass):
            c = cipher.cipher()
            c.run_endec(db_filename, my_pass)
            print "trying to remove file " + db_filename
            os.remove(db_filename)

    def save_txt_data(self, accounts_db, out_txt_filename):
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
    handle_args(sys.argv[1:])
    logger.info('This is info')
    logger.debug('This is debug only message')

    acc = acc_main()
    print("***** done defining class acc_main ****\n")
    acc.add_new_rec()



    #acc.save_db_data()
    #print("*** done save db data ****\n")
    sys.exit()

