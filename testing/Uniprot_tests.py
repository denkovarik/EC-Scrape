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
    def test_results_found(self):
        """
        Tests the Uniprot class member function 'results_found()' on its ability to
        determine if results were returned from a query on Uniprot.
        
        :param self: An instance of the Unprot_tests class.
        """
        db = Uniprot()
        no_results_file = currentdir + "\\test_files\\no_results_found.htm"
        results_file = currentdir + "\\test_files\\results_found.htm"
        # Testing no results found
        with open(no_results_file) as f:
            content = f.read()
        self.assertFalse(db.results_found(content))
        # Testing on results found
        with open(results_file) as f:
            content = f.read()
        self.assertTrue(db.results_found(content))
        
        
    def test_make_request(self):
        """
        Tests the Uniprot class member function 'make_request()' on its ability to
        make a request for the .html file for the Uniprot search results.
        
        :param self: An instance of the Unprot_tests class.
        """
        db = Uniprot()
        # Testing valid request
        url = 'https://www.uniprot.org/uniprot/?query='
        url += '"gnat+family+n-acetyltransferase"+"geobacillus"&sort=score'        
        status, content = db.make_request(url)
        self.assertTrue(status == 200)
        
        
    def test_build_query(self):
        """
        Tests the Uniprot class member function 'build_query()' on its ability
        to create the url for the Uniprot query from the search terms given.
        
        :param self: An instance of the Unprot_tests class.
        """
        db = Uniprot()
        # Testing for protein 'gnat family n-acetyltransferase' and organism 
        # 'geobacillus'
        protein_name = "gnat family n-acetyltransferase"
        organism = "geobacillus"
        #######################################################################
        # Testing field 'All' for protein and field 'All' for organism
        protein_field = "All"
        organism_field = "All"
        condition = "AND"
        search_terms = [
                            (protein_field, protein_name, condition),
                            (organism_field, organism),                           
                        ]
        expected = 'https://www.uniprot.org/uniprot/?query="gnat+family'
        expected += '+n-acetyltransferase"+"geobacillus"&sort=score'
        url = db.build_query(search_terms)
        self.assertTrue(url == expected)
        # Testing field reviewed for reviewed and field 'All' for protein and
        # field 'All' for organism
        protein_field = "All"
        organism_field = "All"
        condition = "AND"
        search_terms = [
                            (protein_field, protein_name, condition),
                            (organism_field, organism),    
                            ("Reviewed", "Reviewed"),                            
                        ]
        expected = 'https://www.uniprot.org/uniprot/?query='
        expected += '"gnat+family+n-acetyltransferase"+"geobacillus"'
        expected += '+reviewed%3Ayes&sort=score'
        url = db.build_query(search_terms)
        self.assertTrue(url == expected)
        # Testing field 'Protein name' for protein and field 'All' for organism
        protein_field = "Protein name"
        organism_field = "All"
        search_terms = [
                            (protein_field, protein_name),
                            (organism_field, organism),                           
                        ]
        expected = 'https://www.uniprot.org/uniprot/?query=name%3A"gnat+family'
        expected += '+n-acetyltransferase"+"geobacillus"&sort=score'
        url = db.build_query(search_terms)
        self.assertTrue(url == expected)
        # Testing field 'All' for protein and field 'Organism' for organism
        protein_field = "All"
        organism_field = "Organism"
        search_terms = [
                            (protein_field, protein_name),
                            (organism_field, organism),                           
                        ]
        expected = 'https://www.uniprot.org/uniprot/?query="gnat+family'
        expected += '+n-acetyltransferase"+organism%3A"geobacillus"&sort=score'
        url = db.build_query(search_terms)
        self.assertTrue(url == expected)
        # Testing field 'Protein name' for protein and field 'Organism' for 
        # organism
        protein_field = "Protein name"
        organism_field = "Organism"
        search_terms = [
                            (protein_field, protein_name),
                            (organism_field, organism),                           
                        ]
        expected = 'https://www.uniprot.org/uniprot/?query=name%3A"gnat'
        expected += '+family+n-acetyltransferase"+organism%3A"geobacillus"'
        expected += '&sort=score'
        url = db.build_query(search_terms)
        self.assertTrue(url == expected)
        #######################################################################
        
        
    def test_build_query_error_checking(self):
        """
        Tests the Uniprot class member function 'build_query()' on its ability to 
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
            db.build_query(search_terms)
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
            db.build_query(search_terms)
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
            db.build_query(search_terms)
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
            db.build_query(search_terms)
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
            db.build_query(search_terms)
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
                        ("Reviewed", "Reviewed"),
                        ]
        # Testing field 'All'
        self.assertTrue(Uniprot.field_supported(search_terms[0][0])[0])
        # Testing field 'Protein name'
        self.assertTrue(Uniprot.field_supported(search_terms[1][0])[0])
        # Testing field 'Organism'
        self.assertTrue(Uniprot.field_supported(search_terms[2][0])[0])
        # Testing field 'Reviewed'
        self.assertTrue(Uniprot.field_supported(search_terms[3][0])[0])
        
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