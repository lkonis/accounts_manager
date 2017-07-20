# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:47:30 2011
Upgraded Mon March 2, 2015
@author: lkonis
"""


import sys
from encrypt import *

# this class contains method
class cipher(encryption):
    mode='ENC'              # mode can be encoder or decoder
    def run_endec(self, *args):
      if len(args)<1:
          args = sys.argv[1:]


      if not args:
        print '\ncipher.py - a python script for text file ciphering'
        print 'the user should pick a code-word which will be used to encode a text file'
        print 'the exact same code word will be used afterward to de-cipher that file'
        print '\nusage: cipher infile code-word\n'
        print 'by default, infile will be ciphered (encoded)'
        print 'if it has a ".coded" extention, then it will be decoded'

        sys.exit(1)

      filename = " ".join(args[:-1])    # file to be encoded/decoded
      password = args[-1]    # code remembered by the user
      if len(password)<=4:
          print ("Cipher: no password or password too short (min 4 char)\nLeaving file uncoded")
          sys.exit(2)
      if '.coded' in filename:
          self.mode='DEC' # detect that file is coded and define as decoding
      else:
          self.mode='ENC'


      if self.mode=='ENC':   # to encode
          outfile = filename+".coded"
      else:             # to decode
          if '.coded' in filename:
              filename = filename.split('.coded')[0]
              outfile = filename + '.decoded'
          else:
              filename = filename.split('.decoded')[0]
              outfile = filename+".decoded"

      # HERE call the new PyCrypto
      if self.mode=='ENC':
          self.encrypt(self.getKey(password), filename)
      else:
          self.decrypt(self.getKey(password), filename)

      if self.mode=='ENC':
          print "Cipher: Done encoding into file: "  + outfile + "\n"
      else:
          print "Cipher: Done decoding\n"
      return

def main():
    c = cipher()
    c.run_endec()#"lkjlkj.txt", "1222")



if __name__ == '__main__':
  main()
