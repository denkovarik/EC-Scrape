import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from utils import *
import math


class Utils_tests(unittest.TestCase):
    """
    Runs all tests for the utility functions in utils.py.
    """   
    def test_parse_keywords(self):
        """
        Tests function parse_keywords() on its ability to parse the keywords 
        and create the necessary data structure for it.'
        
        :param self: An element of the Utils_tests class.
        """
        # Test Case 1
        keywords = 'hypothetical protein'
        exp = [{"Not": False, "Keyword" : "hypothetical"}, 
               {"Not": False, "Keyword" : "protein"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 2
        keywords = "'hypothetical protein'"
        exp = [{"Not": False, "Keyword" : "hypothetical protein"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 3
        keywords = '"hypothetical protein"'
        exp = [{"Not": False, "Keyword" : "hypothetical protein"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 4
        keywords = 'DNA Polymerase "hypothetical protein" Glutimate'
        exp = [{"Not": False, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": False, "Keyword" : "hypothetical protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 5
        keywords = 'NOT hypothetical protein'
        exp = [{"Not": True, "Keyword" : "hypothetical"}, 
               {"Not": False, "Keyword" : "protein"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 6
        keywords = 'hypothetical NOT protein'
        exp = [{"Not": False, "Keyword" : "hypothetical"}, 
               {"Not": True, "Keyword" : "protein"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 7
        keywords = 'NOT "hypothetical protein"'
        exp = [{"Not": True, "Keyword" : "hypothetical protein"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 8
        keywords = 'NOT DNA Polymerase NOT "hypothetical protein" Glutimate'
        exp = [{"Not": True, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": True, "Keyword" : "hypothetical protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        
        
    def test_prcs_blast_rslts(self):
        """
        Tests function prcs_blast_rslts() on its ability to process the 
        blast results and scrape online databases for the ec numbers.'
        
        :param self: An element of the Utils_tests class.
        """
        email = 'dennis.kovarik@mines.sdsmt.edu'
        path = currentdir + "\\test_files\\blast_Glutaminase.xml"
        self.assertTrue(os.path.isfile(path))
        f = open(path, 'r')
        blast_xml = f.read()
        f.close()
        seq_len = 348
        exp = '(EC-Scraped (glutaminase A [Geobacillus thermodenitrificans] (NCBI Protein Accession: WP_029761658) (EC-Scraped EC 3.5.1.2))) (EC-Scraped (glutaminase A [Geobacillus] (NCBI Protein Accession: WP_011887640) (EC-Scraped EC 3.5.1.2))) '
        rslt = prcs_blast_rslts(blast_xml, seq_len, email, 97.0, 86.0)
        self.assertTrue(rslt == exp)
        
        
    def test_tag_ec(self):
        """
        Tests function tag_ec() on its ability to replace 'EC ' with 
        'EC-Scraped EC '
        
        :param self: An element of the Utils_tests class.
        """
        # Test Case 1
        txt = 'GNAT family N-acetyltransferase, EC 2.3.1.1'
        exp = 'GNAT family N-acetyltransferase, (EC-Scraped EC 2.3.1.1)'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)
        # Test Case 2
        txt = 'GNAT family EC 2.3.1.1 N-acetyltransferase, EC 2.3.1.1'
        exp = 'GNAT family (EC-Scraped EC 2.3.1.1) N-acetyltransferase, (EC-Scraped EC 2.3.1.1)'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)
        # Test Case 3
        txt = 'GNAT family N-acetyltransferase, ec 2.3.1.1'
        exp = 'GNAT family N-acetyltransferase, (EC-Scraped EC 2.3.1.1)'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)
        # Test Case 4
        txt = 'GNAT family ec 2.3.1.1 N-acetyltransferase, ec 2.3.1.1'
        exp = 'GNAT family (EC-Scraped EC 2.3.1.1) N-acetyltransferase, (EC-Scraped EC 2.3.1.1)'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)
        # Test Case 5
        txt = 'GNAT family somethingec N-acetyltransferase, EC 2.3.1.1'
        exp = 'GNAT family somethingec N-acetyltransferase, (EC-Scraped EC 2.3.1.1)'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)
        # Test Case 6
        txt = 'GNAT family EC EC N-acetyltransferase, EC EC 2.3.1.1'
        exp = 'GNAT family EC EC N-acetyltransferase, EC (EC-Scraped EC 2.3.1.1)'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)
        # Test Case 7
        txt = 'GNAT family EC EC N-acetyltransferase, ec EC 2.3.1.1 tEC'
        exp = 'GNAT family EC EC N-acetyltransferase, ec (EC-Scraped EC 2.3.1.1) tEC'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)
        # Test Case 8
        txt = 'GNAT family N-acetyltransferase, (EC 2.3.1.1)'
        exp = 'GNAT family N-acetyltransferase, ((EC-Scraped EC 2.3.1.1))'
        rslt = tag_ec(txt)
        # Test Case 9
        txt = 'GNAT family (EC 2.3.1.1) N-acetyltransferase, (EC 2.3.1.1)'
        exp = 'GNAT family ((EC-Scraped EC 2.3.1.1)) N-acetyltransferase, ((EC-Scraped EC 2.3.1.1))'
        rslt = tag_ec(txt)
        self.assertTrue(rslt == exp)      
        
        
    def test_extract_ec(self):
        """
        Tests running the utility function 'extract_ec()' to extract an EC 
        number from a string.
        
        :param self: An element of the Utils_tests class.
        """
        # Test Case 1
        test = 'GNAT family N-acetyltransferase, EC 2.3.1.1'
        rslt = extract_ec(test)
        exp = '2.3.1.1'
        self.assertTrue(rslt == exp)
        # Test Case 2
        test = 'GNAT family N-acetyltransferase, EC 2.3.1.112'
        rslt = extract_ec(test)
        exp = '2.3.1.112'
        self.assertTrue(rslt == exp)
        # Test Case 3
        test = 'GNAT family N-acetyltransferase, EC 2.3.31.112'
        rslt = extract_ec(test)
        exp = '2.3.31.112'
        self.assertTrue(rslt == exp)
        # Test Case 4
        test = 'GNAT family N-acetyltransferase, EC 2.323.31.1'
        rslt = extract_ec(test)
        exp = '2.323.31.1'
        self.assertTrue(rslt == exp)
        # Test Case 5
        test = 'GNAT family N-acetyltransferase, EC 122.33.313.141'
        rslt = extract_ec(test)
        exp = '122.33.313.141'
        self.assertTrue(rslt == exp)
        # Test Case 6
        test = 'GNAT family N-acetyltransferase, EC 122.33.313.-'
        rslt = extract_ec(test)
        exp = '122.33.313.-'
        self.assertTrue(rslt == exp)
        # Test Case 7
        test = 'GNAT family N-acetyltransferase, EC 122.33.-.-'
        rslt = extract_ec(test)
        exp = '122.33.-.-'
        self.assertTrue(rslt == exp)
        # Test Case 8
        test = 'GNAT family N-acetyltransferase, EC 2.3.1.1 the end'
        rslt = extract_ec(test)
        exp = '2.3.1.1'
        self.assertTrue(rslt == exp)
        # Test Case 9
        test = 'GNAT family N-acetyltransferase, Predicted EC 2.3.1.1 the end'
        rslt = extract_ec(test)
        exp = '2.3.1.1'
        self.assertTrue(rslt == exp)
        # Test Case 10
        test = 'GNAT family N-acetyltransferase, Web Scraped EC 2.3.1.1 the end'
        rslt = extract_ec(test)
        exp = '2.3.1.1'
        self.assertTrue(rslt == exp)
        # Test Case 11
        test = 'GNAT family N-acetyltransferase, Web Scraped EC 2.3.1. the end'
        rslt = extract_ec(test)
        exp = ''
        self.assertTrue(rslt == exp)
        # Test Case 12
        test = 'GNAT family N-acetyltransferase, Web Scraped EC 2.3..1 the end'
        rslt = extract_ec(test)
        exp = ''
        self.assertTrue(rslt == exp)
        # Test Case 13
        test = 'GNAT family N-acetyltransferase, Web Scraped EC 2..43.1 the end'
        rslt = extract_ec(test)
        exp = ''
        self.assertTrue(rslt == exp)
        # Test Case 14
        test = 'GNAT family N-acetyltransferase, Web Scraped EC .1.43.1 the end'
        rslt = extract_ec(test)
        exp = ''
        self.assertTrue(rslt == exp)
        # Test Case 15
        test = 'GNAT family N-acetyltransferase, Web Scraped EC: 2.3.1.1 the end'
        rslt = extract_ec(test)
        exp = '2.3.1.1'
        self.assertTrue(rslt == exp)
        # Test Case 15
        test = 'GNAT family N-acetyltransferase, Web Scraped the end'
        rslt = extract_ec(test)
        exp = ''
        self.assertTrue(rslt == exp)
        
        
    def test_ec_scrape(self):
        """
        Tests running the utility function 'ec_scrape()'.
        
        :param self: An element of the Utils_tests class.
        """
        # Test Case 1
        email = 'dennis.kovarik@mines.sdsmt.edu'
        acc = 'WP_029761658'
        num_hits = 10
        rslt = ec_scrape(acc, email, num_hits)
        exp = '(EC-Scraped (glutaminase A [Geobacillus thermodenitrificans] (NCBI Protein Accession: WP_029761658) (EC-Scraped EC 3.5.1.2)))'
        self.assertTrue(rslt == exp)
        # Test Case 2
        acc = 'WP_008881006'
        num_hits = 10
        rslt = ec_scrape(acc, email, num_hits)
        exp = '(EC-Scraped (GNAT family N-acetyltransferase, (EC-Scraped EC 2.3.1.1) [Geobacillus sp. WSUCF-018B] UniProtKB: A0A2M9T2M7)) '
        self.assertTrue(rslt == exp)       
        
        
    def test_parse_blast_xml(self):
        """
        Tests the utils function parse_blast_xml on its ability to parse the
        output returned from a blast search return the required data 
        structure.
        
        :param self: An element of the Utils_tests class.
        """
        path = currentdir + "\\test_files\\blast_Glutaminase.xml"
        self.assertTrue(os.path.isfile(path))
        f = open(path, 'r')
        blast_xml = f.read()
        f.close()
        seq_len = 348
        blast_data = parse_blast_xml(blast_xml, seq_len=seq_len)
        self.assertTrue(len(blast_data) == 50)
        # Hit 1
        self.assertTrue(blast_data[0]['Hit_num'] == 1)
        self.assertTrue(blast_data[0]['Hit_accession'] == 'WP_029761658')
        self.assertTrue(abs(blast_data[0]['Per Ident'] - 100.00) < 0.01)
        self.assertTrue(abs(blast_data[0]['Query Cover'] - 87.0) < 1)
        # Hit 3
        self.assertTrue(blast_data[2]['Hit_num'] == 3)
        self.assertTrue(blast_data[2]['Hit_accession'] == 'WP_008880500')
        self.assertTrue(abs(blast_data[2]['Per Ident'] - 91.15) < 0.01)
        self.assertTrue(abs(blast_data[2]['Query Cover'] - 97) < 1)
        # Hit 16
        self.assertTrue(blast_data[15]['Hit_num'] == 16)
        self.assertTrue(abs(blast_data[15]['Per Ident'] - 89.11) < 0.01)
        self.assertTrue(abs(blast_data[15]['Query Cover'] - 87) < 1)
        # Hit 41
        self.assertTrue(blast_data[40]['Hit_num'] == 41)
        self.assertTrue(abs(blast_data[40]['Per Ident'] - 85.15) < 0.01)
        self.assertTrue(abs(blast_data[40]['Query Cover'] - 87) < 1)
        
        
    def test_execution(self):
        """
        Tests the ability of the Utils_tests class to run a test.
        
        :param self: An instance of the Utils_tests class.
        """
        self.assertTrue(True)
        
        
if __name__ == '__main__':
    unittest.main()