import xml.etree.cElementTree as et
from classes.NCBI import NCBI
from classes.Uniprot import *
from classes.Annot_Reader import *
from classes.BLAST_Rslts_Itr import BLAST_Rslts_Itr
from time import sleep
from progress.bar import IncrementalBar
import random
import sys, os, time
from subprocess import Popen, list2cmdline


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
    
    
def check_dl_blast_args(args):
    """
    Checks for the necessary command line arguements for using downloaded blast 
    results for searching for the EC numbers for proteins.
    
    :param args: A python dictionary of command line arguments.
    """
    # Make sure flag is set to use downloaded blast results
    if not '--from_downloaded_blast' in args.keys():
        raise Exception("Flag not set to use downloaded BLAST results")
    elif args['--from_downloaded_blast'] is None:
        raise Exception("Flag '--from_downloaded_blast' set to None")
    elif not args['--from_downloaded_blast']:
        raise Exception("Flag '--from_downloaded_blast' set to False")
    # Check the path to dir containing downloaded blast results
    if not '--BLAST_rslts_path' in args.keys():
        raise Exception("'--BLAST_rslts_path' Flag not set")
    elif args['--BLAST_rslts_path'] is None:
        raise Exception("'--BLAST_rslts_path' Flag set to None")
    elif type(args['--BLAST_rslts_path']) != type("str"):
        raise Exception("'--BLAST_rslts_path' is invalid type")
    elif not os.path.isdir(args['--BLAST_rslts_path']):
        msg = "'--BLAST_rslts_path' " + args['--BLAST_rslts_path'] \
            + " does not exist."
        raise Exception(msg)
    
    
def dl_blast_ec_scrape(reader, args):
    """
    Parses downloaded blast results for protein accession numbers, then uses 
    those accession numbers to search online databases for EC numbers.
    
    :param reader: An instance of the Annot_Reader class to read and write 
                   to an excel file of a genome annotation.
    :param args: A python dictionary of command line arguements
    """
    # Check for necessary command line arguments
    check_dl_blast_args(args)
    # Build a dictionary mapping proteins by contig location
    loc2row = {}
    for ind in reader.df.index:
        loc = reader.df['location'][ind]
        loc2row[loc] = ind
    # Parse results in --BLAST_rslts_path
    num_rslts = len(os.listdir(args['--BLAST_rslts_path']))
    bar = IncrementalBar('| Processing Downloaded BLAST Results...', max = num_rslts)
    for file in os.listdir(args['--BLAST_rslts_path']):
        if os.path.isfile(file):
            filepath = args['--BLAST_rslts_path'] + file
            loc = file.split(".")[0]
            entry = reader.read(loc2row[loc], 'function')
            if not Annot_Reader.has_ec(entry):
                output = prcs_blast_rslts_html(filepath, reader, args)
                if output.strip() != "":
                    output = entry + output
                    # Write the results
                    reader.write(output, loc2row[loc], 'function')
        bar.next()
           
    
def ec_scrape(features, email, max_uniprot_hits):
    """
    Scrapes the web for the ec number for the protein with the given 
    accession number.
    
    :param features: Dictionary of extracted features from the Blast results.
    :param email: The users email
    :param max_uniprot_hits: The max number of hits on Uniprot to use.
    :return: The results as a string
    """
    # Query NCBI database for EC number through the entrez database
    ncbi = NCBI()
    rslt = ncbi.protein.search(features['Accession'], email)
    if rslt is None:
        return ""
    uniprot = Uniprot()
    rslt_found = '{EC-Scraped '
    # If EC number not found from above, the query Uniprot Database for it
    if not 'EC Number' in rslt.keys():
        srch = [("Protein name",rslt['Protein name']), \
                ("Organism",rslt['Organism'])]
        uniprot.search(srch)
        itr = iter(uniprot)
        for i in itr:
            if Annot_Reader.has_ec(i['protein names']):
                proteins = tag_ec(i['protein names'])
                rslt_found += '(' + proteins + ' [' + i['organism'] + '] ' + 'UniProtKB: ' + i['id'] + ')'
    else:
        rslt_found += "(" + rslt['Protein name'] + " [" + rslt['Organism'] + '] ' + "(NCBI Protein Accession: " + features['Accession'] + ") " + '(EC-Scraped EC ' + rslt['EC Number'] + '))'
    # If no results found, return empty string
    if rslt_found.strip() == '{EC-Scraped':
        rslt_found = ''
    else:
        rslt_found += ' Program: ' + features['Program'] + ', ' 
        rslt_found += 'Query Cover: ' + str(features['Query Cover']) + ', ' 
        rslt_found += 'E value: ' + str(features['E value']) + ', ' 
        rslt_found += 'Per. Ident: ' + str(features['Per. Ident'])
        rslt_found += '} '
    return rslt_found


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
            sleep(2)

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
    
    
def online_blast_ec_scrape(reader, args):
    """
    Uses Biopython's api to blast sequences. It will then use these results 
    to scrape NCBI protein database and Uniprot for the ec numbers of 
    proteins.
        
    :param reader: An instance of the Annot_Reader class for reading the 
                   excel sheet genome annotation.
    :param args: A python dictionary of command line arguements.
    """
    rows_to_process = set((reader.rows))
    processing = set(())
    # Create temp dir to hold results returned from processes
    if not os.path.isdir('temp\\'):
        os.mkdir('temp\\')
        
    # Start Blasting
    itr = iter(rows_to_process)
    num_rows = len(rows_to_process)
    bar = IncrementalBar('| BLASTing Sequences...', max = num_rows)
    num_processing = 0 
    max_num_processes = args['--num_threads']
    tempdir = 'temp\\'
    count = 0

    # Make sure there are no files left in temp dir
    for file in os.listdir(tempdir):
        path = tempdir + file
        os.remove(path)

    if args['--from_downloaded_blast']:
        exit()

    while len(reader.rows) > 0:
        cmd = []
        rows_added = []
        while count < num_rows and len(processing) < max_num_processes:
            row = next(itr)
            # Read the Sequences
            seq = reader.read(row, 'nucleotide_sequence')
            out_file = tempdir + str(row) + ".txt"
            cmd += [build_cmd(seq, out_file, row, args)]
            processing.add(row)
            count += 1
        if len(cmd) > 0:
            # Blast the sequence
            num_processing += len(processing)
            exec_commands(cmd, max_num_processes)       
        while len(os.listdir(tempdir)) > 0:
            filename = os.listdir(tempdir)[0]
            filepath = tempdir + filename
            f = open(filepath, 'r')
            content = f.read()
            f.close()
            os.remove(filepath)
            completed_row = filename.split(".")[0]
            completed_row = completed_row.strip()
            completed_row = int(completed_row)
            val = reader.read(completed_row, 'function') + " " + content
            reader.write(val, completed_row, 'function')
            reader.rows.remove(completed_row)
            processing.remove(completed_row)
            bar.next()
            num_processing -= 1
        # Autosave
        reader.save_job(reader.autosave_filename)
    

def parse_blast_xml(xml, seq_len = None):
    """
    Parses the xml from a blast and returns the results in a list of 
    dictionaries.
    
    :param xml: The xml output as a string
    :return: The blast data as a list of dictionaries
    """
    blast_program = ""
    out = []
    # Parse xml from a string
    root = et.fromstring(xml)
    for node in root:
        if node.tag == 'BlastOutput_program':
            blast_program = node.text
        elif node.tag == 'BlastOutput_query-len':
            seq_len = int(node.text)
    itr = './BlastOutput_iterations/Iteration/Iteration_hits/'
    for hit in root.findall(itr):
        features =  {
                        "Program"   : blast_program
                    }
        for f in hit:
            if f.tag == 'Hit_num':
                features[f.tag] = int(f.text)
            elif f.tag == 'Hit_len':
                features[f.tag] = int(f.text)
            elif f.tag == 'Hit_hsps':
                pass
            elif f.tag == 'Hit_accession':
                features['Accession'] = f.text
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
                        features['E value'] = float(Hsp.text)
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
        features['Per. Ident'] = float(features['Hsp_identity']) / features['Hsp_align-len'] * 100
        # Calculate the Query Cover
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
    max_blast_hits = 5
    max_uniprot_hits = 50
    # Dict to hold arguements
    args =  {
                '--src'                     : None,
                '--dest'                    : None,
                '--sheet'                   : 0,
                '--keywords'                : None,
                '--program'                 : 'blastx',
                '--visible'                 : False,
                '--load_job'                : None,
                '--email'                   : email, 
                '--min_pct_idnt'            : min_pct_idnt,
                '--min_qry_cvr'             : min_qry_cvr,
                '--max_blast_hits'          : max_blast_hits,
                '--max_uniprot_hits'        : max_uniprot_hits,
                '--num_threads'             : 1,
                '--from_downloaded_blast'   : False,
                '--BLAST_rslts_path'        : None
            }
    received = set(())
    required    = set(('--src', '--email', '--dest'))
    float_args  = set(('--min_pct_idnt', '--min_qry_cvr'))
    int_args    = set(('--max_blast_hits', '--max_uniprot_hits', \
                       '--num_threads'))

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
            elif arg == '--from_downloaded_blast':
                down = False
                if val == 'True':
                    down = True
                args['--from_downloaded_blast'] = down
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
    
    
def prcs_blast_rslts(filepath, reader, args):
    """
    Processes the blast results from file and scrapes online databases 
    for ec numbers.
    
    :param filepath: Filepath to the blast rslts
    :param reader: An instance of the Annot_Reader class
    :param args: A python dictionary of command line arguments
    :return: The results of the search
    """
    # Determine if file is .xml or .htm or .html file.
    the_filepath = filepath.split('.')
    if the_filepath[-1] == 'xml':
        return prcs_blast_rslts_xml(filepath, reader, args)
    elif the_filepath[-1] == 'htm':
        return prcs_blast_rslts_html(filepath, reader, args)
    elif the_filepath[-1] == 'html':
        return prcs_blast_rslts_html(filepath, reader, args)
    else:
        return ''
    
    return output.strip() 
 
    
def prcs_blast_rslts_html(filepath, reader, args):
    """
    Processes the blast results from a html file and scrapes online databases 
    for ec numbers.
    
    :param filepath: Filepath to the blast rslts .html file.
    :param reader: An instance of the Annot_Reader class
    :param args: A python dictionary of command line arguments
    :return: The results of the search
    """
    if not os.path.isfile(filepath):
        return ""
    f = open(filepath)
    content = f.read()
    f.close()
    c = 0
    output = ""
    for hit in BLAST_Rslts_Itr(content):  
        if hit['Per. Ident'] >= args['--min_pct_idnt'] \
        and hit['Query Cover'] >= args['--min_qry_cvr']:
            output += ec_scrape(hit, args['--email'], args['--max_uniprot_hits']) + " "
            c += 1
            if c >= args['--max_blast_hits']:
                break
    return output.strip()
        
    
def prcs_blast_rslts_xml(filepath, reader, args):
    """
    Processes the blast results stored in an xml file and then scrapes online 
    databases for ec numbers.
    
    :param filepath: The filepath of the blast results xml file.
    :param reader: An instance of the Annot_Reader class
    :param args: A python dictionary of command line arguments
    :return: The results of the search
    """
    # Read the file
    f = open(filepath, 'r')
    blast_xml = f.read()
    f.close()
    num_blast_hits_used = 0
    output = ""
    blast_data = parse_blast_xml(blast_xml)
    for hit in blast_data:
        if hit['Per. Ident'] >= args['--min_pct_idnt'] \
        and hit['Query Cover'] >= args['--min_qry_cvr']:
            acc = hit['Accession']
            output += ec_scrape(hit, args['--email'], args['--max_uniprot_hits']) + " "
            num_blast_hits_used += 1
        if num_blast_hits_used >= args['--max_blast_hits']:
            break
    return output.strip()
    
    
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