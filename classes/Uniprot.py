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
            if not start and condition == "AND":
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
        # Define the sort criteria
        url += '&sort=' + sort
        return url
        
        
    def ec_search(self, search_terms):
        """
        Performs a REST API call to Uniport to make a query given search terms.
        
        :param self: Instance of the Uniprot class
        :param search_terms: A list of tuples of strings that search as the 
                             search terms and keywords for the Uniprot query.
        :return: A set of EC Numbers.
        """
            
        return ec
    
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
            # Check for field 'All'
        if field.lower() == "protein name":
            return True, "Field Supported"
        if field.lower() == "organism":
            return True, "Field Supported"
        return False, "Field Not Supported"
    
    
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
                