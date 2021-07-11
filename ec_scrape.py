# File: ec_scrape.py
#
# Description:
# Performs a blast on sequences in a genome annotation and then searches 
# online databases like NCBI protein and UniProt for their EC Number. This
# is the main program file which is the start of the program.
#
# Author: Dennis Kovarik

import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
import shutil
import xlwings as xw
import pandas as pd
from classes.Annot_Reader import *
from utils import *


args = parse_args_ec_scrape()

# Read the excel sheet
reader = Annot_Reader(args)

rows_to_process = set((reader.rows))
processing = set(())
# Create temp dir to hold results returned from processes
if not os.path.isdir('temp\\'):
    os.mkdir('temp\\')
# Start Blasting
itr = iter(rows_to_process)
num_rows = len(rows_to_process)
bar = IncrementalBar('| BLASTing Sequences...', max = num_rows)
num_processing = 0 
max_num_processes = 50
tempdir = 'temp\\'
count = 0

# Make sure there are no files left in temp dir
for file in os.listdir(tempdir):
    path = tempdir + file
    os.remove(path)

while len(reader.rows) > 0:
    cmd = []
    rows_added = []
    while count < num_rows and len(processing) < max_num_processes:
        row = next(itr)
        # Read the Sequences
        seq = reader.read(row, 'nucleotide_sequence')
        out_file = tempdir + str(row) + ".txt"
        cmd += [build_cmd(seq, out_file, row, args)]
        processing.add(row)
        count += 1
    if len(cmd) > 0:
        # Blast the sequence
        num_processing += len(processing)
        exec_commands(cmd, max_num_processes)       
    while len(os.listdir(tempdir)) > 0:
        filename = os.listdir(tempdir)[0]
        filepath = tempdir + filename
        f = open(filepath, 'r')
        content = f.read()
        f.close()
        os.remove(filepath)
        completed_row = filename.split(".")[0]
        completed_row = completed_row.strip()
        completed_row = int(completed_row)
        val = reader.read(completed_row, 'function') + " " + content
        reader.write(val, completed_row, 'function')
        reader.rows.remove(completed_row)
        processing.remove(completed_row)
        bar.next()
        num_processing -= 1
    # Autosave
    reader.save_job(reader.autosave_filename)