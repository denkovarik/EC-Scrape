from Bio import Entrez 

Entrez.email = "dennis.kovarik@mines.sdsmt.edu"
handle = Entrez.esearch(db="protein", term="WP_011887816", retmax=100)
records = Entrez.read(handle)
identifiers = records['IdList']
handle = Entrez.efetch(db="protein", id=identifiers)
text = handle.read()
print(text)