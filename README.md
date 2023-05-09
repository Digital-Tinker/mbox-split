# mbox-split

usage: search.py [-h] [-o OUTPUT] [-nv] [-vo VERIFY_OUTPUT] source filter

Script to filter an mbox file using a list of Message IDs. Accepts an mbox file as input and a text file with Message
IDs, 1 per line and outputs an mbox containing only those messages that match the filter list.

positional arguments:
  source                Source mbox path
  filter                Filter text file with list of Message IDs, 1 per line

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path, defaults to output.mbox
  -nv, --no-verify      Disable verification
  -vo VERIFY_OUTPUT, --verify-output VERIFY_OUTPUT
                        Specify file to output any missing Message IDs
