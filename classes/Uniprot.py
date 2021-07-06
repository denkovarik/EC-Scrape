import requests


class Results_Itr():
    """
    Iterator to iterate through the results returned from a query on 
    Uniprot.
    """
    def __init__(self, content):
        """
        Initializes an instance of the Results_Itr class.
        
        :param self: An instance of the Results_Itr class
        :param content: The content from the html file of the Results from 
                        a query on Uniprot
        """
        # The content of the results .html file returned
        self.row = content
        # The current results as a dictionary
        self.cur = None
        # The current start and end positions within the html file
        self.start_pos = 0
        self.end_pos = 0
        self.cur_row = ''
        # Boolean to indicate if at end of results
        self.end = False
        # The features from the results row
        self.features = {}
        self.began = False
                    
            
    def __iter__(self):
        """
        The overload iter python built-in to make the class iterable.
        
        :param self: An instance of the Results_Itr class.
        """
        return self
        
        
    def __next__(self):
        """
        Sets the instance of the Results_Itr class to the next result of
        all the results returned from Uniprot.
            
        :param self: An instance of the Results_Itr class
        """
        if not self.began:
            self.began = True
            # Set the iterator to the first results
            self.begin()
        if not self.end:
            self.start_pos = self.row.find('<tr id=', self.end_pos)
            if self.start_pos == -1:
                self.end_itr()
                # Stop the iteration
                raise StopIteration
            self.end_pos = self.row.find('</tr>', self.start_pos) + 5
            if self.end_pos == -1:
                self.end_itr()
                # Stop the iteration
                raise StopIteration
            self.cur_row = self.row[self.start_pos:self.end_pos]
            # Extract the features
            self.extract_features(self.cur_row)
            return self.features
        # Stop the iteration
        raise StopIteration
            
            
    def begin(self):
        """
        Sets the instance of the Results_Itr class to the beginning of the
        results returned from Uniprot.
            
        :param self: An instance of the Results_Itr class
        """
        # The current results as a dictionary
        self.cur = None
        # The current start and end positions within the html file
        self.start_pos = 0
        self.end_pos = 0
        self.cur_row = ''
        # Boolean to indicate if at end of results
        self.end = False
        self.began = True
        # The features from the results row
        self.features = {}
        s = 0
        # Find the starting point of the results table
        s = self.row.find('<table class="grid" id="results">', s)
        if s == -1:
            self.end_itr()
            return
        s = self.row.find('<tr', s)
        if s == -1:
            self.end_itr()
            return
        e = self.row.find('</tr>', s)
        if e == -1:
            self.end_itr()
            return
        s = self.row.find('<tr', e)
        if s == -1:
            self.end_itr()
            return
        e = self.row.find('</tr>', s)
        if e == -1:
            self.end_itr()
            return
        
        
    def end_itr(self):
        """
        Marks the class as at the end of iteration.
        
        :param self: An instance of the Results_Itr class.
        """
        self.began = False
        self.end = True
            
            
    def extract_features(self, row):
        """
        Extracts the features from the 'row' parameter, which is a row from
        the results table from a Uniprot query. The features that are 
        currently being extracted are the id and the protein names.
         
        :param self: An instance of the Unprot class.
        :param row: A row from the results table in the html file as a String
        """
        self.features['id'] = self.get_entry_id(row)
        self.features['protein names'] = self.get_protein_names(row)
            
            
    def get_entry_id(self, row):
        """
        Returns the entry id found in the parameter 'row'.
            
        :param self: An instance of the Unprot class.
        :param row: A row from the results table in the html file as a String
        """
        s = row.find('<tr id=')
        s = row.find('"', s) + 1
        e = row.find('"', s)
        entry_id = row[s:e]
        return entry_id.strip()
        
        
    def get_protein_names(self, the_row, name=None):
        """
        Returns the protein names found in the parameter 'row'.
            
        :param self: An instance of the Unprot class.
        :param row: A row from the results table in the html file as a String
        :param name: The protein name to match the results to
        """
        s = the_row.find('<div class="long"')
        s = the_row.find('>', s) + 1
        e = the_row.find('</div>', s)
        protein_names = the_row[s:e].strip()
        return protein_names


class Uniprot():
    """
    Class for searching the Uniprot Database for EC Numbers for proteins.
    """
    def __init__(self):
        """
        Inizializes an instance of the Uniprot Class.
        """
        self.content = ""
        self.root = "https://www.uniprot.org"
        self.results_itr = None
        self.query = None
        
        
    def __iter__(self):
        """
        The overload iter python built-in to make the class iterable.
        
        :param self: An instance of the Uniprot class.
        """
        return Results_Itr(self.content)
        
        
    def build_query(self, search_terms, sort='score'):
        """
        Builds the url for the the Uniprot search query given search terms.
        
        :param self: Instance of the Uniprot class
        :param search_terms: A list of tuples of strings that search as the 
                             search terms and keywords for the Uniprot query.
        :param sort: Criteria for how to sort results. Default for Uniprot is 
                     'score'.
        :return: The url for the Uniprot search query as a String
        """
        # Error checking of search_terms parameter
        url = ""
        valid, err_msg = Uniprot.check_search_terms(search_terms)
        if not valid:
            raise Exception(err_msg)
        # Build the query
        url += self.root + '/uniprot/?query='
        start = True
        for i in search_terms:
            # Right now only the AND condition in implemented
            condition = "AND"
            # Check if the condition is specified
            if len(i) > 2:
                condition = i[2].upper()
            # Add condition
            if not start and condition == "AND" \
            and Uniprot.field_supported(i[0])[0]:
                url += '+'
            start = False
            # Search term for field 'All'
            if i[0].lower() == 'all':
                term = i[1].strip().replace(" ", "+")
                url += '"' + term + '"'
            # Search term for field 'Protein name'
            if i[0].lower() == 'protein name':
                term = i[1].strip().replace(" ", "+")
                url += 'name%3A"' + term + '"'
            # Search term for field 'Organism'
            if i[0].lower() == 'organism':
                term = i[1].strip().replace(" ", "+")
                url += 'organism%3A"' + term + '"'
            # Search term for field 'Organism'
            if i[0].lower() == 'reviewed':
                term = "yes"
                url += 'reviewed%3A' + term
        # Define the sort criteria
        url += '&sort=' + sort
        return url
            
    
    @staticmethod
    def check_search_terms(search_terms):
        """
        Checks the search terms in the parameter 'search_terms' for correct
        types and supported search fields in Uniprot.
        
        :param  search_terms: Search terms for the Uniprot search as a list of 
                              tuples of Strings.
        :return: True if the types in 'search_terms' is correct
        :return: False if types in 'search_terms' is invalid
        :return: An error message as a string
        """
        # Check the data types of search_terms
        if type(search_terms) is not list:
            err = "Parameter 'search_terms' must be a list"
            return False, err
        # Make sure that search_terms list is not empty
        if len(search_terms) == 0:
            err = "Parameter 'search_terms' must not be empty"
            return False, err
        # Check the types of the search_terms list
        for e in search_terms:
            if type(e) is not tuple:
                err = "Eelements in parameter 'search_terms' must be tuples."
                return False, err
            # Check the types of elements in tuples.
            for i in e:
                if type(i) != type("string"):
                    err = "Elements in tuples must me strings"
                    return False, err
            # Check if search field is supported
            supported, err = Uniprot.field_supported(e[0])
            if not supported:
                return False, err
        return True, "Types Valid"
    
    
    @staticmethod
    def field_supported(field):
        """
        Determines if a Uniprot search field is supported by this software or 
        by Uniprot itself.
        
        :param field: The Uniprot search field.
        :return: True if the search field is supported
        :return: False otherwise
        :return: An error message as a String
        """
        # Check the type of field
        if type(field) != type("string"):
            err = "Error in field_supported. Type of 'field' parameter must "
            err += "be a string."
            return False, err           
        # Check for field 'All'
        if field.lower() == "all":
            return True, "Field Supported"
        # Check for field 'Protein name'
        if field.lower() == "protein name":
            return True, "Field Supported"
        # Check for field 'Organism'
        if field.lower() == "organism":
            return True, "Field Supported"
        # Check for field 'Reviewed'
        if field.lower() == "reviewed":
            return True, "Field Supported"
        return False, "Field Not Supported"

    
    def make_request(self, url):
        """
        Wrapper function for making requests to Uniprot through their REST API
        for the html page of a search query.
        
        :param self: Instance of the Uniprot class
        :param url: The url of the search results on Uniprot.
        :return: The status code of the request as an int
        :return: The text returned from the request as a String 
        """
        # Make the request
        response = requests.get(url)
        return response.status_code, response.text
        
        
    def results_found(self, content):
        """
        Determines if results were found from a query on Uniprot.
        
        :param self: Instance of the Uniprot class
        :param content: The content of the html file from the request
        """
        return (content.find('<div id="noResultsMessage">') == -1)
                
        
    def search(self, search_terms):
        """
        Performs a REST API call to Uniport to make a query given search terms.
        
        :param self: Instance of the Uniprot class
        :param search_terms: A list of tuples of strings that search as the 
                             search terms and keywords for the Uniprot query.
        """
        self.query = self.build_query(search_terms)   
        status_code, self.content = self.make_request(self.query)
        self.results_itr = Results_Itr(self.content)