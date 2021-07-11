import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import shutil
import xlwings as xw
import pandas as pd
from classes.Annot_Reader import *
from utils import *


class Annot_Reader_tests(unittest.TestCase):
    """
    Runs all tests for the Annot_Reader class.
    """
    def test_autosave(self):
        """
        Tests Annot_Reader class to autosave if prematurely terminated.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
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
        # Construct an Annot_Reader
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        self.assertTrue(reader.rows == set((2,14)))   
        
            
    def test_load_job(self):
        """
        Tests Annot_Reader class on member function 'load_job()' on 
        its ability to load a job from file.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        job1 = currentdir + '\\test_files\\' "load_job_test1.txt"
        args =  {
                '--src' : None,
                '--dest' : None,
                '--sheet': 0,
                '--keywords' : "hypothetical protein",
                '--visible' : False,
                '--load_job' : job1,
                '--email' : email, 
                '--min_pct_idnt' : min_pct_idnt,
                '--min_qry_cvr' : min_qry_cvr,
                '--max_blast_hits' : max_blast_hits,
                '--max_uniprot_hits' : max_uniprot_hits,
            }
        # Construct an Annot_Reader
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        self.assertTrue(reader.rows == set((2,14)))
        self.assertTrue(reader.args['--keywords'] == None)
        
        
    def test_parse_keywords(self):
        """
        Tests function parse_keywords() on its ability to parse the keywords 
        and create the necessary data structure for it.'
        
        :param self: An element of the Annot_Reader_tests class.
        """
        # Test Case 1
        keywords = 'hypothetical protein'
        exp = [{"Not": False, "Keyword" : "hypothetical"}, 
               {"Not": False, "Keyword" : "protein"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 2
        keywords = "'hypothetical protein'"
        exp = [{"Not": False, "Keyword" : "hypothetical protein"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 3
        keywords = '"hypothetical protein"'
        exp = [{"Not": False, "Keyword" : "hypothetical protein"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 4
        keywords = 'DNA Polymerase "hypothetical protein" Glutimate'
        exp = [{"Not": False, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": False, "Keyword" : "hypothetical protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 5
        keywords = 'NOT hypothetical protein'
        exp = [{"Not": True, "Keyword" : "hypothetical"}, 
               {"Not": False, "Keyword" : "protein"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 6
        keywords = 'hypothetical NOT protein'
        exp = [{"Not": False, "Keyword" : "hypothetical"}, 
               {"Not": True, "Keyword" : "protein"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 7
        keywords = 'NOT "hypothetical protein"'
        exp = [{"Not": True, "Keyword" : "hypothetical protein"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 8
        keywords = 'NOT DNA Polymerase NOT "hypothetical protein" Glutimate'
        exp = [{"Not": True, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": True, "Keyword" : "hypothetical protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 9
        keywords = 'NOT (DNA Polymerase) NOT "hypothetical protein" Glutimate'
        exp = [{"Not": True, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": True, "Keyword" : "hypothetical protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 10
        keywords = 'NOT -DNA Polymerase) NOT $"hypothetical protein" --Glutimate'
        exp = [{"Not": True, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": True, "Keyword" : "hypothetical protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 11
        keywords = 'NOT -DNA Polymerase) NOT $"hypothetical-protein" --Glutimate'
        exp = [{"Not": True, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": True, "Keyword" : "hypothetical-protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 12
        keywords = "NOT -DNA Polymerase) NOT $'hypothetical-protein' --Glutimate"
        exp = [{"Not": True, "Keyword" : "DNA"}, 
               {"Not": False, "Keyword" : "Polymerase"},
               {"Not": True, "Keyword" : "hypothetical-protein"},
               {"Not": False, "Keyword" : "Glutimate"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        # Test Case 13
        keywords = None
        exp = [{"Not": False, "Keyword" : "*"}]
        rslt = Annot_Reader.parse_keywords(keywords)
        self.assertTrue(rslt == exp)
        
        
    def test_save_job(self):
        """
        Tests Annot_Reader class on member function 'save_job' on 
        its ability to save a job to file.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy3.xls"
        job1 = currentdir + '\\test_files\\' "job1.txt"
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        if os.path.isfile(job1):
            os.remove(job1)
        self.assertFalse(os.path.isfile(cpy))
        self.assertFalse(os.path.isfile(job1))
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        args =  {
                    '--src' : orig,
                    '--dest' : cpy,
                    '--sheet': 0,
                    '--visible' : False,
                    '--keywords' : "hypothetical protein",
                    '--load_job' : None,
                    '--email' : email, 
                    '--min_pct_idnt' : min_pct_idnt,
                    '--min_qry_cvr' : min_qry_cvr,
                    '--max_blast_hits' : max_blast_hits,
                    '--max_uniprot_hits' : max_uniprot_hits,
                }
        # Construct an Annot_Reader
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        keywords = 'hypothetical protein'
        keywords = Annot_Reader.parse_keywords(keywords)
        reader.compile_rows(keywords)
        reader.save_job(job1)
        # Validate the results
        f = open(job1, 'r')
        txt = f.read()
        f.close()
        txt = txt.split("\n")
        for i in range(len(txt)):
            line = txt[i]
            if line != "======Rows_to_BLAST======" \
            and line != "=========================":
                params = line.split(" ")
                if params[0] == "--src":
                    exp = 'C:\\Users\\1985937\\Documents\\BI_Sum_2021\\EC-Scrape\\testing\\test_files\\test_genome_annotation.xls'
                elif params[0] == "--dest":
                    exp = 'C:\\Users\\1985937\\Documents\\BI_Sum_2021\\EC-Scrape\\testing\\test_files\\test_genome_annotation_cpy3.xls'
                elif params[0] == "--sheet":
                    exp = '0'
                    self.assertTrue(params[1] == exp)
                elif params[0] == "--keywords":
                    keyword = ""
                    for i in range(1, len(params)):
                        keyword += params[i]
                        if i < len(params) - 1:
                            keyword += " "                  
                    exp = 'hypothetical protein'
                    self.assertTrue(keyword == exp)
                elif params[0] == "--load_job":
                    exp = 'None'
                    self.assertTrue(params[1] == exp)
                elif params[0] == "--email":
                    exp = 'None'
                    self.assertTrue(params[1] == exp)
                elif params[0] == "--min_pct_idnt":
                    exp = '97.0'
                    self.assertTrue(params[1] == exp)
                elif params[0] == "--min_qry_cvr":
                    exp = '95.0'
                    self.assertTrue(params[1] == exp)
                elif params[0] == "--max_blast_hits":
                    exp = '10'
                    self.assertTrue(params[1] == exp)
                elif params[0] == "--max_uniprot_hits":
                    exp = '50'
                    self.assertTrue(params[1] == exp)
            elif line == '======Rows_to_BLAST======':
                i += 1
                received = set(())
                expected = set((4, 16))
                while txt[i] != '=========================':
                    val = int(txt[i].strip())
                    received.add(val)
                    i += 1
                self.assertTrue(received == expected)
            i += 1
        
        
    def test_compile_rows(self):
        """
        Tests Annot_Reader class on member function 'compile_rows()' on 
        its ability to compile a list of rows to perform operations on.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xls"
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        self.assertFalse(os.path.isfile(cpy))
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        args =  {
                    '--src' : orig,
                    '--dest' : cpy,
                    '--sheet': 0,
                    '--visible' : False,
                    '--keywords' : "hypothetical protein",
                    '--load_job' : None,
                    '--email' : email, 
                    '--min_pct_idnt' : min_pct_idnt,
                    '--min_qry_cvr' : min_qry_cvr,
                    '--max_blast_hits' : max_blast_hits,
                    '--max_uniprot_hits' : max_uniprot_hits,
                }
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        # Construct an Annot_Reader
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        keywords = [{"Not": False, "Keyword" : "hypothetical"}]
        reader.compile_rows(keywords)
        self.assertTrue(reader.rows == set((2, 14)))
    
    
    def test_matches_keywords(self):
        """
        Tests Annot_Reader class on static function 'matches_keywords()' on 
        its ability to determine if a string matches a list of keywords give 
        to it.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        # Test case 1
        keywords = [{"Not": False, "Keyword" : "hypothetical"}]
        txt = "hypothetical protein"
        self.assertTrue(Annot_Reader.matches_keywords(txt, keywords))
        # Test case 2
        keywords = [{"Not": False, "Keyword" : "hypothetical Protein"}]
        txt = "Hypothetical protein"
        self.assertTrue(Annot_Reader.matches_keywords(txt, keywords))
        # Test case 3
        txt = "DNA polymerase IV (EC 2.7.7.7)"
        keywords = [{"Not": False, "Keyword" : "hypothetical"}]
        self.assertFalse(Annot_Reader.matches_keywords(txt, keywords))
        # Test case 4
        txt = "DNA polymerase IV (EC 2.7.7.7)"
        keywords = [{"Not": True, "Keyword" : "hypothetical"}]
        self.assertTrue(Annot_Reader.matches_keywords(txt, keywords))
        # Test case 5
        txt = "DNA polymerase IV (EC 2.7.7.7)"
        keywords = [{"Not": True, "Keyword" : "hypothetical"},
                    {"Not": False, "Keyword" : "DNA"},
                    {"Not": False, "Keyword" : "polymerase"}]
        self.assertTrue(Annot_Reader.matches_keywords(txt, keywords))
        # Test case 6
        txt = "hypothetical protein"
        keywords = [{"Not": True, "Keyword" : "hypothetical"},
                    {"Not": False, "Keyword" : "DNA"},
                    {"Not": False, "Keyword" : "polymerase"}]
        self.assertFalse(Annot_Reader.matches_keywords(txt, keywords))
        # Test case 7
        txt = "hypothetical protein"
        txt2 = "DNA polymerase IV (EC 2.7.7.7)"
        keywords = [{"Not": False, "Keyword" : "*"}]
        self.assertTrue(Annot_Reader.matches_keywords(txt, keywords))
        self.assertTrue(Annot_Reader.matches_keywords(txt2, keywords))
        # Test case 8
        txt = "hypothetical protein"
        txt2 = "DNA polymerase IV (EC 2.7.7.7)"
        keywords = [{"Not": False, "Keyword" : "*"},
                    {"Not": True, "Keyword" : "hypothetical"}]
        self.assertFalse(Annot_Reader.matches_keywords(txt, keywords))
        self.assertTrue(Annot_Reader.matches_keywords(txt2, keywords))
        # Test case 9
        txt = "hypothetical protein"
        txt2 = "DNA polymerase IV (EC 2.7.7.7)"
        keywords = [{"Not": True, "Keyword" : "*"}]
        self.assertFalse(Annot_Reader.matches_keywords(txt, keywords))
        self.assertFalse(Annot_Reader.matches_keywords(txt2, keywords))
        # Test case 10
        txt = "hypothetical protein"
        txt2 = "DNA polymerase IV (EC 2.7.7.7)"
        keywords = [{"Not": True, "Keyword" : "*"},
                    {"Not": False, "Keyword" : "hypothetical"}]
        self.assertFalse(Annot_Reader.matches_keywords(txt, keywords))
        self.assertFalse(Annot_Reader.matches_keywords(txt2, keywords))
        
    
    def test_is_ec(self):
        """
        Tests Annot_Reader class on determining if a string is an ec number 
        or not.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        test0 = ""
        test1 = "Hi there"
        test2 = "EC"
        test3 = "2.EC"
        test4 = "2.E.C.C"
        test5 = "2.E.C.7"
        test6 = "2.7.7.7"
        test7 = "3.1.3.-"
        test8 = "3.5.-.-"
        test9 = "2.7.7.7"
        test10 = "7.023"
        test11 = "8.21..5"
        test12 = "(1.1.1.1"
        test13 = "1.1.1.1("
        test14 = "1.(1.1.1"
        test15 = "2.7.7.7)"
        test16 = ")2.7.7.7"
        test17 = "2.7).7.7"
        test18 = "(1.1.1.1("
        test19 = "(1.1.(1.1("
        test20 = "(1.1.)1.1("
        test21 = "(1.1.1.1)"
        self.assertFalse(Annot_Reader.is_ec(test0))
        self.assertFalse(Annot_Reader.is_ec(test1))
        self.assertFalse(Annot_Reader.is_ec(test2))
        self.assertFalse(Annot_Reader.is_ec(test3))
        self.assertFalse(Annot_Reader.is_ec(test4))
        self.assertFalse(Annot_Reader.is_ec(test5))
        self.assertTrue(Annot_Reader.is_ec(test6))
        self.assertTrue(Annot_Reader.is_ec(test7))
        self.assertTrue(Annot_Reader.is_ec(test8))
        self.assertTrue(Annot_Reader.is_ec(test9))
        self.assertFalse(Annot_Reader.is_ec(test10))
        self.assertFalse(Annot_Reader.is_ec(test11))
        self.assertTrue(Annot_Reader.is_ec(test12))
        self.assertTrue(Annot_Reader.is_ec(test13))
        self.assertFalse(Annot_Reader.is_ec(test14))
        self.assertTrue(Annot_Reader.is_ec(test15))
        self.assertTrue(Annot_Reader.is_ec(test16))
        self.assertFalse(Annot_Reader.is_ec(test17))
        self.assertTrue(Annot_Reader.is_ec(test18))
        self.assertFalse(Annot_Reader.is_ec(test19))
        self.assertFalse(Annot_Reader.is_ec(test20))
        self.assertTrue(Annot_Reader.is_ec(test21))
        
        
    def test_has_ec(self):
        """
        Tests Annot_Reader class on determining if a gene already has an 
        associated ec number.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        test1 = "hypothetical protein"
        test2 = "DNA polymerase IV (EC 2.7.7.7)"
        test3 = "Sigma-X negative effector (EC 3 and more)"
        test4 = "Hypothetical protein TEPIRE1_21570 (predicted: PeP phosphonomutase (predicted EC 2.7.8.23) (predicted EC 4.1.3.30))"
        test5 = "Glutaminase (EC 3.5.-.-)"
        test6 = "Histidinol-phosphatase (EC 3.1.3.-)"
        test7 = " (predicted EC 2.3.1.1)"
        test8 = "hypothetical protein (predicted: MULTISPECIES: GNAT family N-acetyltransferase [Geobacillus] (predicted EC 2.3.1.1))"
        test9 = "Aminodeoxychorismate lyase, EC 4.1.3.38"
        test10 = "Aminodeoxychorismate lyase, EC: 4.1.3.38"
        test11 = "Aminodeoxychorismate lyase, EC: -.-.-.-"
        test12 = "Histidinol-phosphatase (EC -.1.3.1)"
        test13 = "DNA polymerase IV (Web Scaped EC 2.7.7.7)"
        
        self.assertFalse(Annot_Reader.has_ec(test1))
        self.assertTrue(Annot_Reader.has_ec(test2))
        self.assertFalse(Annot_Reader.has_ec(test3))
        self.assertTrue(Annot_Reader.has_ec(test4))
        self.assertTrue(Annot_Reader.has_ec(test5))
        self.assertTrue(Annot_Reader.has_ec(test6))
        self.assertTrue(Annot_Reader.has_ec(test7))
        self.assertTrue(Annot_Reader.has_ec(test8))
        self.assertTrue(Annot_Reader.has_ec(test9))
        self.assertTrue(Annot_Reader.has_ec(test10))
        self.assertFalse(Annot_Reader.has_ec(test11))
        self.assertFalse(Annot_Reader.has_ec(test12))
        self.assertTrue(Annot_Reader.has_ec(test13))
        # Run on test genome annotation
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xls"
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        self.assertFalse(os.path.isfile(cpy))
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        args =  {
                    '--src' : orig,
                    '--dest' : cpy,
                    '--sheet': 0,
                    '--visible' : False,
                    '--keywords' : None,
                    '--load_job' : None,
                    '--email' : email, 
                    '--min_pct_idnt' : min_pct_idnt,
                    '--min_qry_cvr' : min_qry_cvr,
                    '--max_blast_hits' : max_blast_hits,
                    '--max_uniprot_hits' : max_uniprot_hits,
                }
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        self.assertTrue(reader.has_ec(reader.read(0, 'function')))
        self.assertTrue(reader.has_ec(reader.read(1, 'function')))
        self.assertFalse(reader.has_ec(reader.read(2, 'function')))
        self.assertTrue(reader.has_ec(reader.read(3, 'function')))
        self.assertTrue(reader.has_ec(reader.read(4, 'function')))
        self.assertTrue(reader.has_ec(reader.read(5, 'function')))
        self.assertTrue(reader.has_ec(reader.read(6, 'function')))
        self.assertTrue(reader.has_ec(reader.read(7, 'function')))
        self.assertTrue(reader.has_ec(reader.read(8, 'function')))
        self.assertTrue(reader.has_ec(reader.read(9, 'function')))
        self.assertFalse(reader.has_ec(reader.read(10, 'function')))
        self.assertFalse(reader.has_ec(reader.read(11, 'function')))
        self.assertFalse(reader.has_ec(reader.read(12, 'function')))
        self.assertFalse(reader.has_ec(reader.read(13, 'function')))
        self.assertFalse(reader.has_ec(reader.read(14, 'function')))
        self.assertTrue(reader.has_ec(reader.read(15, 'function')))
        self.assertTrue(reader.has_ec(reader.read(16, 'function')))
        self.assertTrue(reader.has_ec(reader.read(17, 'function')))
        self.assertTrue(reader.has_ec(reader.read(18, 'function')))
        
        
    def test_write(self):
        """
        Tests Annot_Reader class on writing a value to a cell in the excel 
        sheet
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' + 'test_genome_annotation.xls'
        cpy = currentdir + '\\test_files\\' \
                         + 'test_genome_annotation_write2.xls'
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        args =  {
                    '--src' : orig,
                    '--dest' : cpy,
                    '--sheet': 0,
                    '--visible' : False,
                    '--keywords' : None,
                    '--load_job' : None,
                    '--email' : email, 
                    '--min_pct_idnt' : min_pct_idnt,
                    '--min_qry_cvr' : min_qry_cvr,
                    '--max_blast_hits' : max_blast_hits,
                    '--max_uniprot_hits' : max_uniprot_hits,
                }
        # Construct an Annot_Reader
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        write_row = 3
        write_col = "function"
        val = reader.read(write_row, write_col)
        val += " Modified++"
        reader.write(val, write_row, write_col)
        exp = "DNA polymerase IV (EC 2.7.7.7) Modified++"
        self.assertTrue(reader.read(write_row, write_col) == exp)
        
        
    def test_init(self):
        """
        Tests the initialization of the Annot_Reader object.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xls"
        shifted = currentdir + '\\test_files\\'
        shifted += 'test_genome_annotation_shifted_data_frame.xls'
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        self.assertFalse(os.path.isfile(cpy))
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        args =  {
                    '--src' : orig,
                    '--dest' : cpy,
                    '--sheet': 0,
                    '--visible' : False,
                    '--keywords' : None,
                    '--load_job' : None,
                    '--email' : email, 
                    '--min_pct_idnt' : min_pct_idnt,
                    '--min_qry_cvr' : min_qry_cvr,
                    '--max_blast_hits' : max_blast_hits,
                    '--max_uniprot_hits' : max_uniprot_hits,
                }
        # Construct an Annot_Reader
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        self.assertTrue(reader.dest == cpy)
        self.assertTrue(reader.header['start row'] == 1)
        self.assertTrue(reader.cols['function'] == 'H')
        del(reader)
        # Reload singleton class
        args['--dest'] = orig
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        self.assertTrue(reader.dest == orig)
        # Loading file with shifted data frame
        self.assertTrue(os.path.isfile(shifted))
        
        
    def test_read_cell(self):
        """
        Tests Annot_Reader on reading a cell from the excel sheet
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        orig = currentdir + '\\test_files\\' "test_genome_annotation.xls"
        cpy = currentdir + '\\test_files\\' "test_genome_annotation_cpy.xls"
        self.assertTrue(os.path.isfile(orig))
        if os.path.isfile(cpy):
            os.remove(cpy)
        self.assertFalse(os.path.isfile(cpy))
        # Now copy the file
        shutil.copyfile(orig, cpy)
        self.assertTrue(os.path.isfile(cpy))
        email  = None
        min_pct_idnt  = 97.0
        min_qry_cvr = 95.0
        max_blast_hits = 10
        max_uniprot_hits = 50
        args =  {
                    '--src' : orig,
                    '--dest' : cpy,
                    '--sheet': 0,
                    '--visible' : False,
                    '--keywords' : None,
                    '--load_job' : None,
                    '--email' : email, 
                    '--min_pct_idnt' : min_pct_idnt,
                    '--min_qry_cvr' : min_qry_cvr,
                    '--max_blast_hits' : max_blast_hits,
                    '--max_uniprot_hits' : max_uniprot_hits,
                }
        reader = Annot_Reader(args)
        reader.autosave_filename = 'test_autosave.txt'
        exp = "DNA polymerase IV (EC 2.7.7.7)"
        self.assertTrue(reader.read(3, 'function') == exp)
        
        
    def test_cols(self):
        """
        Tests Annot_Reader.int_2_col on its ability to convert an int
        to a supported excel column label.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        self.assertTrue(Annot_Reader.col_labels[1] == "A")
        self.assertTrue(Annot_Reader.col_labels[26] == "Z")
        self.assertTrue(Annot_Reader.col_labels[27] == "AA")
        self.assertTrue(Annot_Reader.col_labels[28] == "AB")
        self.assertTrue(Annot_Reader.col_labels["A"] == 1)
        self.assertTrue(Annot_Reader.col_labels["Z"] == 26)
        self.assertTrue(Annot_Reader.col_labels["AA"] == 27)
        self.assertTrue(Annot_Reader.col_labels["AB"] == 28)
        
        
    def test_execution(self):
        """
        Tests the ability of the Annot_Reader_tests class to run a test.
        
        :param self: An instance of the Annot_Reader_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()