from distutils.core import setup
setup(
  name = 'pbd',
  packages = ['pbd'],
  version = '0.9',
  description = 'Pbd is a Python module to disassemble serialized protocol buffers descriptors (https://developers.google.com/protocol-buffers/).',
  author = 'Radoslaw Matusiak',
  author_email = 'radoslaw.matusiak@gmail.com',
  url = 'https://github.com/rsc-dev/pbd',
  download_url = 'https://github.com/rsc-dev/pbd/releases/tag/0.9',
  keywords = ['disassembler', 'pb2', 'protocol buffers', 'reverse'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Disassemblers'
  ],
)