import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from classes.BLAST_Rslts_Itr import BLAST_Rslts_Itr


class BLAST_Rslts_Itr_tests(unittest.TestCase):
    """
    Runs all tests for the BLAST_Rslts_Itr class.
    """  
    def test_no_rslt_found(self):
        """
        Tests iterator on file where no results where found.
        
        :param self: An instance of the BLAST_Rslts_Itr_tests class.
        """
        filename = 'no_results_found.htm'
        dirpath = parentdir + '\\testing\\test_files\\'
        self.assertTrue(os.path.isdir(dirpath))
        filepath = dirpath + filename
        self.assertTrue(os.path.isfile(filepath))
        f = open(filepath)
        content = f.read()
        f.close()
        for acc in BLAST_Rslts_Itr(content):
            self.assertTrue(False)


    def test_next(self):
        """
        Tests the python overloaded next function.
        
        :param self: An instance of the BLAST_Rslts_Itr_tests class.
        """
        filename = 'NCBI_Blast_Nucleotide_Sequence.htm'
        filepath = parentdir + '\\testing\\test_files\\' + filename
        self.assertTrue(os.path.isfile(filepath))
        f = open(filepath)
        content = f.read()
        f.close()
        itr = iter(BLAST_Rslts_Itr(content))
        # Test for BLAST program used
        self.assertTrue(itr.program == 'blastx')
        features = next(itr)
        self.assertTrue(features['Accession'] == 'WP_008880880.1')
        self.assertTrue(features['Query Cover'] == float(99))
        self.assertTrue(features['Per. Ident'] == float(99.75))
        self.assertTrue(features['E value'] == float(0.0))
        features = next(itr)
        self.assertTrue(features['Accession'] == 'WP_060476104.1')
        self.assertTrue(features['Query Cover'] == float(99))
        self.assertTrue(features['Per. Ident'] == float(99.51))
        features = next(itr)
        self.assertTrue(features['Accession'] == 'WP_168368883.1')
        self.assertTrue(features['Query Cover'] == float(99))
        self.assertTrue(features['Per. Ident'] == float(98.52))

    
    def test_iter(self):
        """
        Tests the python overloaded iter function.
        
        :param self: An instance of the BLAST_Rslts_Itr_tests class.
        """
        filename = 'NCBI_Blast_Nucleotide_Sequence.htm'
        filepath = parentdir + '\\testing\\test_files\\' + filename
        self.assertTrue(os.path.isfile(filepath))
        f = open(filepath)
        content = f.read()
        f.close()
        itr = iter(BLAST_Rslts_Itr(content))
        
        
    def test_init(self):
        """
        Tests the initialization of the BLAST_Rslts_Itr class.
        
        :param self: An instance of the BLAST_Rslts_Itr_tests class.
        """
        filename = 'NCBI_Blast_Nucleotide_Sequence.htm'
        filepath = parentdir + '\\testing\\test_files\\' + filename
        self.assertTrue(os.path.isfile(filepath))
        f = open(filepath)
        content = f.read()
        f.close()
        itr = BLAST_Rslts_Itr(content)
        
    
    
    def test_execution(self):
        """
        Tests the ability of the BLAST_Rslts_Itr_tests class to run a test.
        
        :param self: An instance of the BLAST_Rslts_Itr_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()