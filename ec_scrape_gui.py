# File: ec_scrape_gui.py
#
# Description:
# This program is the GUI version of ec_scrape.py.
# Performs a blast on sequences or parses downloaded BLAST result files. 
# for proteins in a genome annotation. Afterwards it then searches 
# online databases like NCBI protein and UniProt for their EC Number. This
# is the main program file which is the start of the program.
#
# Author: Dennis Kovarik

import PySimpleGUI as sg
import os, io, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
import shutil
import xlwings as xw
import pandas as pd
from classes.Annot_Reader import *
from utils import *


def add_optional_cmd_args(values, tag):
    """
    Addes a set of optional arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :return: A list of the added optional args
    """
    cmd_args = []
    if values[tag] != "":
        cmd_args += [tag]
        cmd_args += [values[tag]]
    return cmd_args


def add_required_cmd_args(values, tag, name):
    """
    Addes a set of required arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :param name: Item named used in popup window.
    :return: A list of the added required args
    """
    if values[tag] == "":
        msg = name + " is Required"
        layout = [[sg.Text(msg)]]
        window = sg.Window(msg, layout, modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        # Exit  if error occured
        exit()
    cmd_args = [tag]
    cmd_args += [values[tag]]
    return cmd_args


def add_required_filepath_cmd_args(values, tag, name):
    """
    Addes a set of filepath required arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :param name: Item named used in popup window.
    :return: A list of the added required args
    """
    if values[tag] == "":
        msg = name + " is Required"
        layout = [[sg.Text(msg)]]
        window = sg.Window(msg, layout, modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        # Exit  if error occured
        exit()
    cmd_args = [tag]
    cmd_args += [values[tag].replace("/","\\")]
    return cmd_args
    
    
def add_required_folderpath_cmd_args(values, tag, name):
    """
    Addes a set of dirpath required arguements to a list of command line 
    arguements for the program.
    
    :param values: The values entered in the GUI fileds
    :param cmd_args: A list of arguements for the program.
    :param tag: The tag for the cmd args
    :param name: Item named used in popup window.
    :return: A list of the added required args
    """
    if values[tag] == "":
        msg = name + " is Required"
        layout = [[sg.Text(msg)]]
        window = sg.Window(msg, layout, modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        # Exit  if error occured
        exit()
    cmd_args = [tag]
    path = values[tag] + '/'
    cmd_args += [path.replace("/","\\")]
    return cmd_args


def build_cmd_args_dwnl_BLAST(values, event):
    cmd_args = ['run_ec_scrape.py']
    # Source file
    tag = '--src'
    name = 'Source RAST Genome Annotation '
    cmd_args += add_required_filepath_cmd_args(values, tag, name)
    # Destination file
    if values['--dest'] == '':
        layout = [[sg.Text("Destination file is required", font=32)]]
        window = sg.Window("Destination file is required", layout, \
                 modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        exit()
    if values['--dest'].split('.')[-1] != 'xlsx':
        layout = [[sg.Text("Destination file must be a .xlsx file", font=32)]]
        window = sg.Window("Destination file must be a .xlsx file", layout, \
                 modal=True)
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
        exit()
    dest = values['--dest']
    cmd_args += ['--dest']
    cmd_args += [dest.replace("/","\\")]
    # Email
    tag = '--email'
    name = "Email "
    cmd_args += add_required_cmd_args(values, tag, name)
    # Optional keywords argument
    tag = '--keywords'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Min Query Cover Arg
    tag = '--min_qry_cvr'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Min Per. Ident
    tag = '--min_pct_idnt'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Max Blast Hits to Use Arg
    tag = '--max_blast_hits'
    cmd_args += add_optional_cmd_args(values, tag)
    # Optional Max Uniprot Hits to Use Arg
    tag = '--max_uniprot_hits'
    cmd_args += add_optional_cmd_args(values, tag)
    cmd_args += ['--from_downloaded_blast']
    cmd_args += ['True']
    # BLAST results path
    tag = '--BLAST_rslts_path'
    name = 'Path to BLAST results file '
    cmd_args += add_required_folderpath_cmd_args(values, tag, name)
    return cmd_args
    
    
def build_ec_scrape_via_dwnl_blast_rslt_layout():
    """
    Builds the layout of the window for ec_scrape_via_dwnl_blast_rslt().
    
    :return: The layout for the ec_scrape_via_dwnl_blast_rslt() window.
    """
    delim2 = '-----------------------------------------------------------------'
    delim2 += '----------------------------------------------------------------'
    delim2 += '-----------------------------'
    delim = '================================================================='
    delim += '=========================='
    layout =    [
                    [sg.Text("EC-Scrape via Downloaded BLAST Results")],
                    [sg.Text(delim)],
                    [sg.Text("Required Parameters")],
                    [sg.Text(delim2)],
                    [sg.Text('Select RAST Genome Annotation Source'), \
                             sg.InputText(key='--src'), sg.FileBrowse()],
                    [sg.Text('Filename for RAST Genome Annotation to Write')] \
                             + [sg.Input(key='--dest')],
                    [sg.Text('Select Directory Holding Downloaded BLAST Results'), \
                              sg.InputText(key='--BLAST_rslts_path'), sg.FolderBrowse()],
                    [sg.Text('Enter Email')] + [sg.Input(key='--email')],
                    [sg.Text("\nOptional Parameters")],
                    [sg.Text(delim2)],
                    [sg.Text('Keywords')] + [sg.Input(key='--keywords')],
                    [sg.Text('Min Query Cover')] + [sg.Input(key='--min_qry_cvr')],
                    [sg.Text('Min Per. Ident')] + [sg.Input(key='--min_pct_idnt')],
                    [sg.Text('Max BLAST Hits')] + [sg.Input(key='--max_blast_hits')],
                    [sg.Text('Max Uniprot Hits')] + [sg.Input(key='--max_uniprot_hits')],
                    [sg.Button("Go", key="go_dwnl_ec")],                    
                ]
    return layout


def ec_scrape_via_dwnl_blast_rslt():
    delim3 = '================================================================'
    layout = build_ec_scrape_via_dwnl_blast_rslt_layout()
    window = sg.Window("EC-Scrape via Downloaded BLAST Results", layout, resizable=True, \
             finalize=True, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "go_dwnl_ec":
            window.close()
            # Compile arguements for program
            cmd_args = build_cmd_args_dwnl_BLAST(values, event)
            args = parse_args_ec_scrape(cmd_args)
            # Annot_Reader class to read and write to genome annotation
            reader = Annot_Reader(args)
            # Check for necessary command line arguments
            check_dl_blast_args(args)
            # Build a dictionary mapping proteins by contig location
            loc2row = {}
            for ind in reader.df.index:
                loc = reader.df['location'][ind]
                loc2row[loc] = ind
            # Parse results in --BLAST_rslts_path
            num_rslts = len(os.listdir(args['--BLAST_rslts_path']))
            bar = IncrementalBar('| Processing Downloaded BLAST Results...', \
                    max = num_rslts)
            i = 0
            ec_added = 0
            for file in os.listdir(args['--BLAST_rslts_path']):
                if dl_blast_prcs_hit(file, reader, args, loc2row):
                    ec_added += 1
                sg.OneLineProgressMeter('Processing BLAST Results...', i + 1, \
                        num_rslts, 'Processing Downloaded BLAST Results...')
                bar.next()
                i += 1
            layout =    [
                            [sg.Text("EC-Scrape from Downloaded BLAST Results has Completed")],
                            [sg.Text("EC Numbers were Found for an Additional " \
                                    + str(ec_added) + " Proteins")],
                            [sg.Button("Quit", \
                                key="quit")],
                        ]
            window = sg.Window("Complete", layout, modal=True)
            while True:
                event, values = window.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                elif event == "quit":
                    window.close()


def ec_scrape_via_online_blast():
    layout =    [
                    [sg.Text("EC-Scrape via Online BLAST", font=32)],
                    [sg.Button("EC-Scrape via Online BLAST", \
                                key="online blast ec scrape")],
                    [sg.Button("EC-Scrape via Online BLAST", \
                                key="online blast ec scrape")],
                ]
    window = sg.Window("EC-Scrape via Online BLAST", layout, \
             resizable=True, finalize=True, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
    window.close()
    
    
def main():
    # Define the layout of the main window
    layout =    [
                    [sg.Text("EC-Scrape", \
                             font=32)],
                    [sg.Button("EC-Scrape via Online BLAST", \
                               key="online blast ec scrape")],
                    [sg.Button("EC-Scrape via Downloaded BLAST Results", \
                               key="downloaded blast ec scrape")]
                ]
    window = sg.Window('EC-Scrape', layout, resizable=True, finalize=True)
    # Loop for the main window
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == 'Configure':
            if window.TKroot.state() == 'zoomed':
                status.update(value='Window zoomed and maximized !')
            else:
                status.update(value='Window normal')
        if event == "online blast ec scrape":
            window.close()
            ec_scrape_via_online_blast()
        elif event == "downloaded blast ec scrape":
            window.close()
            ec_scrape_via_dwnl_blast_rslt()
        
    window.close()
if __name__ == "__main__":
    main()