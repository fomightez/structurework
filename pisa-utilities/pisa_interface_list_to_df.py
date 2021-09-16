#!/usr/bin/env python
# pisa_interface_list_to_df.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# pisa_interface_list_to_df.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.8; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a list of inter chain interactions as text from PDBePISA 
# Interfaces page & brings it into Python as a dataframe and saves a file of 
# that dataframe for use elsewhere. 
# Optionally, it can also return that dataframe for use inside a Jupyter 
# notebook.
# First 'word' in the input filename should be the PDB code of the associated data 
# this is what the script will assume. The 'word' needs to be separated with 
# space and not other delimiters, such as an underscore.
# 
# PDBePISA Interfaces page to collect and save as a text file to use as input 
# here is the text table on the PDBePISA Interfaces page for a PDB entry. Select 
# with your mouse the text that begins with `##` through to before the buttons 
# below it and save that as a text file with a text editor.
#
# This script is meant to be a utility script for working with PDBePISA server
# and Python, see a demonstration of use in
# https://github.com/fomightez/XXXXXXX-binder
# It will be part of a larger set of tools meant to facilitate highlighting
# differences & similarities in protein-protein and protein-nucleic 
# interactions of the same protein pairs in different, related complexes, using 
# data from PDBsum, as well. The PDBsum-utilizing code is demonstrated in 
# https://github.com/fomightez/pdbsum-binder
# 
#
#
# Written to run from command line or imported into/pasted/loaded inside a 
# Jupyter notebook cell. When doing in Jupyter (or IPython, I believe) you can 
# skip the file save intermediate, see https://git.io/Jtfon for these advanced 
# examples.
#
#
#
# 
#
#
#
#
# Developed by adapting backbone of `pdbsum_prot_interactions_list_to_df.py` to 
# handle the text data.
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
# - update text after "and Python, see a demonstration of use in" to have correct link
# - reference this script in header documentation of:
#        - pdbsum_prot_interactions_list_to_df.py
#        - pdbsum_prot_interface_statistics_comparing_two_structures.py
#        - pdbsum_prot_interface_statistics_to_df.py
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
# python pisa_interface_list_to_df.py <pdb_code> REST_OF_DATA_FILE_NAME
#-----------------------------------
# Issue `pisa_interface_list_to_df.py -h` for details.
# 
# More examples from running from the command line are at the links below: 
# https://XXXXXXX
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the data file (or data as a string) in the 
# call to the main function similar to below:
# df = pisa_interface_list_to_df("6agb interface_data.txt")
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
df = pisa_interface_list_to_df("6agb interface_data.txt")
df
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

## Settings and options for output dataframe-as-file 
df_save_as_name = 'PISAinterface_summary_pickled_df.pkl' #name for pickled 
# dataframe file

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


###---------------------------HELPER FUNCTIONS---------------------------------###

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


def type_2_key_and_text_to_value(text,title_underline):
    '''
    Takes text and splits out the type/title and the text after, removing the
    string `<-->`. The string `<-->` in the rows of data later cause parsing
    by `read_csv` to be more difficult than it needs to be and so better to
    just remove while I have the section text.
    '''
    parts = text.split(title_underline,1)
    return {parts[0].strip():parts[1].strip().replace('<-->','')}

def handle_pickling_the_dataframe(df, pickle_df, pdb_code, df_save_as_name):
    '''
    Was at end but moved to a function because will be used when 'empty' data
    provided where no interaction occurs.
    '''
    if pickle_df == False:
        sys.stderr.write("\n\nA dataframe of the data "
        "was not stored for use\nelsewhere "
        "because `no_pickling` was specified.")
    else:
        df_save_as_name = pdb_code + "_"+ df_save_as_name
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


###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###

#*******************************************************************************
###------------------------'main' function of script---------------------------##

def pisa_interface_list_to_df(data_file, return_df = True, 
    pickle_df=True, return_pdb_code=False):
    '''
    Main function of script. 
    PDBsum list of interactions to Pandas dataframe.
    Optionally also returns a dataframe of the data. 
    Optionally can also return the PDB code found inside the parse data as well.
    Meant for use in a Jupyter notebook.

    Adapted from the main function in `pdbsum_prot_interactions_list_to_df.py`
    '''
    # Prepare for getting necessary data by setting up column names:
    #---------------------------------------------------------------------------
    column_names = (['row #','dropHERE', 'Chain 1', 'Number_InterfacingAtoms1', 
        'Number_InterfacingResidues1', 'Surface area1', 'dropHEREb',
        'Chain 2', 'Number_InterfacingAtoms2',
        'Number_InterfacingResidues2','Surface area2', 'Interface area', 'Solvation free energy gain', 
        'Solvation gain P-value', 'Interface Hydrogen bonds', 'Interface Salt Bridges',
        'Interface Disuflides','CSS'])
    # column naming for multiindex handling borrows from things worked out in `make_table_of_missing_residues_for_related_PDB_structures.py`
    cols_4_each_pdb = (["Residues not observed (+, -)",
        "% Not observed",
        "Deficient terminus?",
        "Missing ranges"])
    column_names_list = column_names


    # Bring in the necessary data and prepare it in a manner for next step:
    #---------------------------------------------------------------------------
    df = pd.read_csv(
    data_file, sep='\t',index_col=False , 
    skiprows =5, names = column_names_list) # brings in the text of the table 
    # that startswith `## and ends before the buttons below that table on the 
    # PISA server Interfaces page.
    # drop the columns that got tagged with special names during bring in.
    df = df.drop(['dropHERE','dropHEREb'],axis=1)
    # Improve on column headers by making multiindex:
    upper_level_list = [' ','Chain 1','Chain 1','Chain 1'
                    ,'Chain 1', 'Chain 2', 'Chain 2'
                   , 'Chain 2', 'Chain 2','Interface'
                   ,'Interface','Interface','Interface','Interface'
                   ,'Interface', 'Interface'] # based on 
    # https://stackoverflow.com/a/24225106/8508004
    #With multiindex, I can use duplicates of the bottom level column names
    # so I can now simplify column names
    column_names_simplified = (['row #','Chain label','Number_InterfacingAtoms', 
            'Number_InterfacingResidues', 'Surface (Å$^2$)', 
            'Chain label', 'Number_InterfacingAtoms',
            'Number_InterfacingResidues','Surface (Å$^2$)', 'Area (Å$^2$)', 
            'Solvation free energy gain', 
            'Solvation gain P-value', 'Hydrogen bonds', 'Salt Bridges',
            'Disuflides','CSS'])
    # superscript in column names based on https://stackoverflow.com/q/45291459/8508004
    cols = pd.MultiIndex.from_arrays([upper_level_list, column_names_simplified])
    df = df.set_axis(cols, axis=1, inplace=False)

    pdb_code_id = data_file.split()[0] # PDB code for the associated assumed as 
    # first 'word' in file name of input



        

    # feedback
    sys.stderr.write(
        "Provided interactions data read and converted to a dataframe...")


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
    handle_pickling_the_dataframe(df, pickle_df,pdb_code_id, df_save_as_name)

    
    # Return dataframe and pdb code(options)
    #---------------------------------------------------------------------------
    if return_df:
        returned = arrange_returning_the_dataframe_and_info(
            df,pdb_code_id,return_df,return_pdb_code)
        return returned
    

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
    pisa_interface_list_to_df(data_file,**kwargs)
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
    parser = argparse.ArgumentParser(prog='pisa_interface_list_to_df.py',
        description="pisa_interface_list_to_df.py \
        Takes a list of chain interactions from PDBePISA and brings it \
        into Python as a dataframe and \
        saves a file of that dataframe for use elsewhere. Optionally, it can \
        also return that dataframe for use inside a Jupyter notebook. \
        Meant to be a utility script for working \
        with PDBePISA and Python.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")
    parser.add_argument("interactions_file", help="Name of file of interactions \
        file to parse with associated pdb code as first 'word' in file name.\
        ", metavar="DATA_FILE")
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
    data_file = args.interactions_file
    df_save_as_name = args.df_output


    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
