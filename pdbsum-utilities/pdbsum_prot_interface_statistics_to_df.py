#!/usr/bin/env python
# pdbsum_prot_interface_statistics_to_df.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# pdbsum_prot_interface_statistics_to_df.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.8; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a PDB code and gets the corresponding protein-protein interface 
# statistics from PDBsum and brings it into Python as a dataframe and saves a 
# file of that dataframe for use elsewhere. 
# Optionally, it can also return that dataframe for use inside a Jupyter 
# notebook.
#
# This script is meant to be a utility script for working with PDBsum and 
# Python, see a demonstration of use in
# https://github.com/fomightez/pdbsum-binder
# It will be part of a larger set of tools meant to facilitate highlighting
# differences & similarities in protein-protein interactions of the same protein
# pairs in different, related complexes.
# 
#
#
# Written to run from command line or imported into/pasted/loaded inside a 
# Jupyter notebook cell. 
#
#
#
# 
#
#
#
#
# Developed by adapting backbone of `pdbsum_prot_interactions_list_to_df` to 
# handle interface statistics.
#
#
# Dependencies beyond the mostly standard libraries/modules:
#
#
#
# VERSION HISTORY:
# v.0.1. basic working version

#
# To do:
# - make sure works with Python 2.7 <- sometimes I was lazy during development 
# used f-strings, & those need to be replaced with string formatting using 
# `.format()` because Python 2.7 never had f-strings, unless I add the use of 
# future_fstrings package, see https://stackoverflow.com/a/46182112/8508004
#
#
#
#
# TO RUN:
# Examples,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python pdbsum_prot_interface_statistics_to_df.py PDB_CODE
#-----------------------------------
# Issue `pdbsum_prot_interface_statistics_to_df.py -h` for details.
# 
# More examples from running from the command line are at the links below: 
# https://git.io/Jtfon
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the data file (or data as a string) in the 
# call to the main function similar to below:
# df = pdbsum_prot_interface_statistics_to_df("6kiv")
# df
#
#
# A more in-depth series of examples of using this script within a notebook 
# without need to save file intermediates is found at:
# https://git.io/Jtfon
#
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
from pdbsum_prot_interface_statistics_to_df import pdbsum_prot_interface_statistics_to_df
df = pdbsum_prot_interface_statistics_to_df("6kiv")
df
'''
#
#*******************************************************************************
#





#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

## Settings and options for output dataframe-as-file 
df_save_as_name = 'int_stats_pickled_df.pkl' #name for pickled dataframe file

output_file_name_prefix = "page_source" #at present this gets deleted & so I use
# datetime stamp to make unique so limited chance it deletes wrong thing
#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************













#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
import pandas as pd
import numpy as np
# I need StringIO so string handled as file document. Also need to deal 
# with whether Python 3 or 2 because StringIO source differs for Python 2.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import uuid 
from bs4 import BeautifulSoup

output_file_name = "{}{}.htm".format(
    output_file_name_prefix,uuid.uuid1().time) # based 
# https://www.geeksforgeeks.org/generating-random-ids-using-uuid-python/ ; using
# because I don't need this to be human readable and I tested and one made mere
# milliseconds later unique and I dob't have to worry how to handle it myself


###---------------------------HELPER FUNCTIONS-------------------------------###

def _(row):
    '''
    takes the row and .... PLACEHOLDER FOR NOW
    '''
    return _

def split_out_len(text_str):
    '''
    Takes a text string and splits out the number value from in between the 
    parantheses at the end.

    Returns in integer value

    Example input string:
    41-281 (291)

    Example return:
    291
    '''
    return int(text_str.split("(")[1].split(")")[0])



def get_n_save_protprot_page_source(pdb_code):
    '''
    Take a PDB code identifier and gets the Prot-prot page from PDBsum for that
    structure and saves the html as a text file. 

    Returns the file name of the text file produced, output_file_name, which
    has a uuid added from earlier.

    for example, 
    from 
    http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=6kiv&template=interfaces.html ,which is the 'Prot-prot' 
    page for 6kiv, it will get the source html and save it

    Originally included as a helper function in 
    `pdb_code_to_prot_prot_interactions_via_PDBsum.py`; put here because this
    code short enough to not be too much if in two places in the PDBsum utility
    scripts
    '''
    from sh import curl
    main_url = (
        "http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl")
    curl("-L","-o","{}".format(output_file_name),
        "--data","pdbcode={}&template=interfaces.html".format(pdb_code),
        "{}".format(main_url))
    return output_file_name

def get_protein_inter_stats_table(pdb_code):
    #Takes a PDB entry accession identifier alphanumeic (PDB code) and gets
    # from PDBsum the HTML for the 'Interface statistics' portion of the page
    # and converts it into a pandas dataframe.
    page_source_fn = get_n_save_protprot_page_source(pdb_code)
    with open(page_source_fn, 'r') as input_file:
        raw_txt=input_file.read()
    interface_statistics_section = raw_txt.split(
        '<B>Interface statistics</B>',1)[1].split("</table>",1)[0]
    # HTML table to text adapted from https://www.geeksforgeeks.org/convert-html-table-into-csv-file-in-python/

    data = []
    soup = BeautifulSoup(interface_statistics_section,'html.parser') #parser & 
    # use of string described at 
    # http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/
    table_header_html = soup.find_all("table")[0].find_all("tr")[1] 
    list_header = []
    for items in table_header_html.find_all("td"): 
        try: 
            list_header.append(items.get_text()) 
        except: 
            continue
    # Do a few steps to actually clean up the column names in the header 
    # for some reason the salt briges column name comes out from beautifulsoup
    # without space between`salt` and `of`. This fixes:
    list_header = [x.replace("ofsalt","of salt") for x in list_header]
    list_header = [x.replace("\xa0"," ") for x in list_header] #remove line
    #breaks symbols
    list_header = [x.replace("\n"," ") for x in list_header] #remove new line 
    #symbol
    list_header = [x.replace("  "," ") for x in list_header] #collapse double
    # spaces into one
    list_header = [x.strip() for x in list_header] # remove trailing spaces
    list_header = [x for x in list_header if x] #remove blank entries coming 
    # from the 'spacing-gifs' put in of height 1 & width 3 with no text content

      
    # for getting the data  
    HTML_data = soup.find_all("table")[0].find_all("tr")[2:] 
    signals_chain = "/thornton-srv/databases/pdbsum/templates/gif/chain"

    # For some structures there is a note about 'Indented interfaces' that adds
    # lines below that shouldn't be part of the  table and so this will detect
    # such cases and truncate the html up to that point and add the proper html
    # closing so the detection of the lines still works.---------------------##
    indented_note = '''<b>Note</b>. Indented interfaces in the table are equivalent to the
      last prior non-indented interface. Equivalent chains are listed below.
      <br/>'''
    if indented_note in str(HTML_data):
        h_data = str(
            HTML_data)[:str(HTML_data).index(indented_note)] + indented_note
        h_data = h_data.replace(indented_note,"</td></tr>")
        HTML_data = BeautifulSoup(h_data,'html.parser') 
    # End dealing with note about 'Indented interfaces'-----------------------##
      
    for element in HTML_data: 
        sub_data = [] 
        for sub_element in element:
            if signals_chain in str(sub_element):
                #print(sub_element)
                sub_element_2ndpart = str(sub_element).split(signals_chain,1)[1]
                sub_element_pt1 = sub_element_2ndpart.split('.jpg"')[0]
                sub_element_pt2 = sub_element_2ndpart.split(
                    signals_chain,1)[1].split('.jpg"')[0]
                sub_element_string = sub_element_pt1 + ":"+ sub_element_pt2
                sub_element = BeautifulSoup(sub_element_string,'html.parser') 
            try: 
                sub_data.append(sub_element.get_text()) 
            except: 
                continue
        data.append(sub_data) 

    # Similar to column names, clean up the data section
    clean_data = []
    for subdata in data:
        clean_subdata = [x.replace("\xa0"," ") for x in subdata]
        clean_subdata= [x.replace("\n","") for x in clean_subdata]
        clean_subdata = [x for x in clean_subdata if x]
        clean_data.append(clean_subdata)
    data = [x for x in clean_data if x] # remove blank lists from 'empty' lines

    # need to merge elements at index 1-3 and 4-6 into single entries
    clean_data = []
    for subdata in data:
        clean_subdata = ([subdata[0]] + ["".join(subdata[1:4])] + 
            ["".join(subdata[4:7])] + subdata[7:])
        clean_data.append(clean_subdata)
    data = clean_data
      
    # Storing the data into Pandas 
    # DataFrame  
    dataframe = pd.DataFrame(data = data, columns = list_header)
    os.remove(page_source_fn)
    return dataframe

def handle_pickling_the_dataframe(df, pickle_df,df_save_as_name):
    '''
    Was at end but moved to a function because will be used when 'empty' data
    provided where no interaction occurs.
    '''
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

def arrange_returning_the_dataframe_and_info(
    df,pdb_code_id,return_df,return_pdb_code):
    '''
    Was at end but moved to a function because will be used when 'empty' data
    provided where no interaction occurs.
    '''
    if return_df and return_pdb_code:
        sys.stderr.write("\n\nReturning both the PDB code identifier and a "
            "dataframe with the information as well.")
        return pdb_code_id,df
    elif return_df:
        sys.stderr.write("\n\nReturning a dataframe with the information "
                "as well.")
        return df


###--------------------------END OF HELPER FUNCTIONS-------------------------###
###--------------------------END OF HELPER FUNCTIONS-------------------------###

#*******************************************************************************
###------------------------'main' function of script--------------------------##

def pdbsum_prot_interface_statistics_to_df(pdb_code, return_df = True, 
    pickle_df=True):
    '''
    Main function of script. 
    PDBsum protein-protein Interface statistics table  to Pandas dataframe.
    Optionally also returns a dataframe of the data. 
    Optionally can also return the PDB code found inside the parse data as well.
    Meant for use in a Jupyter notebook.

    Adapted from the main function in `blast_to_df.py`
    '''
    df = get_protein_inter_stats_table(pdb_code)


        

    # feedback
    sys.stderr.write("Interface statistics for provided structure read and "
        "converted to a dataframe...")


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
    handle_pickling_the_dataframe(df, pickle_df,df_save_as_name)

    
    # Return dataframe and pdb code(options)
    #---------------------------------------------------------------------------
    if return_df:
        sys.stderr.write("\n\nReturning a dataframe with the information "
            "as well.")
        return df
    

###--------------------------END OF MAIN FUNCTION----------------------------###
###--------------------------END OF MAIN FUNCTION----------------------------###










#*******************************************************************************
###------------------------'main' section of script---------------------------##
def main():
    """ Main entry point of the script """
    # placing actual main action in a 'helper'script so can call that easily 
    # with a distinguishing name in Jupyter notebooks, where `main()` may get
    # assigned multiple times depending how many scripts imported/pasted in.
    kwargs = {}
    if df_save_as_name == 'no_pickling':
        kwargs['pickle_df'] = False
    kwargs['return_df'] = False #probably don't want dataframe returned if 
    # calling script from command line
    pdbsum_prot_interface_statistics_to_df(pdb_code,**kwargs)
    # using https://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/#calling-a-function
    # to build keyword arguments to pass to the function above
    # (see https://stackoverflow.com/a/28986876/8508004 and
    # https://stackoverflow.com/a/1496355/8508004 
    # (maybe https://stackoverflow.com/a/7437238/8508004 might help too) for 
    # related help). Makes it easy to add more later.





if __name__ == "__main__" and '__file__' in globals():
    """ This is executed when run from the command line """
    # Code with just `if __name__ == "__main__":` alone will be run if pasted
    # into a notebook. The addition of ` and '__file__' in globals()` is based
    # on https://stackoverflow.com/a/22923872/8508004
    # See also https://stackoverflow.com/a/22424821/8508004 for an option to 
    # provide arguments when prototyping a full script in the notebook.
    ###-----------------for parsing command line arguments-------------------###
    import argparse
    parser = argparse.ArgumentParser(prog='pdbsum_prot_interface_statistics_to_df.py',
        description="pdbsum_prot_interface_statistics_to_df.py \
        Takes a PDB code and gets the corresponding \
        protein-protein interface statistics from PDBsum and brings it into \
        Python as a dataframe and saves a file of \
        that dataframe for use elsewhere. Optionally, it can \
        also return that dataframe for use inside a Jupyter notebook. \
        Meant to be a utility script for working \
        with PDBsum and Python.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")
    parser.add_argument("pdb_code", help="Identifier code of structure at PDB.",
        metavar="PDB_CODE")
    parser.add_argument('-dfo', '--df_output', action='store', type=str, 
    default= df_save_as_name, help="OPTIONAL: Set file name for saving pickled \
    dataframe. If none provided, '{}' will be used. To force no dataframe to \
    be saved, enter `-dfo no_pickling` without quotes as output file \
    (ATYPICAL).".format(df_save_as_name))



    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    pdb_code = args.pdb_code
    df_save_as_name = args.df_output


    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
