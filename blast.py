# File: blast.py
#
# Description:
# Performs a blast on the fasta sequence passed in from the command line and
# the searches NCBI protein database and UniProt for the EC number of the 
# top BLAST hits.
#
# Author: Dennis Kovarik

from Bio import SeqIO
from Bio.Blast import NCBIWWW
from time import sleep
import sys
from utils import *
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)


def parse_args():
    """
    Parses the arguments to the program.
    
    :return: A dictionary of arguements
    """
    # Expected arguments
    outFile = None
    sleep_time  = None
    fasta_sequence  = None
    email  = None
    min_pct_idnt  = 97.0
    min_qry_cvr = 95.0
    max_blast_hits = 10
    max_uniprot_hits = 50
    # Dict to hold arguements
    args =  {
                '--fasta_sequence' : fasta_sequence,
                '--program' : 'bastx',
                '--email' : email, 
                '--out_file' : outFile,
                '--min_pct_idnt' : min_pct_idnt,
                '--min_qry_cvr' : min_qry_cvr,
                '--max_blast_hits' : max_blast_hits,
                '--max_uniprot_hits' : max_uniprot_hits,
                '--sleep_time' : sleep_time,
                '--id' : '0',
            }
    received = set(())
    required    = set(('--fasta_sequence', '--email', '--program'))
    float_args  = set(('--sleep_time', '--min_pct_idnt', '--min_qry_cvr'))
    int_args    = set(('--max_blast_hits', '--max_uniprot_hits'))
    if len(sys.argv) % 2 != 1:
        print("Invalid command line arguements")
        exit()
    # Parse the arguements
    for i in range(1, len(sys.argv), +2):
        arg = sys.argv[i]
        val = sys.argv[i+1]
        if arg in args:
            received.add(arg)
            if arg in float_args:
                args[arg] = float(val)
            elif arg in int_args:
                args[arg] = int(val)
            elif arg in args:
                args[arg] = val
    # Check that the required arguments where passed in
    for r in required:
        if not r in received:
            print(r + " is a required arguement\n")
            print_usage()
            exit()
    return args
    
    
def print_usage():
    """
    Prints the usage statement
    """
    print("Usage:")
    print("  py blast.py --fasta_sequence <fasta sequence to blast>") 
    print("              --email <the user's email>")
    print("              --out_file <filepath to store result>")
    print("              --min_pct_idnt <the min % identity to use for blast hit>")
    print("              --min_qry_cvr <the min query cover to use for blast hit>") 
    print("              --max_blast_hits <the max number of blast hits to use>") 
    print("              --max_uniprot_hits <the max number of UniProt hits to use>")
    print("              --sleep_time <amount of time to sleep before preforming the blast>")
    print("")
    print("  Required params:\n\t--fasta_sequence\n\t--email")
    

args = parse_args()  
# BLAST requests that we don't flood the servers
if args['--sleep_time'] is not None:
    sleep(args['--sleep_time'])

# Perform the BLAST query
result_handle = NCBIWWW.qblast(program=args['--program'], 
                                      database="nr", 
                                      sequence=args['--fasta_sequence'])
blast_xml = result_handle.read()
result_handle.close()
# Process the blast results
seq_len = len(args['--fasta_sequence'])
output = prcs_blast_rslts(blast_xml, seq_len, \
                          args['--email'], \
                          args['--min_pct_idnt'], \
                          args['--min_qry_cvr'], \
                          args['--max_blast_hits'], \
                          args['--max_uniprot_hits'])
if args['--out_file'] is None:
    print(output)
else:
    save_file = open(args['--out_file'], "w")
    save_file.write(output)
    save_file.close()