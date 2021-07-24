import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from run_blast_utils import *
from classes.Annot_Reader import Annot_Reader
import math


class Run_BLAST_Utils_tests(unittest.TestCase):
    """
    Runs all tests for the utility functions in Run_BLAST_Utils.py.
    """
    def test_parse_fasta(self):
        """
        Tests the ability of the parse_fasta() function to parse a fasta file 
        containing multiple sequences and store the sequences by their location.
        
        :param self: An instance of the Utils_tests class.
        """
        filepath = 'E:\\blast\\mult_query.fasta'
        self.assertTrue(os.path.isfile(filepath))
        queries = parse_fasta(filepath)
        exp = {
            'contig_1_7184_6765': 'MDIKIHSDFSHANLNEMREVYSSVGWTKHTTKIIKQVFEASNVIALATINGRIIGFGRAISDGVFNAAIYDVVVHRDFQKQGIAKKIMEFLLDQLSHVSCVHLISTTGNEEFYRKLGLKRVKTGMARYLNPELSDEYLE',
            'contig_1_10704_10537': 'MKGAESASFVLFLFHRSIRRAGNLHLKERANVPKECAKSGTIRKNFAHYFRIRLK',
            'contig_1_11311_10706': 'MNPSLYHVVYFPLSTGGVMDFYRGLALGLGEEPKYRKVDLFRQIQQAIERLYHERRITPVFILDEMHLAKDAFLQDIAILFNFEMDSTNPFVLILAGLPHLQGKLRLNQHRPLDQRIIMRYRMGPLEKEEVAGYIKHRMKQAGAKHPIFTPSALEAIALQSRGWPRVINTLATTCLLYGYQLKKDAIDEEVVRMAAEEMGY',
            'contig_1_11505_11365': 'MYKSFYSLSREPFAKETDPSEAYQGAPFQEALRALEYVKRTRGSGC',
            'contig_1_13448_12804': 'MIQFHDFDIDVQTYAERGKENDFPLLKKCPHCRAKRPLHRHGYYERNALTPHGDYRIWIVRYRCRECLKTVSVLPSFLLPYFQYTLSAIWQVVKEQLGLTEGTNRAPFLPTKGRHHLLCPAVLPKPIKPSQLFCEAVEDHRPYREKRKGTGFLVDPDVGETRSLFGHQRHVGGRIPTPFCESNGILILHTYPKLEIVEVPTNLSYRRRKSDPVR'
            }
        self.assertTrue(queries == exp)
        
        
    def test_execution(self):
        """
        Tests the ability of the Utils_tests class to run a test.
        
        :param self: An instance of the Utils_tests class.
        """
        self.assertTrue(True)
        
        
if __name__ == '__main__':
    unittest.main()