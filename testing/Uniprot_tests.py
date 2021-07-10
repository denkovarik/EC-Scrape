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
    def test_get_organism(self):
        """
        Tests the Uniprot class member function 'get_organism()' on its 
        ability to extract the source organism from a row.
        
        :param self: An instance of the Uniprot_tests class
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        f.close()
        itr = Results_Itr(content)
        # Test calling Results_Itr class member function begin()
        itr.begin()
        itr.__next__()
        protein_names = itr.get_organism(itr.cur_row)
        expected = 'Geobacillus sp. WSUCF-018B'
        self.assertTrue(protein_names == expected)
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.result_itr = Results_Itr(content)
        itr = iter(db.result_itr)
        itr.begin()
        itr.__next__()
        protein_names = itr.get_organism(itr.cur_row)
        self.assertTrue(protein_names == expected)
        
        
    def test_bug_fix2(self):
        """
        Tests the bug fix where html tags are being included it the text
        that is being scraped from Uniprot.
        
        :param self: An instance of the Uniprot_tests class
        """
        path = currentdir + "\\test_files\\carbonic_anhydrase_.htm"
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        db = Uniprot()
        db.content = content
        db.results_itr = Results_Itr(content)
        itr = iter(db)
        features = next(itr)    
        proteins = "Carbonic anhydrase 6, EC 4.2.1.1 (Carbonate dehydratase VI)  (Carbonic anhydrase VI, CA-VI)  (Salivary carbonic anhydrase)  (Secreted carbonic anhydrase)"
        self.assertTrue(features['protein names'] == proteins)
        f.close()
        
        
    def test_bug_fix1(self):
        """
        Tests the bug fix where iterator doesn't start all the way at the
        beginning with .begin() is called.
        
        :param self: An instance of the Uniprot_tests class
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            content = f.read()
        f.close()
        db.content = content
        db.results_itr = Results_Itr(content)
        itr = iter(db)
        features = next(itr)
        self.assertTrue(features['id'] == 'A0A2M9T2M7')
        proteins = 'GNAT family N-acetyltransferase, EC 2.3.1.1'
        self.assertTrue(features['protein names'] == proteins)
        features = next(itr)
        self.assertTrue(features['id'] == 'A0A2Z3N999')
        proteins = 'GNAT family N-acetyltransferase'
        self.assertTrue(features['protein names'] == proteins)
        itr.begin()
        features = next(itr)
        self.assertTrue(features['id'] == 'A0A2M9T2M7')
        proteins = 'GNAT family N-acetyltransferase, EC 2.3.1.1'
        self.assertTrue(features['protein names'] == proteins)
        
        
    def test_extract_features(self):
        """
        Tests the Uniprot class Results_Itr member function 
        'extract_features()' on its ability to extract the features from a
        row from the results table returned from a query on Uniprot.
        
        :param self: An instance of the Unprot_tests class.
        :param row: A row from the results table in the html file as a String
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        f.close()
        itr = Results_Itr(content)
        # Testing first row
        # Function 'extract_features()' called in Results_Itr class function 
        # 'begin()'
        itr.__next__()
        self.assertTrue(itr.features['id'] == 'A0A2M9T2M7')
        proteins = 'GNAT family N-acetyltransferase, EC 2.3.1.1'
        self.assertTrue(itr.features['protein names'] == proteins)
        org = 'Geobacillus sp. WSUCF-018B'
        self.assertTrue(itr.features['organism'] == org)
        # Iterate to the next result.
        # Function 'extract_features()' called in Results_Itr class function 
        # '__next__()'
        itr.__next__()
        self.assertTrue(itr.features['id'] == 'A0A2Z3N999')
        proteins = 'GNAT family N-acetyltransferase'
        self.assertTrue(itr.features['protein names'] == proteins)
        org = 'Geobacillus thermoleovorans (Bacillus thermoleovorans)'
        self.assertTrue(itr.features['organism'] == org)
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.result_itr = Results_Itr(content)
        itr = iter(db.result_itr)
        next(itr)
        self.assertTrue(itr.features['id'] == 'A0A2M9T2M7')
        proteins = 'GNAT family N-acetyltransferase, EC 2.3.1.1'
        self.assertTrue(itr.features['protein names'] == proteins)
        org = 'Geobacillus sp. WSUCF-018B'
        self.assertTrue(itr.features['organism'] == org)
        next(itr)
        self.assertTrue(itr.features['id'] == 'A0A2Z3N999')
        proteins = 'GNAT family N-acetyltransferase'
        self.assertTrue(itr.features['protein names'] == proteins)
        org = 'Geobacillus thermoleovorans (Bacillus thermoleovorans)'
        self.assertTrue(itr.features['organism'] == org)
        
        
    def test_get_protein_name_short(self):
        """
        Tests the Uniprot class Results_Itr member function 
        'get_protein_name_short()' on its ability to identify and return the 
        short version of the proteinname found in a row from the results 
        table returned from a query on Uniprot.
        
        :param self: An instance of the Unprot_tests class.
        :param row: A row from the results table in the html file as a String
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        f.close()
        itr = Results_Itr(content)
        # Test calling Results_Itr class member function begin()
        itr.begin()
        itr.__next__()
        protein_names = itr.get_protein_name_short(itr.cur_row)
        expected = 'GNAT family N-acetyltransferase'
        self.assertTrue(protein_names == expected)
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.result_itr = Results_Itr(content)
        itr = iter(db.result_itr)
        itr.begin()
        itr.__next__()
        protein_names = itr.get_protein_name_short(itr.cur_row)
        self.assertTrue(protein_names == expected)
        
        
    def test_get_protein_names(self):
        """
        Tests the Uniprot class Results_Itr member function 
        'get_protein_names()' on its ability to identify and return the protein
        names found in a row from the results table returned from a query on 
        Uniprot.
        
        :param self: An instance of the Unprot_tests class.
        :param row: A row from the results table in the html file as a String
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        f.close()
        itr = Results_Itr(content)
        # Test calling Results_Itr class member function begin()
        itr.begin()
        itr.__next__()
        protein_names = itr.get_protein_names(itr.cur_row)
        expected = 'GNAT family N-acetyltransferase, EC 2.3.1.1'
        self.assertTrue(protein_names == expected)
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.result_itr = Results_Itr(content)
        itr = iter(db.result_itr)
        itr.begin()
        itr.__next__()
        protein_names = itr.get_protein_names(itr.cur_row)
        self.assertTrue(protein_names == expected)
        
        
    def test_get_entry_id(self):
        """
        Tests the Uniprot class Results_Itr member function 
        'get_entry_id()' on its ability to identify and return the entry id
        found in a row from the results table returned from a query on Uniprot.
        
        :param self: An instance of the Unprot_tests class.
        :param row: A row from the results table in the html file as a String
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        f.close()
        itr = Results_Itr(content)
        # Test calling Results_Itr class member function begin()
        itr.begin()
        itr.__next__()
        self.assertTrue(itr.get_entry_id(itr.cur_row) == 'A0A2M9T2M7')
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.result_itr = Results_Itr(content)
        itr = iter(db.result_itr)
        itr.begin()
        itr.__next__()
        self.assertTrue(itr.get_entry_id(itr.cur_row) == 'A0A2M9T2M7')
        
    
    def test_Result_Itr_next(self):
        """
        Tests the Uniprot class Results_Itr member function __next__()        
        on its ability to identify the beginning of the results returned from
        a query on Uniprot.
        
        :param self: An instance of the Unprot_tests class.
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        f.close()
        itr = Results_Itr(content)
        # Test calling Results_Itr class member function begin()
        itr.begin()
        itr.__next__()
        #itr.__next__()
        cur_expected = '<tr id="A0A2M9T2M7" class=" entry selected-row"><td class="checkboxColumn"><input class="basket-item namespace-uniprot" id="checkbox_A0A2M9T2M7" type="checkbox"/></td><td class="entryID"><a href="/uniprot/A0A2M9T2M7">A0A2M9T2M7</a></td><td>A0A2M9T2M7_9BACI</td><td class="centered"><div title="Unreviewed (TrEMBL)" class="tooltipped icon-uniprot unreviewed-icon" data-icon="t"></div></td><td><div class="protein_names"><div class="short" title="GNAT family N-acetyltransferase" style="display:none;">GNAT family N-acetyltransferase</div><div class="long">GNAT family N-acetyltransferase, EC 2.3.1.1 </div></div></td><td><div class="gene-names"><span class="shortName"> CV944_10475 </span></div></td><td><a href="/taxonomy/2055939">Geobacillus sp. WSUCF-018B</a></td><td class="number">150</td><td class="addRemoveColumn mid"/></tr>'
        self.assertTrue(itr.cur_row == cur_expected)
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.results_itr = Results_Itr(content)
        itr = iter(db.results_itr)
        itr.begin()
        row = next(itr)
        self.assertTrue(itr.cur_row == cur_expected)
        num_results = 0
        db = Uniprot()
        db.content = content
        db.results_itr = Results_Itr(content)
        itr = iter(db.results_itr)
        for row in db.results_itr:
            num_results += 1
        self.assertTrue(num_results == 25)
        
        
    def test_Results_Itr_int(self):    
        """
        Tests the initalization of the Uniprot class Results_Itr.
        
        :param self: An instance of the Unprot_tests class.
        """
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        itr = Results_Itr(content)
        # Testing default initialization
        self.assertTrue(itr.row == content)
        self.assertTrue(itr.end == False)
        f.close()
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.result_itr = Results_Itr(content)
        itr = iter(db.result_itr)
        self.assertTrue(itr.row == content)
        self.assertTrue(itr.end == False)
        
    
    def test_Results_Itr_begin(self):
        """
        Tests the Uniprot class Results_Itr member function begin on its
        ability to identify the beginning of the results returned from a 
        query on Uniprot.
        
        :param self: An instance of the Unprot_tests class.
        """
        db = Uniprot()
        path = currentdir + '\\test_files\\iterator_test.htm'
        with open(path) as f:
            content = f.read()
        itr = Results_Itr(content)
        # Test calling Results_Itr class member function begin()
        itr.begin()
        itr.__next__()
        self.assertTrue(itr.start_pos == 70333)
        self.assertTrue(itr.end_pos == 71164)
        cur_expected = '<tr id="A0A2M9T2M7" class=" entry selected-row"><td class="checkboxColumn"><input class="basket-item namespace-uniprot" id="checkbox_A0A2M9T2M7" type="checkbox"/></td><td class="entryID"><a href="/uniprot/A0A2M9T2M7">A0A2M9T2M7</a></td><td>A0A2M9T2M7_9BACI</td><td class="centered"><div title="Unreviewed (TrEMBL)" class="tooltipped icon-uniprot unreviewed-icon" data-icon="t"></div></td><td><div class="protein_names"><div class="short" title="GNAT family N-acetyltransferase" style="display:none;">GNAT family N-acetyltransferase</div><div class="long">GNAT family N-acetyltransferase, EC 2.3.1.1 </div></div></td><td><div class="gene-names"><span class="shortName"> CV944_10475 </span></div></td><td><a href="/taxonomy/2055939">Geobacillus sp. WSUCF-018B</a></td><td class="number">150</td><td class="addRemoveColumn mid"/></tr>'
        self.assertTrue(itr.cur_row == cur_expected)
        f.close()
        # Testing with Python's iter built-in function
        db = Uniprot()
        db.content = content
        db.results_itr = Results_Itr(content)
        itr = iter(db.results_itr)
        itr.begin()
        next(itr)
        self.assertTrue(itr.start_pos == 70333)
        self.assertTrue(itr.end_pos == 71164)
        
        
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
        f.close()
        # Testing on results found
        with open(results_file) as f:
            content = f.read()
        self.assertTrue(db.results_found(content))
        f.close()
        
        
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