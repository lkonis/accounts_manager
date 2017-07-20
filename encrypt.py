# encrypt.py
# file using PyCrypto module implementing encryption and decryption methods

import os, random
import time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class encryption:
    chunksize = 1024

    # implementing encryption
    def encrypt(self, key, filename):
        outputFile = filename+".coded"
        fileSize = str(os.path.getsize(filename)+4*16).zfill(16)
        now = time.localtime()
        modifyDate = "File encoded by Crypto.cipher at: %02d-%02d-%d,  %02d:%02d:%02d" % (
            now.tm_mday, now.tm_mon, now.tm_year, now.tm_hour, now.tm_min, now.tm_sec)
        modifyDate = modifyDate + " " * (16*4 - len(modifyDate)-1) + "\n"

        # generating IV (Initializing Vector)
        IV = ''
        try:
            for i in range(16):
                IV += chr(random.randint(0, 0xFF))
        except():
            print "couldn't create IV (Initialize Vector). Exiting..."
            exit(-1)

        encryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(filename, 'rb') as infile:
                with open(outputFile, 'wb') as outfile:
                    outfile.write(fileSize)
                    outfile.write(IV)
                    outfile.write(encryptor.encrypt(modifyDate))

                    while True:
                        chunk = infile.read(self.chunksize)

                        if len(chunk) == 0:
                            break
                        elif len(chunk) % 16 != 0:
                            chunk += ' '* (16 - (len(chunk)%16))
                        outfile.write(encryptor.encrypt(chunk))

    # implementing decryption
    def decrypt(self, key, filename):
        outputFile = filename + ".decoded" # add postfix
        inputFile = filename + ".coded"

        with open(inputFile, 'rb') as infile:
            filesize = long(infile.read(16))
            IV = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(outputFile, 'wb') as outfile:
                dateEnc = infile.read(16 * 4)
                modifyDate = decryptor.decrypt(dateEnc)
                outfile.write(modifyDate)

                while True:
                    chunk = infile.read(self.chunksize)

                    if len(chunk) == 0:
                        break

                    text = decryptor.decrypt(chunk)
                    outfile.write(text)
                outfile.truncate(filesize)

    # get hash word for a given password
    def getKey(self, password):
        hasher = SHA256.new(password)
        return hasher.digest()

# service routine to be used when stand alone
def Main():
    crypt = encryption()
    choice = raw_input('Would you like to (E)ncrypt or (D)ecrypt?: ')
    if choice == '':
        filename = 'run_lite.bat'
        password = '1234'
        crypt.encrypt(crypt.getKey(password), filename)
    elif choice=='E':
        filename = raw_input('File to encrypt: ')
        if filename == '':
            filename = 'run_lite.bat'
            password = '1234'
        else:
            password = raw_input('Password: ')
        try:
            crypt.encrypt(crypt.getKey(password), filename)
        except:
            pass
        print 'Done.'
    elif choice == 'D':
        filename = raw_input('File to decrypt: ')
        if filename == '':
            filename = 'run_lite.bat.coded'

        password = raw_input('Password: ')
        crypt.decrypt(crypt.getKey(password), filename)
        print 'Done.'
    else:
        print 'No option selected'

if __name__ == '__main__':
    Main()
