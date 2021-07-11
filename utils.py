import xml.etree.cElementTree as et
from classes.NCBI import NCBI
from classes.Uniprot import *
from classes.Annot_Reader import *
from time import sleep
from progress.bar import IncrementalBar
import random
import sys, os, time
from subprocess import Popen, list2cmdline


def cpu_count():
    ''' Returns the number of CPUs in the system
    '''
    num = 1
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            pass
    elif sys.platform == 'darwin':
        try:
            num = int(os.popen('sysctl -n hw.ncpu').read())
        except ValueError:
            pass
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            pass

    return num


def exec_commands(cmds, max_task):
    ''' Exec commands in parallel in multiple process 
    (as much as we have CPU)
    '''
    if not cmds: return # empty list

    def done(p):
        return p.poll() is not None
    def success(p):
        return p.returncode == 0
    def fail():
        sys.exit(1)

    #max_task = cpu_count()
    processes = []
    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop()
            os.system(list2cmdline(task))
            processes.append(Popen(task))

        for p in processes:
            if done(p):
                if success(p):
                    processes.remove(p)
                else:
                    fail()

        if not processes and not cmds:
            break
        else:
            time.sleep(5)


def build_cmd(seq, out_file, query_id, args):
    """
    Builds a command to run blast.py on the command line.
    
    :param seq: A fasta sequence to BLAST
    :param out_file: The name of the file to store the results in
    :param query_id: The id of the query
    :param args: A dictionary of arguments need for the BLAST and EC search 
                 from online databases.
    :return: The command to run blast.py on the command line.
    """
    cmd = ["py", "blast.py", \
            "--fasta_sequence", seq, \
            "--email", args["--email"], \
            "--out_file", out_file, \
            "--id", str(query_id), \
            "--min_pct_idnt", str(args["--min_pct_idnt"]), \
            "--min_qry_cvr", str(args["--min_qry_cvr"]), \
            "--max_blast_hits", str(args["--max_blast_hits"]), \
            "--max_uniprot_hits", str(args["--max_uniprot_hits"])]
    return cmd
       
    
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
                '--visible' : False,
                '--load_job' : None,
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

                args[arg] = val
            elif arg == '--visible':
                visible = False
                if args['--visible'] == 'True':
                    visible = True
                args['--visible'] = visible
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