import xml.etree.cElementTree as et
from classes.NCBI import NCBI
from classes.Uniprot import *
from classes.Annot_Reader import *


def ec_scrape(acc, email, max_uniprot_hits):
    """
    Scrapes the web for the ec number for the protein with the given 
    accession number.
    
    :param acc: The accession number to scrape the web for.
    :param email: The users email
    :param max_uniprot_hits: The max number of hits on Uniprot to use.
    :return: The results as a string
    """
    # Query NCBI database for EC number through the entrez database
    ncbi = NCBI()
    rslt = ncbi.protein.search(acc, email)
    uniprot = Uniprot()
    rslt_found = ""
    # If EC number not found from above, the query Uniprot Database for it
    if not 'EC Number' in rslt.keys():
        srch = [("Protein name",rslt['Protein name']), \
                ("Organism",rslt['Organism'])]
        uniprot.search(srch)
        itr = iter(uniprot)
        for i in itr:
            if Annot_Reader.has_ec(i['protein names']):
                proteins = tag_ec(i['protein names'])
                rslt_found += '(EC-Scraped (' + proteins + ' [' + i['organism'] + '] ' + 'UniProtKB: ' + i['id'] + ')) '
    else:
        rslt_found = "(EC-Scraped (" + rslt['Protein name'] + " [" + rslt['Organism'] + '] ' + "(NCBI Protein Accession: " + acc + ") " + '(EC-Scraped EC ' + rslt['EC Number'] + ')))'
    return rslt_found
    
    
def extract_ec(txt):
    """
    Extracts an EC number from a string. Note that this function will not
    modify the original string. It will just find the EC number in the 
    string.
    
    :param txt: The string to extract the EC number from.
    :return: The extracted ec number
    """
    # Make sure that txt has an EC number in it
    if not Annot_Reader.has_ec(txt):
        return ""
    # Find the position of the EC number
    s = -1
    while s < len(txt):
        s += 1
        break_now = False
        temp = s
        s = txt.find("EC ", s + 1)
        if s == -1:
            s = temp
            s = txt.find("EC: ", s)
            if s == -1:
                return ""
            else:
                s += 4
        else:
            s += 3
        # EC 
        if s >= len(txt):
            return ""
        if not txt[s].isdigit():
            break_now = True
        e = txt.find('.', s)
        if e == -1:
            return ""
        elif not break_now:
            t = s
            while t < e:
                if not txt[t].isdigit():
                    t = e
                    break_now = True
                    break
                t += 1
            if not break_now:
                # If this far, then 'EC #.' at least
                t = e
                e = txt.find('.', e + 1)
                if e == -1:
                    return ""
                else:
                    # t on period, make sure following chars are digit or '-' 
                    # until index e is reached
                    while t < e:
                        if not txt[t].isdigit() and txt[t] == '-':
                            t = e
                            break_now = True
                            break
                        t += 1
                    if not break_now:
                        # EC #.#.
                        e = txt.find('.', e + 1)
                        if e == -1:
                            return ""
                        t += 1
                        while t < e:
                            if not txt[t].isdigit() and txt[t] != '-':
                                t = e
                                break_now = True
                                break
                            t += 1
                        if not break_now:
                            # EC #.#.#.
                            e += 1
                            if not txt[e].isdigit() and txt[e] != '-':
                                t = e
                                break_now = True
                                break
                            while e < len(txt): 
                                if not txt[e].isdigit() and txt[e] != '-':   
                                    break
                                e += 1
                            return txt[s:e]
    return ""
        
    


def parse_blast_xml(xml, seq_len = None):
    """
    Parses the xml from a blast and returns the results in a list of 
    dictionaries.
    
    :param xml: The xml output as a string
    :return: The blast data as a list of dictionaries
    """
    out = []
    # Parse xml from a string
    root = et.fromstring(xml)
    itr = './BlastOutput_iterations/Iteration/Iteration_hits/'
    for hit in root.findall(itr):
        features = {}
        for f in hit:
            if f.tag == 'Hit_num':
                features[f.tag] = int(f.text)
            elif f.tag == 'Hit_len':
                features[f.tag] = int(f.text)
            elif f.tag == 'Hit_hsps':
                pass
            else:
                features[f.tag] = f.text
            for Hit_hsps in f:
                for Hsp in Hit_hsps:
                    if Hsp.tag == 'Hsp_num':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_bit-score':
                        features[str(Hsp.tag)] = float(Hsp.text)
                    elif Hsp.tag == 'Hsp_score':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_evalue':
                        features[str(Hsp.tag)] = float(Hsp.text)
                    elif Hsp.tag == 'Hsp_query-from':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_query-to':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_hit-from':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_hit-to':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_query-frame':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_hit-frame':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_identity':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_positive':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_gaps':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    elif Hsp.tag == 'Hsp_align-len':
                        features[str(Hsp.tag)] = int(Hsp.text)
                    else:
                        features[str(Hsp.tag)] = Hsp.text
        # Calculate the percent identity
        features['Per Ident'] = float(features['Hsp_identity']) / features['Hsp_align-len'] * 100
        # Calculate the Query Cover
        if seq_len is not None:
            features['Query Cover'] = float(features['Hsp_query-to'] - features['Hsp_query-from'] + 1) / seq_len * 100
        out += [features]
    return out
    
   

def parse_args_ec_scrape():
    """
    Parses the arguments to the program.
    
    :return: A dictionary of arguements
    """
    # Expected arguments
    email  = None
    min_pct_idnt  = 97.0
    min_qry_cvr = 95.0
    max_blast_hits = 10
    max_uniprot_hits = 50
    # Dict to hold arguements
    args =  {
                '--src' : None,
                '--dest' : None,
                '--sheet': 0,
                '--keywords' : None,
                '--load_job' : False,
                '--email' : email, 
                '--min_pct_idnt' : min_pct_idnt,
                '--min_qry_cvr' : min_qry_cvr,
                '--max_blast_hits' : max_blast_hits,
                '--max_uniprot_hits' : max_uniprot_hits,
            }
    received = set(())
    required    = set(('--src', '--email', '--dest'))
    float_args  = set(('--min_pct_idnt', '--min_qry_cvr'))
    int_args    = set(('--max_blast_hits', '--max_uniprot_hits'))
    if len(sys.argv) % 2 != 1:
        print("Invalid command line arguements")
        print_usage_ec_scrape()
        exit()
    # Parse the arguements
    for i in range(1, len(sys.argv), +2):
        arg = sys.argv[i]
        val = sys.argv[i+1]
        if arg in args:
            received.add(arg)
            if arg in float_args:
                args[arg] = float(val)
            elif arg in int_args:
                args[arg] = int(val)
            elif arg == '--keywords':
                args[arg] = parse_keywords(arg)
            elif arg in args:
                args[arg] = val
    # Check that the required arguments where passed in
    for r in required:
        if not r in received:
            print(r + " is a required arguement\n")
            print_usage_ec_scrape()
            exit()
    # Make sure --src exists
    args['--src'] = str(args['--src'])
    args['--dest'] = str(args['--dest'])
    if not os.path.isfile(args['--src']):
        print(args['--src'] + " does not exist")
        print_usage_ec_scrape()()
    return args
    
    
def parse_keywords(keywords):
    """
    Parses a string of keywords and returns a list of dictionaries that represent the keywords. Each keyword is expected to be space separated. To search for phrases or groups of words, they must be surrounded by quotes. Each keyword is assumed to have the 'AND' condition. This means that only rows containing all keywords will be selected. The logical condition 'OR' is not yet supported. If you would like to exclude rows that contain certain keywords, this can be done by placing the 'NOT' keyword or phrase that you wish to exclude.
    
    For example, if you want to search for rows containing the keywords 'hypothetical' and 'protein', this can be done in the following way:
    
            hypothetical protein
            
    If you want to select rows not containing the phrase 'hypothetical protein', this can be done by the following:
    
            NOT 'hypothetical protein'
            
    If you want to select rows not containing the keyword hypothetical and select rows containing the keyword 'protein', this can be done by the following:
    
            NOT hypothetical protein
            
    :param keywords: The keywords to parse_args_ec_scrape
    :return: The keywords as a list of dictionaries
    """
    s = 0
    e = s
    comp_kw = []
    is_not = False
    phrase_single = False
    while e < len(keywords):
        # Capture phrase surrounded by single quotes
        if keywords[e] == "'":
            # Find the other single quote
            s = e
            stop = False
            while e < len(keywords) and not stop:
                if keywords[e] == "'" and keywords[s+1:e].strip() != '':
                    comp_kw += [{'Not'     : is_not, \
                                 'Keyword' : keywords[s+1:e].strip()}]
                    is_not = False
                    s = e + 1
                    stop = True
                e += 1
        # Capture phrase surrounded by double quotes
        elif keywords[e] == '"':
            # Find the other single quote
            s = e
            stop = False
            while e < len(keywords) and not stop:
                if keywords[e] == '"' and keywords[s+1:e].strip() != '':
                    comp_kw += [{'Not'     : is_not, \
                                 'Keyword' : keywords[s+1:e].strip()}]
                    s = e + 1
                    is_not = False
                    stop = True
                e += 1
        elif keywords[e] == ' ':
            if keywords[s:e].strip() == "":
                pass
            elif keywords[s:e].strip() == "NOT":
                is_not = True
            else:
                comp_kw += [{'Not'     : is_not, \
                             'Keyword' : keywords[s:e].strip()}]
                is_not = False
            s = e
        e += 1
    # Add the last words
    if keywords[s:e].strip() != "":
        comp_kw += [{'Not' : is_not, 'Keyword' : keywords[s:e].strip()}]
    return comp_kw
    
    
def print_usage_ec_scrape():
    """
    Prints the usage statement
    """
    print("Usage:")
    print("  py blast.py --src <the filename and path of source genome annotation excel file to annotate>")
    print("              --dest <the file name and path of the genome annotation to write to>")
    print("              --email <the user's email>")
    print("              --keywords <The keywords for the proteins to perform the BLAST on (keywords must be surronded by quotes)>")
    print("              --load_job <Boolean to indicate whether to load a previos job [True | False]>")
    print("              --min_pct_idnt <the min % identity to use for blast hit>")
    print("              --min_qry_cvr <the min query cover to use for blast hit>") 
    print("              --max_blast_hits <the max number of blast hits to use>") 
    print("              --max_uniprot_hits <the max number of UniProt hits to use>")
    print("              --sleep_time <amount of time to sleep before preforming the blast>")
    print("")
    print("  Required params:\n\t--src\n\t--dest\n\t--email")
    
    
def prcs_blast_rslts(blast_xml, seq_len, email, min_pct_idnt=97.0, \
                     min_qry_cvr=90.0, max_blast_hits=10, \
                     max_uniprot_hits=50):
    """
    Processes the blast results and scrapes online databases for ec numbers.
    
    :param blast_xml: String of the blast results
    :param seq_len: The length of the sequence that was blasted
    :param email: The user's email
    :param min_pct_idnt: The minimum percent identity to accept for 
                         blast results
    :param min_qry_cvr: The minimum query cover to accept for blast results
    :param max_blast_hits: The maximum number of blast hits to use
    :param max_uniprot_hits: The max number of uniprot hits to use
    :return: The results of the search
    """
    num_blast_hits_used = 0
    output = ""
    blast_data = parse_blast_xml(blast_xml, seq_len=seq_len)
    for hit in blast_data:
        if hit['Per Ident'] >= min_pct_idnt \
        and hit['Query Cover'] >= min_qry_cvr:
            acc = hit['Hit_accession']
            output += ec_scrape(acc, email, max_uniprot_hits) + " "
            num_blast_hits_used += 1
        if num_blast_hits_used >= max_blast_hits:
            break
    return output
    
    
def tag_ec(txt):
    """
    Replaces 'EC #.#.#.#' with (EC-Scraped EC #.#.#.#)'.
    
    :param txt: The string to replace 'EC #.#.#.#' with (EC-Scraped EC 
                #.#.#.#)'
    :return: The string in txt with 'EC #.#.#.#' with (EC-Scraped EC 
             #.#.#.#)'.
    """
    if not Annot_Reader.has_ec(txt):
        return txt
    # Find the position of the EC number
    s = 0
    new_start = 0
    while s < len(txt):
        temp_txt = txt.lower()
        break_now = False
        temp = s
        s = temp_txt.find("ec ", s + 1)
        if s == -1:
            s = temp
            s = temp_txt.find("ec: ", s)
            if s == -1:
                return txt
            else:
                ec_start = s
                ec_end = ec_start + 3
                s += 4
        else:
            ec_start = s
            ec_end = ec_start + 2
            s += 3
        # EC 
        if s >= len(txt):
            return txt
        if not txt[s].isdigit():
            break_now = True
            s -= 2
        else:
            e = s
            e = txt.find('.', s)
            if e == -1:
                return txt
        if not break_now:
            t = s
            while t < e:
                if not txt[t].isdigit():
                    t = e
                    break_now = True
                    break
                t += 1
            if not break_now:
                # If this far, then 'EC #.' at least
                t = e
                e = txt.find('.', e + 1)
                if e == -1:
                    return txt
                else:
                    # t on period, make sure following chars are digit or '-' 
                    # until index e is reached
                    while t < e:
                        if not txt[t].isdigit() and txt[t] == '-':
                            t = e
                            break_now = True
                            break
                        t += 1
                    if not break_now:
                        # EC #.#.
                        e = txt.find('.', e + 1)
                        if e == -1:
                            return txt
                        t += 1
                        while t < e:
                            if not txt[t].isdigit() and txt[t] != '-':
                                t = e
                                break_now = True
                                break
                            t += 1
                        if not break_now:
                            # EC #.#.#.
                            e += 1
                            if not txt[e].isdigit() and txt[e] != '-':
                                t = e
                                break_now = True
                                break
                            while e < len(txt): 
                                if not txt[e].isdigit() and txt[e] != '-':   
                                    break
                                e += 1
                            new_start = e
                            txt_to_add = ')'
                            txt = txt[:e] + txt_to_add + txt[e:]
                            text_to_add = '(EC-Scraped EC'
                            num_chars_added = len(text_to_add) \
                                            - len(txt[ec_start:ec_end])
                            txt = txt[:ec_start] + text_to_add + txt[ec_end:]
                            new_start += num_chars_added
                            s = new_start
        s += 1
        

    return txt