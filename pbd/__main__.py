#!/usr/bin/env python

__author__      = 'Radoslaw Matusiak'
__copyright__   = 'Copyright (c) 2016 Radoslaw Matusiak'
__license__     = 'MIT'
__version__     = '0.9'


"""
Protocol buffers disassembler.
"""

import argparse
import os
import sys

from pbd import Pbd


def logo():
        print """
                               
 _|_|_|    _|              _|  
 _|    _|  _|_|_|      _|_|_|  
 _|_|_|    _|    _|  _|    _|  
 _|        _|    _|  _|    _|  
 _|        _|_|_|      _|_|_|  
                               
                      ver {} 
        """.format(__version__)
# end-of-function logo
        
        
def main():
    logo()
    parser = argparse.ArgumentParser(description='Protocol buffers disassembler.')
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('-f', '--file', help='input file')
    input_group.add_argument('-d', '--dir', help='input directory')
    
    parser.add_argument('-o', '--outdir', help='output directory, default=.', default='.')
    
    args = parser.parse_args()
    
    if args.file is None and args.dir is None:
        print '[!] Please specify input file or directory!'
        sys.exit(-1)
    
    if args.file is not None:
        print '[+] Paring file {}'.format(args.file)
        p = Pbd(args.file)
        p.disassemble()
        p.dump(args.outdir)
        print '[+] Proto file saved as {}'.format(os.path.join(args.outdir, p.name))
    elif args.dir is not None:
        files = [os.path.join(args.dir, f) for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f))]

        proto = []
        for f in files:
            print '[+] Paring file {}'.format(f)        
            p = Pbd(f)
            p.disassemble()
            proto.append(p)
        
        print '[+] Fixing imports...'        
        for p in proto: p.find_imports(proto)
        
        print '[+] Dumping files...'
        for p in proto: p.dump(args.outdir)
# end-of-function main
    

if __name__ == '__main__':
    main()    