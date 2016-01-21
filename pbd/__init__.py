#!/usr/bin/env python

__author__      = 'Radoslaw Matusiak'
__copyright__   = 'Copyright (c) 2016 Radoslaw Matusiak'
__license__     = 'MIT'
__version__     = '0.9'


"""
Protocol buffers disassembler.
"""

import os
import sys

from google.protobuf.descriptor_pb2 import FileDescriptorProto


class Pbd():
    """
    Google protocol buffers disassembler.
    """
    
    LABELS =[None, 'optional', 'required', 'repeated']
    TYPES = [None, 'double', 'float', 'int64', 'uint64', 'int32', 'fixed64', 'fixed32', 'bool', 'string', 
            'group', 'message', 'bytes', 'uint32', 'enum', 'sfixed32', 'sfixed64', 'sint32', 'sint64']
    
    def __init__(self, input_file):
        """Constructor.
        
        Keyword arguments:
        input_file -- input file name
        """
        self.input_file = input_file
        self.lines = []
        self.tabs = 0
        
        self.package = ''
        self.name = None
        
        self.defines = []
        self.uses = []
        self.imports = []
    # end-of-method __init__
    
    def _print(self, line=''):
        """Append line to internal list. 
        Uses self.tabs to format indents.
        
        Keyword arguments:
        line -- line to append
        """
        self.lines.append('{}{}'.format('\t'*self.tabs , line))
    # end-of-method _print

    def _dump_enum(self, e, top=''):
        """Dump single enum type.
        
        Keyword arguments:
        top -- top namespace
        """
        self._print()
        self._print('enum {} {{'.format(e.name))
        self.defines.append('{}.{}'.format(top,e.name))
        
        self.tabs+=1
        for v in e.value:
            self._print('{} = {};'.format(v.name, v.number))
        self.tabs-=1
        self._print('}')
    # end-of-method _dump_enums 
    
    def _dump_field(self, fd):
        """Dump single field.
        """
        v = {}
        v['label'] = Pbd.LABELS[fd.label]
        v['type'] = fd.type_name if len(fd.type_name) > 0 else Pbd.TYPES[fd.type]
        v['name'] = fd.name
        v['number'] = fd.number
        v['default'] = '[default = {}]'.format(fd.default_value) if len(fd.default_value) > 0 else ''
        
        f = '{label} {type} {name} = {number} {default};'.format(**v)
        f = ' '.join(f.split())
        self._print(f)
        
        if len(fd.type_name) > 0:
            self.uses.append(fd.type_name)
    # end-of-function _dump_field    
    
    def _dump_message(self, m, top=''):
        """Dump single message type.
        
        Keyword arguments:
        top -- top namespace
        """
        self._print()
        self._print('message {} {{'.format(m.name))
        self.defines.append('{}.{}'.format(top, m.name))
        self.tabs+=1
        
        for f in m.field:
            self._dump_field(f)
        
        for e in m.enum_type:
            self._dump_enum(e, top='{}.{}'.format(top, m.name))
        
        for n in m.nested_type:
            self._dump_message(n, top='{}.{}'.format(top, m.name))
        
        self.tabs-=1
        self._print('}')
    # end-of-method _dump_messages  
    
    def _walk(self, fd):
        """Walk and dump (disasm) descriptor.
        """
        top = '.{}'.format(fd.package) if len(fd.package) > 0 else ''
        
        for e in fd.enum_type: self._dump_enum(e, top)
        for m in fd.message_type: self. _dump_message(m, top)
    # end-of-method _walk   
    
    def disassemble(self):
        """Disassemble serialized protocol buffers file.
        """
        ser_pb = open(self.input_file, 'rb').read()  # Read serialized pb file
        
        fd = FileDescriptorProto()
        fd.ParseFromString(ser_pb)
        self.name = fd.name
        
        self._print('// Reversed by pbd (https://github.com/rsc-dev/pbd)')

        if len(fd.package) > 0:
            self._print('package {};'.format(fd.package))
            self.package = fd.package
        else:
            self._print('// Package not defined')
        
        self._walk(fd)
    # end-of-method disassemble
    
    def dump(self, out_dir='.'):
        """Dump proto file to given directory.
        
        Keyword arguments:
        out_dir -- dump directory. Default='.'
        """
        uri = out_dir + os.sep + self.name
        with open(uri, 'w') as fh:
            fh.write('\n'.join(self.lines))
    # end-of-method dump
    
    
    def find_imports(self, pbds):
        """Find all missing imports in list of Pbd instances.
        """
        # List of types used, but not defined
        imports = list(set(self.uses).difference(set(self.defines)))
        
        # Clumpsy, but enought for now 
        for imp in imports:
            for p in pbds:
                if imp in p.defines:
                    self.imports.append(p.name)
                    break
        
        self.imports = list(set(self.imports))
        
        for import_file in self.imports:
            self.lines.insert(2, 'import "{}";'.format(import_file))
    # end-of-method find_imports
    
    pass
# end-of-class Pbd    


if __name__ == '__main__':
    pass