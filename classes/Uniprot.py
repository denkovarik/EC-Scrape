class Uniprot():
    """
    Class for searching the Uniprot Database for EC Numbers for proteins.
    """
    def __init__():
        """
        Inizializes an instance of the Uniprot Class.
        """
        self.content = ""
    
    
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
                