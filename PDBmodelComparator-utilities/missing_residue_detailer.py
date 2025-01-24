#!/usr/bin/env python
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# NOT THe ACTUALmissing_residue_detailer.py by Wayne Decatur THIS IS JUST A STARTING POINT
#THAT WILL MAKE UP MATCH TO FIRST GLANCE IN JMOL for 4dqo SO TEST WITH PYTEST CAN 
#BE RUN TO SEE IF PYTEST WORKING 'IN THEORY' BEFORE THIS SCRIPT ACTUALLY DOES WHAT IT IS MEANT TO DO
# ver 0.1
#
#*******************************************************************************
# PURPOSE: Python code that gives the details that FirstGlance in Jmol 
# (https://www.bioinformatics.org/firstglance/fgij/) detailing missing residues. 
# The information provided is the same when you click on the 'Missing Residues' 
# link on the 'Molecule Information Tab' page that comes up when you start 
# FirstGlance in Jmol. Makes for a nice text table summary of the missing 
# residue information
#
# Details: The javascript functions concerning missing residues in `moltab.js`
# (https://bioinformatics.org/firstglance/fgij/moltab.js) were converted to 
# equivalent Python to give as close as possible same result as the information 
# FirstGlance in Jmol gives you. Essentially `makeMissingReport()` and 
# `getMissingCount2()` were converted to Python.
# A few of the test cases noted in `moltab.js` were tested during development to
# ensure the results were the same; however, this testing was not exhaustive.
# The particular version of `moltab.js` used, believed to be from FirstGlance in
# Jmol version 4.31 according to the information on 
# https://www.bioinformatics.org/firstglance/fgij/, from which this Python 
# implementation was adapted is found at the bottom of this file.
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# - Pandas
#
#
# VERSION HISTORY:
# v.0.1. basic working version
#
#
# To do yet:
# - ?
#
#
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python missing_residue_detailer.py [entry_identifier]
#-----------------------------------
# Issue `missing_residue_detailer.py -h` for details.
#
# To use the main function in a Jupyter Notebook:
#------------------------------------------------
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the dataframe (or dataframe file) and columns:
# from missing_residue_detailer import generate_missing_report
# report_html_text = generate_missing_report(<PDB_id_code>)
#
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
from missing_residue_detailer import generate_missing_report
report_html_text = generate_missing_report("6w6v")
'''
#
#
#*******************************************************************************
#


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
suffix_4_results = "_missing_residue_details.html" #this will be appended to PDB 
# identifier to make output name

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************






















#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
from urllib.request import urlopen
import requests
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
import pandas as pd
import numpy as np


###--------------INDEXES FOR FIXED WIDTH SECTION 'REMARK 465'----------------###
# Index settings based on what Eric has in moltab.js for the two types of 
# REMARK 465 sections he had seen, specifically:
'''
// 4asw NMR
//REMARK 465 SSSEQ=SEQUENCE NUMBER; I=INSERTION CODE.)                            
//REMARK 465   MODELS 1-  9                                                       
//REMARK 465     RES C SSSEQI                                                     
//REMARK 465     MET A     1                                                      

// 1o9a NMR; 1d66 XRAY
//REMARK 465 IDENTIFIER; SSSEQ=SEQUENCE NUMBER; I=INSERTION CODE.)                
//REMARK 465                                                                      
//REMARK 465   M RES C SSSEQI                                                     
//REMARK 465     XXX X     1    
'''
# Note that GitHub Copilot called that 'modern' and 'legacy':
'''
Modern format example:
REMARK 465 MISSING RESIDUES
REMARK 465 THE FOLLOWING RESIDUES WERE NOT LOCATED IN THE EXPERIMENT
REMARK 465   M RES C SSSEQI
REMARK 465     MET A     1


Legacy format example:
REMARK 465 SSSEQ=SEQUENCE NUMBER; I=INSERTION CODE
REMARK 465     RES C SSSEQI
REMARK 465     GLY A    24
'''
###---------END OF INDEXES FOR FIXED WIDTH SECTION 'REMARK 465'--------------###
###---------END OF INDEXES FOR FIXED WIDTH SECTION 'REMARK 465'--------------###




###---------------------------HELPER FUNCTIONS-------------------------------###

def fetch_pdbheader(pdb_id):
    '''
    Take a PDB accession code and return the PDB file header

    lifted/adapted directly from https://github.com/fomightez/sequencework/blob/master/LookUpTaxon/LookUpTaxonFA.py , based on http://boscoh.com/protein/fetching-pdb-files-remotely-in-pure-python-code and http://www.pdb.org/pdb/static.do?p=download/http/index.html & more universal for outside of MyBinder than `curl`!
    THIS CODE IS GOOD. Works on Anaconda Cloud but today MyBinder connection seemed initially bad because says it times out. an earlier version of `fetch_pdbheader_using_requests` using same endpoint as this draft worked after waiting a long time. And then this worked in same MyBinder session, so who knows! Seems fine!
    SEE `fetch_pdbheader_using_requests()` below as it will be more adaptable to WASM because uses the RCSB's CORS-enabledDirect file access server instead.
    '''
    url = f'http://www.rcsb.org/pdb/files/{pdb_id}.pdb?headerOnly=YES'
    with urlopen(url) as response:
        return response.read()
 
def fetch_pdbheader_using_requests(pdb_id):
    """
    Take a PDB accession code and return the PDB file header using RCSB's Direct file access server with CORS headers
    See https://www.wwpdb.org/ftp/pdb-ftp-sites

    Version of `fetch_pdbheader()` from above but with requests and because
    happens to have CORS headers enabled is more universal & works for outside of 
    MyBinder-served sessions, even WASM! Both ipykernel & pyodide-compatible. 
    """
    url = f'https://files.rcsb.org/header/{pdb_id.upper()}.pdb'
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    return response.text



def generate_output_file_name(pdb_id,  suffix_4_results):
    '''
    Takes a PDB identifier and file name suffix arguments and returns string for
    the name of the output file.  

    suffix_4_results = "_missing_residue_details.txt" 


    Specific example
    =================
    Calling function with
        ("1d66")
    returns
        "1d66_missing_residue_details.txt"
    '''
    return pdb_id + suffix_4_results

def write_string_to_file(s, fn):
    '''
    Takes a string, `s`, and a name for a file & writes the string to the file.
    '''
    with open(fn, 'w') as output_file:
        output_file.write(s)

###--------------------------END OF HELPER FUNCTIONS-------------------------###
###--------------------------END OF HELPER FUNCTIONS-------------------------###


## FOR DEVELOPMENT TO GIVE SOMETHING THAT WILL WORK FOR 4dqo. DELETE THIS WHEN CLOSER TO REALLY WORKING
fgij_4dqo_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>246</b> residues of Protein including 2 <a href="javascript: showLigNSRHelp()">non-standard residue(s)</a> (no <a href="http://proteopedia.org/wiki/index.php/Selenomethionine" target="_blank">selenomethonine</a> [MSE]):</center></td></tr><tr><td> H</td><td><center>6</center></td><td><font color="red">1-</font>, 0+</td><td>217-222</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>216</b> residues of Protein:</center></td></tr><tr><td> L</td><td><center>2</center></td><td>0</td><td>211-212</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>124</b> residues of Protein:</center></td></tr><tr><td> C</td><td><center>36</center></td><td><font color="red">7-</font>, 0+</td><td>118-118, 143-152, 178-178P, 239-246</td></tr></tbody></table>'''


#*******************************************************************************
###------------------------'main' function of script--------------------------##

def generate_missing_report(PDBid, return_report_string = True):
    '''
    Main function of script. 
    PDB id code to details of missing residues.

    Takes the following:
    - PDB id code of a macromolecular structure deposited at the Protein Data 
    Bank (could be modified eith editing to use a file if it has a complete 
    header)

    - a boolean of whether to return a string with the HTML content in it

    Optional: 
    Makes a string `missing_report` containing the HTML content of the report
    that can be used in-memory if you import this script.
    '''
    missing_report = ""

    ### THIS SPECIAL CONDITIONAL only if concern if you are developer, Wayne.
    # Doesn't really makedetails, just copies previously sourced HTML for `4dqo`
    # from FirstGlance in Jmol.
    STILL_IN_EARLY_DEVELOPMENT = True
    if STILL_IN_EARLY_DEVELOPMENT:
        file_needed = generate_output_file_name(PDBid, suffix_4_results)
        if PDBid == "4dqo":
            write_string_to_file(fgij_4dqo_main_table_html, file_needed)
            missing_report = fgij_4dqo_main_table_html,
        else:
            stub_placeholder_string = "script to generate this in the works!"
            write_string_to_file(stub_placeholder_string, file_needed)
            missing_report = stub_placeholder_string
        sys.stderr.write("Comment out the `return` on line 260 under control of the \
            `if STILL_IN_EARLY_DEVELOPMENT:` if you want to test fetching the \
            header from PDB, which is currently skipped to make the tests 'run' even if not accurately testing at this stage.")
        return #COMMENT THIS RETURN OUT IF YOU PREFER TO STOP HERE INSTEAD OF CONTINUING ON AND TEST GETTING THE PDB HEADER BECAUSE THIS DRAFT NOT BROUGHT UP TO CURRENT AND GLITCH ON LARGE PDB FILE HEADERS.
    ### END OF SPECIAL DEVELOPMENT CONDITIONAL. 

    if PDBid == "0rid": # this one doesn't exist and is meant to test file 
        # handling which is not built in to this older draft yet
        PDBheaderhandler = fetch_pdbheader_using_requests(PDBid)
        print (PDBheaderhandler[0:1500])

    
    #PDBPageList.append(PDBhandler) #DECIDED I DIDN'T NEED #couldn't pass each to a list entry with Full entries from NCBI because read in in batches so would add more than one anyway

    '''

    # Bring in the necessary data and make collected results into dataframe:
    #---------------------------------------------------------------------------
    # df = pd.read_csv(results, sep='\t', header=None, names=col_names)
    # AT FIRST I HAD ABOVE, because I mistakenly though documentation said
    # `pd.read_csv()` work with a string so I thought I wouldn't have to resort
    # to acrobatics I used in
    # `patmatch_results_to_df.py` to handle correctly whether provided a file
    # or string; however, seems that I do need to handle all that.
    try:
        df = pd.read_csv(results, sep='\t', header=None, names=col_names)
    except (TypeError,OSError,IOError) as e:
        # The `except` above the pass has three errors it excepts because the
        # first was a TypeError seen when I tried to pass a file-like string to
        # `with open` because it seems `with open` method is incompatible with
        # use of StringIO, I think, which I usually use to try to pass things 
        # associated with file methods string. (I qualifed it with 'I think' b/c 
        # questions on stackoverlflow seemed to agree but I didn't try every 
        # possibility because realized this would probably be a better way to 
        # handle anyway.) That TypeError except got me to the next issue which
        # was trying the string as a file name and getting it was too long, and 
        # so I added the `OSError` catch and that seemed to make passing a 
        # string into the function work. `IOError` seemed to handle that same
        # thing in Python 2.7.
        # Note "FileNotFoundError is a subclass of OSError"(https://stackoverflow.com/a/28633573/8508004)
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO
        df = pd.read_csv(StringIO(results), sep='\t', header=None, names=col_names)
        # I need StringIO so string handled as file document. 
        

    # feedback
    sys.stderr.write("Provided results read and converted to a dataframe...")


    # Reporting and Saving
    #---------------------------------------------------------------------------
    #print(df)#originally for debugging during development,added..
    # Document the full set of data collected in the terminal or 
    # Jupyter notebook display in some manner. 
    # Using `df.to_string()` because more universal than `print(df)` 
    # or Jupyter's `display(df)`.
    #sys.stderr.write("\nFor documenting purposes, the following lists the "
    #    "parsed data:\n")
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #    display(df)
    #sys.stderr.write(df.to_string())

    # Handle pickling the dataframe
    if pickle_df == False:
        sys.stderr.write("\n\nA dataframe of the data "
        "was not stored for use\nelsewhere "
        "because `no_pickling` was specified.")
    else:
        df.to_pickle(df_save_as_name )
        # Let user know
        sys.stderr.write("\n\nA dataframe of the data "
        "has been saved as a file\nin a manner where other "
        "Python programs can access it (pickled form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}'".format(df_save_as_name ))
    '''

    
    # Return report HTML content as a string (optional)
    #---------------------------------------------------------------------------
    if return_report_string:
        sys.stderr.write("String containing HTML text content returned.")
        return missing_report

###--------------------------END OF MAIN FUNCTION----------------------------###
###--------------------------END OF MAIN FUNCTION----------------------------###



    
#*******************************************************************************
###------------------------'main' section of script---------------------------##
def main(PDBid):
    """ Main entry point of the script """
    # placing actual main action in a 'helper'script so can call that easily 
    # with a distinguishing name in Jupyter notebooks, where `main()` may get
    # assigned multiple times depending how many scripts imported/pasted in.
    kwargs = {}
    kwargs['return_report_string'] = False #probably don't want string returned 
    # if calling script from command line
    generate_missing_report(PDBid,**kwargs)
    # using https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/#calling-a-function
    # to build keyword arguments to pass to the function above
    # (see https://stackoverflow.com/a/28986876/8508004 and
    # https://stackoverflow.com/a/1496355/8508004 
    # (maybe https://stackoverflow.com/a/7437238/8508004 might help too) for 
    # related help). Makes it easy to add more later.


if __name__ == "__main__":
    ###-----------------for parsing command line arguments-------------------###
    import argparse
    parser = argparse.ArgumentParser(prog='missing_residue_detailer.py',
        description="missing_residue_detailer.py \
        takes a Protein DataBank entry identifier and gives missing residue \
        information in a nice summary table text.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")

    parser.add_argument("pdb_id",help="Text indicating a Protein DataBank \
        entry identifier. Example: `1d66` or `1D66`. ", metavar="PDB_IDENTIFIER")



    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    PDBid = args.pdb_id.lower()
    print(args)
    print(PDBid)

    main(PDBid)

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
