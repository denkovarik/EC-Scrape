import xml.etree.cElementTree as et
from classes.NCBI import NCBI
from classes.Uniprot import *
from classes.Annot_Reader import *


def ec_scrape(acc, max_uniprot_hits, email):
    """
    Scrapes the web for the ec number for the protein with the given 
    accession number.
    
    :param acc: The accession number to scrape the web for.
    :param max_uniprot_hits: The max number of hits on Uniprot to use.
    :param email: The users email
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
    
    
def tag_ec(txt):
    """
    Replaces 'EC #.#.#.#' with (EC-Scraped EC #.#.#.#)'.
    
    :param txt: 
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