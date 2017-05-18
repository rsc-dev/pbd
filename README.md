# Pbd - Protocol Buffers Disassembler

[![Join the chat at https://gitter.im/rsc-dev/pbd](https://badges.gitter.im/rsc-dev/pbd.svg)](https://gitter.im/rsc-dev/pbd?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## About
Pbd is a Python module to disassemble serialized protocol buffers descriptors (https://developers.google.com/protocol-buffers/).

Example:
```sh
>python -m pbd -f examples\test.ser

 _|_|_|    _|              _|
 _|    _|  _|_|_|      _|_|_|
 _|_|_|    _|    _|  _|    _|
 _|        _|    _|  _|    _|
 _|        _|_|_|      _|_|_|

                      ver 0.9

[+] Paring file test.ser
[+] Proto file saved as .\test.proto
>type test.proto
// Reversed by pbd (https://github.com/rsc-dev/pbd)
// Package not defined

message Person {
        required string name = 1 ;
        required int32 id = 2 ;
        optional string email = 3 ;
}
```

## Installation
```sh
pip install pbd
```
or
```sh
python setup.py install
```

## Usage
### API

```python
import pbd

input_file_name = 'test.protoc'

proto = Pbd(input_file_name)
proto.disassemble()
proto.dump()
```

For multiple files with imports:
```python
import os
import pbd

input_dir = 'input\\'  # Input directory with serialized descriptors
output_dir = 'output\\'  # Output direcotry for proto files
input_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))] 

proto = []

for f in files:
    p = Pbd(f)
    p.disassemble()
    proto.append(p)
        
for p in proto: 
    p.find_imports(proto)
    p.dump(output_dir)
```


### Standalone module
Check help for available options:
```sh
python -m pbd -h
```

Disasm single file.
```sh
python -m pbd -f test.ser
```

Disasm all files in given directory and fix imports.
```sh
python -m pbd -i input_dir\ -o output_dir\
```

## License
Code is released under [MIT license](https://github.com/rsc-dev/loophole/blob/master/LICENSE.md) © [Radoslaw '[rsc]' Matusiak](https://rm2084.blogspot.com/).