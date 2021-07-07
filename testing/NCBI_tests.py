import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from classes.NCBI import *


class NCBI_tests(unittest.TestCase):
    """
    Runs all tests for the Uniprot class.
    """
    def test_search(self):
        """
        Tests doing a search on the NCBI protein database. PLEASE NOTE THAT
        TESTS IN THIS TEST CASE MAY BREAK IF NCBI CHANGES THE ENTRY FOR
        THE ACCESSION NUMBER CAI38050. This should be the only test case
        that is susceptible to this.
        
        :param self: An instance of the NCBI_tests class.
        """
        # naphthoate synthase search
        ncbi = NCBI()
        accession = "CAI38050"
        exp =   {
                    'Protein name': 'naphthoate synthase', 
                    'Organism': 'Corynebacterium jeikeium K411', 
                    'EC Number': '4.1.3.36'
                }
        email = "dennis.kovarik@mines.sdsmt.edu"
        rslt = ncbi.protein.search(accession, email)
        self.assertTrue(rslt == exp)
        # Test with no expected results
        ncbi = NCBI()
        accession = "WP_NOT!!!"
        email = "dennis.kovarik@mines.sdsmt.edu"
        err = False
        try:
            rslt = ncbi.protein.search(accession, email)
            err = False
        except:
            err = True
        finally:
            self.assertTrue(err)
        
        
    def test_extract_ec(self):
        """
        Tests the NCBI.Protein member function 'extract_ec()' on its
        ability to retreive the ec number from the hit on the NCBI protein 
        database.
        
        :param self: An instance of the NCBI_tests class.
        """
        # naphthoate synthase hit
        path = currentdir + "\\test_files\\biopython_entrez_naphthoate_synthase_[Corynebacterium_jeikeium_K411].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "CAI38050"
        self.assertTrue(ncbi.protein.extract_ec(content, accession) == '4.1.3.36')
        # Glucose-1-phosphate adenylyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_Glucose-1_phosphate_adenylyltransferase_[Oscillatoria_nigro_viridis_PCC_7112].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "AFZ06929"
        self.assertTrue(ncbi.protein.extract_ec(content, accession) == '2.7.7.27')
    
        
    def test_has_ec(self):
        """
        Tests the NCBI.Protein member function 'has_ec()' on its ability to 
        determine if a hit on NCBI has an ec number reported.
        
        :param self: An instance of the NCBI_tests class.
        """
        # naphthoate synthase hit
        path = currentdir + "\\test_files\\biopython_entrez_naphthoate_synthase_[Corynebacterium_jeikeium_K411].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "CAI38050"
        self.assertTrue(ncbi.protein.has_ec(content, accession))
        # GNAT family N-acetyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_GNAT_family_N_acetyltransferase_[Geobacillus].txt"
        with open(path) as f:
            content = f.read()
        f.close()
        self.assertTrue(os.path.isfile(path))
        ncbi = NCBI()
        accession = "WP_008881006"
        self.assertFalse(ncbi.protein.has_ec(content, accession))
        # Glucose-1-phosphate adenylyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_Glucose-1_phosphate_adenylyltransferase_[Oscillatoria_nigro_viridis_PCC_7112].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "AFZ06929"
        self.assertTrue(ncbi.protein.has_ec(content, accession))
        # aminodeoxychorismate lyase hit
        path = currentdir + "\\test_files\\biopython_entrez_aminodeoxychorismate_lyase_[Geobacillus].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "WP_011887816"
        self.assertFalse(ncbi.protein.has_ec(content, accession))
        
        
    def test_extract_organism(self):
        """
        Tests the NCBI.Protein member function 'extract_protein_name()' on its
        ability to retreive the organism name from the hit on the NCBI 
        protein database.
        
        :param self: An instance of the NCBI_tests class.
        """
        # naphthoate synthase hit
        path = currentdir + "\\test_files\\biopython_entrez_naphthoate_synthase_[Corynebacterium_jeikeium_K411].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        exp = "Corynebacterium jeikeium K411"
        self.assertTrue(ncbi.protein.extract_organism(content) == exp)
        # GNAT family N-acetyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_GNAT_family_N_acetyltransferase_[Geobacillus].txt"
        with open(path) as f:
            content = f.read()
        f.close()
        self.assertTrue(os.path.isfile(path))
        ncbi = NCBI()
        exp = "Geobacillus"
        self.assertTrue(ncbi.protein.extract_organism(content) == exp)
        # Glucose-1-phosphate adenylyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_Glucose-1_phosphate_adenylyltransferase_[Oscillatoria_nigro_viridis_PCC_7112].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "AFZ06929"
        exp = "Oscillatoria nigro-viridis PCC 7112"
        self.assertTrue(ncbi.protein.extract_organism(content) == exp)
        # aminodeoxychorismate lyase hit
        path = currentdir + "\\test_files\\biopython_entrez_aminodeoxychorismate_lyase_[Geobacillus].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "WP_011887816"
        exp = "Geobacillus"
        self.assertTrue(ncbi.protein.extract_organism(content) == exp)
    

    def test_extract_Protein_Name(self):
        """
        Tests the NCBI.Protein member function 'extract_protein_name()' on its
        ability to retreive the protein name from the hit on the NCBI protein 
        database.
        
        :param self: An instance of the NCBI_tests class.
        """
        # naphthoate synthase hit
        path = currentdir + "\\test_files\\biopython_entrez_naphthoate_synthase_[Corynebacterium_jeikeium_K411].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "CAI38050"
        exp = "naphthoate synthase"
        self.assertTrue(ncbi.protein.extract_protein_name(content, accession) == exp)
        # GNAT family N-acetyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_GNAT_family_N_acetyltransferase_[Geobacillus].txt"
        with open(path) as f:
            content = f.read()
        f.close()
        self.assertTrue(os.path.isfile(path))
        ncbi = NCBI()
        accession = "WP_008881006"
        exp = "GNAT family N-acetyltransferase"
        self.assertTrue(ncbi.protein.extract_protein_name(content, accession) == exp)
        # Glucose-1-phosphate adenylyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_Glucose-1_phosphate_adenylyltransferase_[Oscillatoria_nigro_viridis_PCC_7112].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "AFZ06929"
        exp = "Glucose-1-phosphate adenylyltransferase"
        self.assertTrue(ncbi.protein.extract_protein_name(content, accession) == exp)
        # aminodeoxychorismate lyase hit
        path = currentdir + "\\test_files\\biopython_entrez_aminodeoxychorismate_lyase_[Geobacillus].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "WP_011887816"
        exp = "aminodeoxychorismate lyase"
        self.assertTrue(ncbi.protein.extract_protein_name(content, accession) == exp)
    
    
    def test_extract_info(self):
        """
        Tests the NCBI.Protein member function 'extract_info()' on its ability
        to retreive the protein name, organism, and ec number (if available)
        from the hit on the NCBI protein database.
        
        :param self: An instance of the NCBI_tests class.
        """
        # naphthoate synthase hit
        path = currentdir + "\\test_files\\biopython_entrez_naphthoate_synthase_[Corynebacterium_jeikeium_K411].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        ncbi = NCBI()
        accession = "CAI38050"
        exp =   {
                    'Protein name': 'naphthoate synthase', 
                    'Organism': 'Corynebacterium jeikeium K411', 
                    'EC Number': '4.1.3.36'
                }
        self.assertTrue(ncbi.protein.extract_info(content, accession) == exp)
        f.close()
        # GNAT family N-acetyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_GNAT_family_N_acetyltransferase_[Geobacillus].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        ncbi = NCBI()
        accession = "WP_008881006"
        exp =   {
                    'Protein name': 'GNAT family N-acetyltransferase', 
                    'Organism': 'Geobacillus'
                }
        self.assertTrue(ncbi.protein.extract_info(content, accession) == exp)
        f.close()
        # Glucose-1-phosphate adenylyltransferase hit
        path = currentdir + "\\test_files\\biopython_entrez_Glucose-1_phosphate_adenylyltransferase_[Oscillatoria_nigro_viridis_PCC_7112].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "AFZ06929"
        exp = {
                'Protein name': 'Glucose-1-phosphate adenylyltransferase', 'Organism': 'Oscillatoria nigro-viridis PCC 7112', 
                'EC Number': '2.7.7.27'
               }
        self.assertTrue(ncbi.protein.extract_info(content, accession) == exp)
        # aminodeoxychorismate lyase hit
        path = currentdir + "\\test_files\\biopython_entrez_aminodeoxychorismate_lyase_[Geobacillus].txt"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        ncbi = NCBI()
        accession = "WP_011887816"
        exp =   {   'Protein name': 'aminodeoxychorismate lyase', 
                    'Organism': 'Geobacillus'
                }
        self.assertTrue(ncbi.protein.extract_info(content, accession) == exp)
        
        
    def test_init(self):
        """
        Tests the initialization of the NCBI class and Protein inner class.
        
        :param self: An instance of the NCBI_tests class.
        """
        ncbi = NCBI()
        self.assertTrue(str(type(ncbi)) == "<class 'classes.NCBI.NCBI'>")
        self.assertTrue(str(type(ncbi.protein)) \
            == "<class 'classes.NCBI.NCBI.Protein'>")
        self.assertTrue(ncbi.root_path == "https://www.ncbi.nlm.nih.gov")
        self.assertTrue(ncbi.protein.root_path \
            == "https://www.ncbi.nlm.nih.gov/protein/")
        
        
        
    def test_execution(self):
        """
        Tests the ability of the NCBI_tests class to run a test.
        
        :param self: An instance of the NCBI_tests class.
        """
        self.assertTrue(True)
     

if __name__ == '__main__':
    unittest.main()