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
sys.path.insert(0, currentdir)
import shutil
import xlwings as xw
import pandas as pd
from classes.Annot_Reader import *
from utils import *

    
args = parse_args_ec_scrape()
print(args['--keywords'])

orig = 'testing\\test_files\\' + 'test_genome_annotation.xls'
cpy = 'testing\\test_files\\' + 'test_genome_annotation_write21.xls'
# Read the excel sheet
reader = Annot_Reader(src=args['--src'], dest=args['--dest'], sheet=args['--sheet'])

