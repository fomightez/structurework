#!/usr/bin/env python
# pdbsum_stats_and_info_adpated_example.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# pdbsum_stats_and_info_adpated_example.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
#
#
# PURPOSE: Takes a PDB code and gets the corresponding data of resolution, 
# R-value, and ligands bound along the lines of this biostars post:
# https://www.biostars.org/p/9515231/#9515231
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
# Developed by adapting backbone of `pdbsum_prot_interface_statistics_to_df.py` 
# to handle getting information off main page and some ligand info
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
# python pdbsum_stats_and_info_adpated_example.py PDB_CODE
#-----------------------------------
# Issue `pdbsum_stats_and_info_adpated_example.py -h` for details.
# 
# More examples from running from the command line are at the links below: 
# https://git.io/Jtfon
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the data file (or data as a string) in the 
# call to the main function similar to below:
# df = pdbsum_stats_and_info_adpated_example("6kiv")
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
from pdbsum_stats_and_info_adpated_example import pdbsum_stats_and_info_adpated_example
df = pdbsum_stats_and_info_adpated_example("6kiv")
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
df_save_as_name = 'statsninfo_pickled_df.pkl' #name for pickled dataframe file

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



def get_n_save_Top_page_source(pdb_code):
    '''
    Take a PDB code identifier and gets the 'Top page' from PDBsum for that
    structure and saves the html as a text file. 

    Returns the file name of the text file produced, output_file_name, which
    has a uuid added from earlier.

    for example, 
    from 
    https://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=1eve&template=main.html ,which is the 'Top page' 
    page for 1eve, it will get the source html and save it

    '''
    from sh import curl
    main_url = (
        "http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl")
    curl("-L","-o","{}".format(output_file_name),
        "--data","pdbcode={}&t&template=main.html".format(pdb_code),
        "{}".format(main_url))
    return output_file_name

def get_protein_statsningo_table(pdb_code):
    #Takes a PDB entry accession identifier alphanumeic (PDB code) and gets
    # from PDBsum the HTML for the Top page
    # and converts it into a pandas dataframe.
    page_source_fn = get_n_save_Top_page_source(pdb_code)
    with open(page_source_fn, 'r') as input_file:
        raw_txt=input_file.read()
    resolution = raw_txt.split('Resolution:',1)[1].split("&Aring;",1)[0].split("<td align=left>")[-1].strip()+" Å"
    #print(resolution)
    r_value = raw_txt.split('R-factor:',1)[1].split("&nbsp;&nbsp;&nbsp;&nbsp;",1)[0].split("<td class=ntxt valign=top>")[-1].strip()
    #print(r_value)
    ligands_section_exp = raw_txt.split(
        '<b>Ligands</b>',1)[1].split("</table>",3)
    # HTML table to text adapted from https://www.geeksforgeeks.org/convert-html-table-into-csv-file-in-python/
    ligands_section = "</table>".join(ligands_section_exp[:2])
    ligands_end_of_hrefs = ligands_section.split("</a>")
    ligands_list = ", ".join([x.split()[-1] for x in ligands_end_of_hrefs[:-1]])
    #print(ligands_list)
    data_dict = { 'PDB id' : [pdb_code],
    'Resolution':[resolution],
    'R value':[r_value],
    'Ligands':[ligands_list]
        }

    # Storing the data into Pandas 
    # DataFrame  
    dataframe = pd.DataFrame(data_dict)
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

def pdbsum_stats_and_info_adpated_example(pdb_code, return_df = True, 
    pickle_df=True):
    '''
    Main function of script. 
    PDBsum information to Pandas dataframe.
    Optionally also returns a dataframe of the data. 
    Optionally can also return the PDB code found inside the parse data as well.
    Meant for use in a Jupyter notebook.

    Adapted from the main function in `blast_to_df.py`
    '''
    df = get_protein_statsningo_table(pdb_code)


        

    # feedback
    sys.stderr.write("Details for specified structure read and "
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
    pdbsum_stats_and_info_adpated_example(pdb_code,**kwargs)
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
    parser = argparse.ArgumentParser(prog='pdbsum_stats_and_info_adpated_example.py',
        description="pdbsum_stats_and_info_adpated_example.py \
        Takes a PDB code and gets some details & brings the information it into \
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
