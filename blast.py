from Bio import SeqIO
from Bio.Blast import NCBIWWW
from time import sleep
import sys


outFile = sys.argv[1]
sleep_time = int(sys.argv[2])

sleep(sleep_time)

print("Blast for " + outFile)
fasta_string = open("testing\\test_files\\test_BLAST.fasta").read()

result_handle = NCBIWWW.qblast(program="blastx", 
                                      database="nr", 
                                      sequence=fasta_string, 
                                      entrez_query="txid2 [ORGN]")
save_file = open(outFile, "w")

save_file.write(result_handle.read())

save_file.close()

result_handle.close()