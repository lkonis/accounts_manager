Accounts manager
================
This is a python project that helps read/write and manage a personal accounts/password database
The project is written in python, probably using tk for graphical interface later on
the database is supposed to be encrypted using any desired function, which is not included here
The interface however for importing/exporting, managing and browsing is described here:

Files
-----
There are four files (at least) that are required here:
* python_acc_man.py       - python file containing code for all interfaces
* crypto_cipher.py        - python file containing call to an encryption file
* acc_db.db.coded (encripted file) - data file that can be written and read using the encrypt/decrypt methods
* a forth file (encrypt.py) that should implement encryption/decryption 
  - the latter should implement cipher class with encrypt/decrypt methods. it is not stored in git reporsitory and is up to every user how to implement it

python File metadata (at the moment, only one field really requried here)
----------------------------------
* <last modified>

### each field in database contains:
* name | date of insertion| user name | password| general description  
* name | ins_date         | user      | pass    | commment

## methods:
* encrypt 		- tbd
* decrypt 		- tbd
* load       		- load existing database file
* import_new_rec 	- import new record
* save_db_data 		- save updated database file
* save_txt_data 	- export updated database file into local text file
* add_new_rec a 	- command-line interface to import new record and save updated databse in db and text format

## future methods:
* history records
* graphical display
