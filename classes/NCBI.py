import requests
from Bio import Entrez 


class NCBI():
    """
    Class to make queries on the NCBI database
    """
    class Protein():
        """
        NCBI inner class to make searches on the NCBI Protein database
        """
        def __init__(self, ncbi_root_path):
            """
            Initializes an instance of the NCBI.Protein inner class.
            
            :param self: An instance of the NCBI class
            :param ncbi_root_path: The root path for the NCBI Protein databse
            """
            self.root_path = ncbi_root_path + "/protein/"
            
            
        def extract_ec(self, content, accession):
            """
            NCBI.Protein function to extract the ec number from a hit on NCBI.
                
            :param self: An instance of the NCBI.Protein class
            :param content: String from hit on NCBI Protein database.
            :param accession: The accession number of the protein
            """
            s = 0
            s = content.find('accession "' + accession + '"', s)
            s = content.rfind('seq {', 0, s)
            e = content.find('seq {', s + 1)
            if e == -1:
                section = content[s:]
            else:
                section = content[s:e]
            s = 0
            s = section.find('annot {', s)
            s = section.find('data ftable {', s)
            s = section.find('data prot {', s)
            s = section.find('ec {', s)
            s = section.find('"', s) + 1
            e = section.find('"', s)
            return section[s:e].strip()
            
            
        def extract_info(self, content, acc):
            """
            NCBI.Protein function to extract info from a hit on NCBI. The 
            info that this function will extract includes the following:
                * Protein name
                * Organism
                * EC number (if available)
                
            :param self: An instance of the NCBI.Protein class
            :param content: String from hit on NCBI Protein database.
            :param acc: The accession number of the protein
            """
            info = {}
            info['Protein name'] = self.extract_protein_name(content, acc)
            info['Organism'] = self.extract_organism(content)
            if self.has_ec(content, acc):
                info['EC Number'] = self.extract_ec(content, acc)
            return info
            
            
        def extract_organism(self, content):
            """
            NCBI.Protein function to extract the organism name from a hit on NCBI.
                
            :param self: An instance of the NCBI.Protein class
            :param content: String from hit on NCBI Protein database.
            """
            s = 0        
            s = content.find('taxname', s)
            s = content.find('"', s) + 1
            e = content.find('"', s)
            name = content[s:e].strip()
            return name
            
         
        def extract_protein_name(self, content, accession):
            """
            NCBI.Protein function to extract the protein name from a hit on NCBI.
                
            :param self: An instance of the NCBI.Protein class
            :param content: String from hit on NCBI Protein database.
            :param accession: The accession number of the protein
            """
            s = 0
            s = content.find('accession "' + accession + '"', s)
            s = content.rfind('seq {', 0, s)
            e = content.find('seq {', s + 1)
            if e == -1:
                section = content[s:]
            else:
                section = content[s:e]
            s = 0
            s = section.find('annot {', s)
            s = section.find('data ftable {', s)
            s = section.find('data prot {', s)
            s = section.find('name {', s)
            s = section.find('"', s) + 1
            e = section.find('"', s)
            return section[s:e].strip()
            
            
        def has_ec(self, content, accession):
            """
            Determines if a hit from the NCBI Protein database has an ec 
            number reported.
            
            :param self: An in stance of the NCBI.Protein class
            :param content: The string of the hit on NCBI
            :param accession: The accession number of the protein
            """
            s = 0
            s = content.find('accession "' + accession + '"', s)
            if content.rfind('seq {', 0, s) != -1:
                s = content.rfind('seq {', 0, s)
                e = content.find('seq {', s + 1)
                if e == -1:
                    section = content[s:]
                else:
                    section = content[s:e]
                s = 0
            s = section.find('annot {', s)
            s = section.find('data ftable {', s)
            s = section.find('data prot {', s)
            if section.find('ec {', s) == -1:
                return False
            return True
            
            
        def search(self, accession, email):
            """
            Makes a search on the NCBI Protein database using the Biopython
            library.
            
            :param self: An instance of the NCBI.Protein class.
            :param accession: The accesion number of the protein to search
            :param email: The user's email address
            """
            # NCBI may block users with no email :(
            Entrez.email = email
            # Make the search
            handle = Entrez.esearch(db="protein", term=accession, retmax=100)
            records = Entrez.read(handle)
            identifiers = records['IdList']
            if len(identifiers) == 0:
                raise Exception("No Results Found for " + accession)
            handle = Entrez.efetch(db="protein", id=identifiers[0])
            text = handle.read()
            # Extract necessary info
            info = self.extract_info(text, accession)
            return info
            
                         
        
    def __init__(self):
        """
        Initializes an instance of the NCBI class.
        
        :param self: An instance of the NCBI class
        """
        self.root_path = "https://www.ncbi.nlm.nih.gov"
        self.protein = NCBI.Protein(self.root_path)
        