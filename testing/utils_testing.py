import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from utils import *
from classes.Annot_Reader import Annot_Reader
import math


class Utils_tests(unittest.TestCase):
    """
    Runs all tests for the utility functions in utils.py.
    """  
    def test_prcs_blast_rslts_html(self):
        """
        Runs testing for the utility function prcs_blast_rslts_html()
        
        :param self: An element of the Utils_tests class.
        """
        email = 'dennis.kovarik@mines.sdsmt.edu'
        out_file = "0.txt"
        min_pct_idnt  = 95.0
        min_qry_cvr = 90.0
        max_blast_hits = 5
        max_uniprot_hits = 50
        query_id = 0
        blast_rslts_path = currentdir + "\\test_files\\blast_rslts\\"
        orig = currentdir + '\\test_files\\' "test_genome_annotation2.xlsx"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xlsx"
        args =  {
                    '--src'                     : orig,
                    '--dest'                    : cpy,
                    '--keywords'                : None,
                    '--visible'                 : False,
                    '--load_job'                : None,
                    '--email'                   : email, 
                    '--sheet'                   : 0,
                    '--min_pct_idnt'            : min_pct_idnt,
                    '--min_qry_cvr'             : min_qry_cvr,
                    '--max_blast_hits'          : max_blast_hits,
                    '--max_uniprot_hits'        : max_uniprot_hits,
                    '--from_downloaded_blast'   : True,
                    '--BLAST_rslts_path'        : blast_rslts_path,

                }
        reader = Annot_Reader(args)
        dl_blast_ec_scrape(reader, args)
        filepath = currentdir + "\\test_files\\blast_rslts\\contig_1_15267_15503.htm"
        self.assertTrue(os.path.isfile(filepath))
        exp = "(EC-Scraped (GNAT family N-acetyltransferase, (EC-Scraped EC 2.3.1.1) [Geobacillus sp. WSUCF-018B] UniProtKB: A0A2M9T2M7))    (EC-Scraped (GNAT family N-acetyltransferase [Geobacillus sp. DSP4a] (NCBI Protein Accession: WP_216367871.1) (EC-Scraped EC 2.3.1.-)))"
        out = prcs_blast_rslts_html(filepath, reader, args)
        self.assertTrue(out == exp)

    
    def test_dl_blast_ec_scrape(self):
        """
        Runs testing for the utility function dl_blast_ec_scrape()
        
        :param self: An element of the Utils_tests class.
        """
        email = 'dennis.kovarik@mines.sdsmt.edu'
        out_file = "0.txt"
        min_pct_idnt  = 95.0
        min_qry_cvr = 90.0
        max_blast_hits = 5
        max_uniprot_hits = 50
        query_id = 0
        blast_rslts_path = currentdir + "\\test_files\\blast_rslts\\"
        orig = currentdir + '\\test_files\\' "test_genome_annotation2.xlsx"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xlsx"
        args =  {
                    '--src'                     : orig,
                    '--dest'                    : cpy,
                    '--keywords'                : None,
                    '--visible'                 : False,
                    '--load_job'                : None,
                    '--email'                   : email, 
                    '--sheet'                   : 0,
                    '--min_pct_idnt'            : min_pct_idnt,
                    '--min_qry_cvr'             : min_qry_cvr,
                    '--max_blast_hits'          : max_blast_hits,
                    '--max_uniprot_hits'        : max_uniprot_hits,
                    '--from_downloaded_blast'   : True,
                    '--BLAST_rslts_path'        : blast_rslts_path,

                }
        reader = Annot_Reader(args)
        dl_blast_ec_scrape(reader, args)
        #print(reader.read(1, 'function'))
        
        
    def test_check_dl_blast_args(self):
        """
        Runs testing for the utility function check_dl_blast_args() on its 
        ability to chech the command line arguments for using downloaded 
        blast results.
        
        :param self: An element of the Utils_tests class.
        """
        email = 'dennis.kovarik@mines.sdsmt.edu'
        out_file = "0.txt"
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        query_id = 0
        blast_rslts_path = currentdir + "\\test_files\\blast_rslts\\"
        job1 = currentdir + '\\test_files\\' "load_job_test1.txt"
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xlsx"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xlsx"
        args =  {
                    '--src'                     : orig,
                    '--dest'                    : cpy,
                    '--keywords'                : None,
                    '--visible'                 : False,
                    '--load_job'                : None,
                    '--email'                   : email, 
                    '--sheet'                   : 0,
                    '--min_pct_idnt'            : min_pct_idnt,
                    '--min_qry_cvr'             : min_qry_cvr,
                    '--max_blast_hits'          : max_blast_hits,
                    '--max_uniprot_hits'        : max_uniprot_hits,
                }
        # Test case for where --from_downloaded_blast flag is not set 
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertTrue(err)
        # Test case for where --from_downloaded_blast flag is set to None
        args['--from_downloaded_blast'] = None
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertTrue(err)
        # Test case for where --from_downloaded_blast flag is set to False
        args['--from_downloaded_blast'] = False
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertTrue(err)
        args['--from_downloaded_blast'] = True
        # Test case for where --BLAST_rslts_pathflag is not set 
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertTrue(err)
        # Test case for where --BLAST_rslts_path is set to None
        args['--BLAST_rslts_path'] = None
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertTrue(err)
        # Test case for where --BLAST_rslts_path is not a string
        args['--BLAST_rslts_path'] = True
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertTrue(err)
        # Test case for where --BLAST_rslts_path not a valid directory
        args['--BLAST_rslts_path'] = "Not\\valid\\path\\"
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertTrue(err)
        # Test case for where --BLAST_rslts_path is a valid directory
        args['--BLAST_rslts_path'] = currentdir \
                                   + "\\test_files\\blast_rslts\\"
        err = False
        try:
            check_dl_blast_args(args)
        except:
            err = True
        finally:
            self.assertFalse(err)
        
        
    def test_build_cmd(self):
        """
        Tests the utilities function 'build_cmd()' on its ability to build a 
        command to run blast.py on the command line.
        
        :param self: An element of the Utils_tests class.
        """
        seq = 'AATTGGC'
        email = 'dennis.kovarik@mines.sdsmt.edu'
        out_file = "0.txt"
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        query_id = 0
        job1 = currentdir + '\\test_files\\' "load_job_test1.txt"
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy3.xls"
        args =  {
                    '--src' : orig,
                    '--dest' : cpy,
                    '--sheet': 0,
                    '--keywords' : None,
                    '--visible' : False,
                    '--load_job' : job1,
                    '--email' : email, 
                    '--min_pct_idnt' : min_pct_idnt,
                    '--min_qry_cvr' : min_qry_cvr,
                    '--max_blast_hits' : max_blast_hits,
                    '--max_uniprot_hits' : max_uniprot_hits,
                }
        cmd = build_cmd(seq, out_file, query_id, args)
        exp = ["py", "blast.py", "--fasta_sequence", "AATTGGC", "--email", "dennis.kovarik@mines.sdsmt.edu", "--out_file", "0.txt", "--id", "0", "--min_pct_idnt", "97.0", "--min_qry_cvr", "95.0", "--max_blast_hits", "10", "--max_uniprot_hits", "50"]
        self.assertTrue(cmd == exp)
        
        
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