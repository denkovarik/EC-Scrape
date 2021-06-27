import unittest
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from classes.Uniprot import *


class Uniprot_tests(unittest.TestCase):
    """
    Runs all tests for the Uniprot class.
    """
    def test_execution(self):
        """
        Tests the ability of the Uniprot_tests class to run a test.
        
        :param self: An instance of the Unprot_tests class.
        """
        self.assertTrue(True)
        
        
    def test_field_supported(self):
        """
        Tests the function field_supported() on its ability to perform determine
        which search fields are supported for Uniprot. 
        
        :param self: An instance of the Unprot_tests class.
        """
        # Testing supported fields
        search_terms = [
                        ("All", "gnat family n-acetyltransferase"),
                        ("Protein name", "gnat family n-acetyltransferase"),
                        ("Organism", "geobacillus"),                           
                        ]
        # Testing field 'All'
        self.assertTrue(Uniprot.field_supported(search_terms[0][0]))
        # Testing field 'Protein name'
        self.assertTrue(Uniprot.field_supported(search_terms[1][0]))
        # Testing field 'Organism'
        self.assertTrue(Uniprot.field_supported(search_terms[2][0]))
        
        # Testing unsupported fields
        search_terms = [
                        ("Pie", "gnat family n-acetyltransferase"),
                        (1, "gnat family n-acetyltransferase"),
                        ("animal", "geobacillus"),                           
                        ]
        self.assertFalse(Uniprot.field_supported(search_terms[0][0])[0])
        self.assertFalse(Uniprot.field_supported(search_terms[1][0])[0])
        self.assertFalse(Uniprot.field_supported(search_terms[2][0])[0])
        
        
    def test_ec_search_types(self):
        """
        Tests the ability of the Uniprot_tests class member function 
        ec_search() to check for correct types of the search fields.
        
        :param self: An instance of the Unprot_tests class.
        """
        # Testing correct types. Expect no exception.       
        try:
            search_terms = [
                            ("All", "gnat family n-acetyltransferase"),
                            ("All", "geobacillus"),                           
                            ]
            Uniprot.ec_search(search_terms)
            self.assertTrue(True)
        except:
            self.assertTrue(False)
            
        # Testing incorrect type of search_terms parameter. Expect exception.
        error = False
        try:
            search_terms = set((
                            ("All", "gnat family n-acetyltransferase"),
                            ("All", "geobacillus"),                           
                            ))
            Uniprot.ec_search(search_terms)
            error = False
        except TypeError:
            error = True
        finally:
            if not error:
                self.assertTrue(False)
            else:
                self.assertTrue(True)

        # Testing incorrect types for elements of search_terms list. 
        # Expect exception.
        error = False
        try:
            search_terms = [
                                ("All", "gnat family n-acetyltransferase"),
                                ["All", "geobacillus"],                           
                            ]
            Uniprot.ec_search(search_terms)
            error = False
        except TypeError:
            error = True
        finally:
            if not error:
                self.assertTrue(False)
            else:
                self.assertTrue(True)
                
        # Testing incorrect types for elements in tuples for elements of 
        # search_terms list. Expect exception.
        error = False
        try:
            search_terms = [
                                ("All", "gnat family n-acetyltransferase"),
                                ("All", 1),                           
                            ]
            Uniprot.ec_search(search_terms)
            error = False
        except TypeError:
            error = True
        finally:
            if not error:
                self.assertTrue(False)
            else:
                self.assertTrue(True)             
                
        # Testing empty list for search_terms parameter. Expect exception.
        error = False
        try:
            search_terms = []
            Uniprot.ec_search(search_terms)
            error = False
        except:
            error = True
        finally:
            if not error:
                self.assertTrue(False)
            else:
                self.assertTrue(True)
 

if __name__ == '__main__':
    unittest.main()