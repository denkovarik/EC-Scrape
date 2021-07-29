# File: ec_scrape.py
#
# Description:
# Performs a blast on sequences or parses downloaded BLAST result files. 
# for proteins in a genome annotation. Afterwards it then searches 
# online databases like NCBI protein and UniProt for their EC Number. This
# is the main program file which is the start of the program.
#
# Author: Dennis Kovarik

import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
import shutil
import xlwings as xw
import pandas as pd
from classes.Annot_Reader import *
from utils import *


args = parse_args_ec_scrape(sys.argv)
# Read the excel sheet
reader = Annot_Reader(args)
if '--from_downloaded_blast' in args.keys() \
and args['--from_downloaded_blast'] == True:
    ec_added = dl_blast_ec_scrape(reader, args)
    print("Found EC Numbers for an additional " + str(ec_added) + " proteins")
else:
    online_blast_ec_scrape(reader, args)