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
    def test_ec_search_error_checking(self):
        """
        Tests the Uniprot class member function 'ec_search()' on its ability to 
        perform error checking on the search terms passed into the function.
        
        :param self: An instance of the Unprot_tests class.
        """
        # Testing correct types. Expect no exception.   
        db = Uniprot()
        try:
            search_terms = [
                                ("All", "gnat family n-acetyltransferase"),
                                ("All", "geobacillus"),                           
                            ]
            db.ec_search(search_terms)
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
            db.ec_search(search_terms)
            error = False
        except:
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
            db.ec_search(search_terms)
            error = False
        except:
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
            db.ec_search(search_terms)
            error = False
        except:
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
            db.ec_search(search_terms)
            error = False
        except:
            error = True
        finally:
            if not error:
                self.assertTrue(False)
            else:
                self.assertTrue(True)
    
    
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
        
        
    def test_check_search_types(self):
        """
        Tests the ability of the Uniprot_tests class member function 
        ec_search() to check for correct types of the search fields.
        
        :param self: An instance of the Unprot_tests class.
        """
        # Testing correct types. Expect True returned.       
        search_terms = [
                            ("All", "gnat family n-acetyltransferase"),
                            ("All", "geobacillus"),                           
                        ]
        self.assertTrue(Uniprot.check_search_terms(search_terms)[0])
            
        # Testing incorrect type of search_terms parameter. Expect False.
        search_terms = set((
                            ("All", "gnat family n-acetyltransferase"),
                            ("All", "geobacillus"),                           
                            ))
        self.assertFalse(Uniprot.check_search_terms(search_terms)[0])

        # Testing incorrect types for elements of search_terms list. 
        # Expect False returned.
        search_terms = [
                            ("All", "gnat family n-acetyltransferase"), 
                            ["All", "geobacillus"]
                        ]
        self.assertFalse(Uniprot.check_search_terms(search_terms)[0])

        # Testing incorrect types for elements in tuples for elements of 
        # search_terms list. Expect False returned.
        search_terms = [("All", "gnat family n-acetyltransferase"), ("All", 1)]
        self.assertFalse(Uniprot.check_search_terms(search_terms)[0])            
                
        # Testing empty list for search_terms parameter. Expect False returned.
        search_terms = []
        self.assertFalse(Uniprot.check_search_terms(search_terms)[0])
 

if __name__ == '__main__':
    unittest.main()