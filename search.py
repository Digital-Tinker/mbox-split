#!/bin/python3

import os
import mailbox
import argparse
from tqdm import tqdm

# Set up Arguments
parser = argparse.ArgumentParser(description="Script to filter an mbox file using a list of Message IDs. Accepts an mbox file as input and a text file with Message IDs, 1 per line and outputs an mbox containing only those messages that match the filter list.")

parser.add_argument("source", help = "Source mbox path")
parser.add_argument("filter", help = "Filter text file with list of Message IDs, 1 per line")
parser.add_argument("-o", "--output", default="output.mbox", help = "Output file path, defaults to output.mbox")
parser.add_argument("-nv", "--no-verify", action='store_true', help = "Disable verification")
parser.add_argument("-vo", "--verify-output", help = "Specify file to output any missing Message IDs")

args = parser.parse_args()


# Open Mbox files
print("Opening mbox files")
try:
    source = mailbox.mbox(args.source, create=False)
    dest = mailbox.mbox(args.output)
    if os.path.getsize(args.output) > 0:
        proceed = input("Output file is not empty. Do you wish to overwrite? (y/n) ")
        if proceed.lower() == "y" or proceed.lower() == "yes":
            print("Continuing with overwrite")
            f = open(args.output, 'r+')
            f.truncate(0)
            f.close()
        elif proceed.lower() == "n" or proceed.lower() == "no":
            print("Exiting")
            exit()
        else:
            print("Unrecognized input, exiting")
            exit()
except (mailbox.NoSuchMailboxError, PermissionError, FileNotFoundError):
    print("Unable to open source or output mbox. Please verify name or permissions and try again")
    raise SystemExit

# Open Filter file
print("Reading Message IDs from filter file")
try:
    with open(args.filter, "r") as f:
        message_ids = [line.strip() for line in f]
except (PermissionError, FileNotFoundError):
    print("Unable to open filter file. Please verify name or permissions and try again")
    raise SystemExit

print("Indexing mbox, please be patient as this can take time with no indication of progress. Search will start after with progress bar.")

# Copy filtered messages into output file
for message in tqdm(source):
    if message['Message-ID'] in message_ids:
        dest.add(message)
print("Export completed to "+args.output)

# Verify if any Message IDs were missed in output file
if args.no_verify == False:
    print("Starting Verification")
    for message in tqdm(dest):
        if message['Message-ID'] in message_ids:
            message_ids.remove(message['Message-ID'])
    if len(message_ids) > 0:
        print("Message IDs not found in source mbox: ")
        for ids in message_ids:
            print(str(ids+'\n'))
        #TODO Fix this part - why did it trigger without the argument
        if args.verify_output:
            print("Saving Message IDs to "+args.verify_output)
            with open(args.verify_output, 'w') as fp:
                for ids in message_ids:
                    fp.write(str(ids)+'\n')
    else:
        print("No missing Message IDs found. Exiting")
