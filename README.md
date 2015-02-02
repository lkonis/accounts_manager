# accounts_manager
This is a python project that helps maintain, read/write etc. a personal accounts/password database
The project is written in python, probably using tk for graphicall interface
the database is encrypted using any desired function, which is not included here
The interface however for importing/exporting, managing and browsing is described here:

## files:
There are two files (at least) that are required here:
* python_acc_man.py       - python file containing code for all interfaces
* acc_db (encripted file) - data file that can be written and read using the encrypt/decrypt methods
## python File metadata (at the moment, only one field really requried here)
* <last modified>
## each field contains:
* name | date of insertion| date of last modification | user name | password| general description  
* name | ins_date         | mod_date                  | user      | pass    | desc
## methods:
* encrypt
* decrypt
* load        (load data)
* import_new (import new records)
* export
* export_last (export from last modification)
## future methods:
* history records
* graphical display
