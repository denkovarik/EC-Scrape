class Uniprot():
    """
    Class for searching the Uniprot Database for EC Numbers for proteins.
    """
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
    def ec_search(search_terms):
        """
        Performs a search on Uniprot via REST Api give search terms.
        
        :param  search_terms: Search terms for the Uniprot search as a list of 
                              tuples of Strings.
        :return: A set of EC numbers from the search
        """
        # Check the data types of search_terms
        if type(search_terms) is not list:
            err = "Error in Uniprot class member function 'ec_search()'. "
            err += "Parameter 'search_terms' must be a list"
            raise TypeError(err)
        # Make sure that search_terms list is not empty
        if len(search_terms) == 0:
            err = "Error in Uniprot class member function 'ec_search()'. "
            err += "Parameter 'search_terms' must not be empty"
            raise Exception(err)
        # Check the types of the search_terms list
        for e in search_terms:
            if type(e) is not tuple:
                err = "Error in Uniprot class member function 'ec_search()'. "
                err += "Eelements in parameter 'search_terms' must be tuples."
                raise TypeError(err)
            # Check the types of elements in tuples.
            for i in e:
                if type(i) != type("string"):
                    err = "Error in Uniprot class member function 'ec_search()'. "
                    err += "Elements in tuples must me strings"
                    raise TypeError(err)
            # Check if search field is supported
            supported, err = Uniprot.field_supported(e[0])
            if not supported:
                raise Exception(error)
                