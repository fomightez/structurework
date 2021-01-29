#!/usr/bin/env python
# pdbsum_prot_interactions_list_to_df.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.0"


# pdbsum_prot_interactions_list_to_df.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.8; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes a list of protein-protein interactions as text from PDBsum and 
# brings it into Python as a dataframe and saves a 
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
# Developed by adapting backbone of `hhsuite3_results_to_df` to handle the text
# data.
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
# python pdbsum_prot_interactions_list_to_df.py DATA_FILE_NAME
#-----------------------------------
# Issue `pdbsum_prot_interactions_list_to_df.py -h` for details.
# 
# More examples from running from the command line are at the links below: 
# https://git.io/Jtfon
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify at least the data file (or data as a string) in the 
# call to the main function similar to below:
# df = pdbsum_prot_interactions_list_to_df("test_data.txt")
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
df = pdbsum_prot_interactions_list_to_df("data.txt")
df
'''
#
# For testing, use these PDBsum data in addition to ones I was using at the time 
# because these cover more of a range of complexity:
#from 6KIZ Cryo-EM structure of human MLL1-NCP complex, binding mode2
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=C&chain2=G
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=B&chain2=N
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=C&chain2=E
#http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=6kiz&chain1=A&chain2=B
#
#*******************************************************************************
#





#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

## Settings and options for output dataframe-as-file 
df_save_as_name = 'prot_int_pickled_df.pkl' #name for pickled dataframe file

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


###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###

#*******************************************************************************
###------------------------'main' function of script---------------------------##

def pdbsum_prot_interactions_list_to_df(data_file, return_df = True, 
    pickle_df=True, return_pdb_code=False):
    '''
    Main function of script. 
    PDBsum list of interactions to Pandas dataframe.
    Optionally also returns a dataframe of the data. 
    Optionally can also return the PDB code found inside the parse data as well.
    Meant for use in a Jupyter notebook.

    Adapted from the main function in `blast_to_df.py`
    '''
    # These few varibales needs to be available early for 'empty' data files 
    # where there was no interaction between those chains
    column_names = (['Atom1 no.', 'Atom1 name', 'Atom1 Res name', 
        'Atom1 Res no.', 'Atom1 Chain', 'Atom2 no.', 'Atom2 name', 
        'Atom2 Res name', 'Atom2 Res no.', 'Atom2 Chain', 'Distance'])
    pdb_code_delimiter = "PDB code:"


    # Bring in the necessary data and prepare it in a manner for next step:
    #---------------------------------------------------------------------------
    # Bring in the file so it can be parsed
    with open(data_file, 'r') as int_file:
        raw_data_txt=int_file.read()

    pdb_code_id = raw_data_txt.split(pdb_code_delimiter,1)[1].split()[0]

    # Because of the way I set up parsing below I found if this is supplied with 
    # data from an 'empty' protein-protein interaction (e.g., 7c7a E B 
    # [http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=7c7a&chain1=E&chain2=B]
    # is empty while 7c7a E G 
    # [http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetIface.pl?pdb=7c7a&chain1=E&chain2=G] 
    # has only one interactions and isn't empty <=== those two good for 
    # testing handling then), it fails with an error (`IndexError: list index 
    # out of range` at the line of first parsting to assign `most_raw_data`).
    # This section will hopefully now catch those situations and make a
    # dataframe with the normal column names and one row of Nan while also 
    # giving feedback.
    if len(raw_data_txt.split("\n")) <= 8:
        # feedback
        sys.stderr.write("An 'empty' dataframe has been made as there "
            "**APPEARS TO BE NO INERACTIONS FOR THESE PAIRS OF CHAINS**.")
        df = pd.DataFrame(np.nan, index=[0], columns=column_names) # based on 
        # https://stackoverflow.com/a/30053507/8508004
        df['type'] = np.nan
        handle_pickling_the_dataframe(df, pickle_df,df_save_as_name)
        if return_df:
            returned = arrange_returning_the_dataframe_and_info(
                df,pdb_code_id,return_df,return_pdb_code)
            return returned
        sys.exit(0)

    # Split each type of section for parsing:
    #---------------------------------------------------------------------------
    split_on_string = "------------"
    # pdb_code_delimiter has been moved to top of function because needed for
    # 'empty' data where no interaction between the chains was observed
    typical_line_after_pdb = "------------------------------"
    # first collect the PDB code id <=== MOVED UP HIGHER LATER BECAUSE NEED FOR 
    # DATA WHERE NO INTERACTION SEEN, TOO
    #`pdb_code_id` now assigned above. (See above comment.)
    #print (pdb_code_id)
    # now remove everything before first first type of interactions section
    most_raw_data= raw_data_txt.split(
        pdb_code_delimiter,1)[1].split(
        typical_line_after_pdb,1)[1].split(split_on_string,1)[1]
    first_section_type = raw_data_txt.split(
        pdb_code_delimiter,1)[1].split(typical_line_after_pdb,1)[1].split(
        split_on_string,2)[0].rsplit("\n",2)[1]
    #print(first_section_type)
    #print(most_raw_data)
    # separate out tallies section, the section with `Number of...` at bottom, 
    # while easy to get and move out
    tallies_section = "Number of" + most_raw_data.split("Number of",1)[1]
    section_title_underl_replacement = "~~~~~~~~~~~~"
    interactions_sections_text = (
        first_section_type + "\n" + section_title_underl_replacement + 
        most_raw_data.split("Number of",1)[0])
    #print(interactions_sections_text)
    # Potentially there could just be one section if only one type of 
    # interaction. Check for that case and skip additional processing for other
    # sections if that is the case. Since replaced underline in first section
    # with different symbol, if the section delimiter no longer exists in the 
    # `interactions_sections_text` that means it is only that section.
    if split_on_string in interactions_sections_text:
        # Now make a string for each section with the title/type as a key. Place 
        # each as an item in a list to have all types separate.
        sections = []
        # Since the title is above the delimiter for the two not touched yet (recall
        # first section already replaced with section_title_underl_replacement), it
        # will be annoying to keep type with each section but can be done.
        # Having those sections after the first untouched also means the first 
        # section is fairly well demarcated although need to leave off the 
        # type of the next section since it occurs before delimiter
        first_section_text = interactions_sections_text.split(
            split_on_string,1)[0].rsplit("\n",2)[-3]
        #print(first_section_text)
        # And add that as a type:text key value pair to the sections list.
        sections.append(type_2_key_and_text_to_value(
            first_section_text,section_title_underl_replacement))
        # Now remove that text block from interactions_sections_text to only
        # leave any other sections needing parsing to type and text.
        remaining_to_split_to_sections = (
            interactions_sections_text[len(first_section_text)+1:])
        #print(remaining_to_split_to_sections)
        delimiters_in_text_to_process = remaining_to_split_to_sections.count(
            split_on_string)
        for x in range(delimiters_in_text_to_process):
            if x == delimiters_in_text_to_process-1:
                #pass then this is the last section so process slightly 
                # different since just use end as end and don't need to look for
                # next delimiter
                sections.append(type_2_key_and_text_to_value(
                    remaining_to_split_to_sections,split_on_string))
            else:
                next_section_text = remaining_to_split_to_sections.rsplit(
                    split_on_string,1)[0].rsplit("\n",2)[-3] # note the 
                # `rsplit()` is to leave off the type header of the next section 
                # as above
                # And add that as type:text key value pair to the sections list.
                sections.append(type_2_key_and_text_to_value(
                    next_section_text,split_on_string))
                # Now remove that text block from interactions_sections_text to 
                # only leave any other sections needing parsing to type & text.
                remaining_to_split_to_sections = (
                    remaining_to_split_to_sections[len(next_section_text)+1:])
    else:
        sections = [type_2_key_and_text_to_value(
            interactions_sections_text,section_title_underl_replacement)]

    # Remove the Atom set column indicator lines:
    #---------------------------------------------------------------------------
    # Remove `<----- A T O M   1 ----->       <----- A T O M   2 ----->` line at
    # start of each section.
    col_indic = "<----- A T O M   1 ----->       <----- A T O M   2 ----->\n"
    fixed_sections = []
    for section in sections:
        fixed_section = {}
        for k,v in section.items():
            if col_indic in v:
                fixed_section[k] = v.split(col_indic)[1].strip()
        fixed_sections.append(fixed_section)
    sections = fixed_sections 


    

    # Collect each type of interaction as a separate dataframe:
    #---------------------------------------------------------------------------
    # The `type` column will distinguish the type so that the different 
    # dataframes can be combined later.
    ''' # from DEVELOPING
    df = pd.read_csv(StringIO(
        list(sections[0].values())[0]),header=[0,1], delim_whitespace = True) # 
    # So the issue is that `Atom` and `Res` abbreviations are on top line of 
    # table with specific properties related on second line so far using 
    # https://stackoverflow.com/q/41005577/8508004 to make multinidex and then 
    # using the join based on https://stackoverflow.com/a/46357204/8508004; note 
    # that this was not working with `pd.read_table()` because it was just 
    # reading the two rows as two strings; fortunately, I read 
    # https://stackoverflow.com/a/57574961/8508004 that said `pd.read_table()` 
    # was deprecated (which I am not 100% sure it is), however, that encouraged 
    # me to try switching to `pd.read_cvs()` with `delim_whitespace = True` 
    # caused  Multindex coloumns to be made that was then easily combined to 
    # single line using `join` approach I had seen a couple places for making 
    # double line multindex into single line, for example see 
    # https://stackoverflow.com/a/46357204/8508004)
    #df.columns = df.columns.map(' '.join)
    # However. that approach to the columns names was getting much closer it was
    # not perfect because chain doesn't have a modifier and so was throwing the
    # map off. So can I fix or hand edit? Looking at result of `print(list(df.columns))` without `df.columns = df.columns.map(' '.join)` made it clear the shift is there from the start and easier to just define. Had to add in `atom1` and `2` because duplicate names not allowed.
    '''
    #column_names assignment  WAS MOVED TO TOP BECAUSE NEEDED IT AVAILABLE FOR 
    # WHEN AN 'EMPTY' DATA FILE IS PRROVIDED WHERE NO CHAIN-CHAIN INTERACTIONS 
    # IN THE DATA.
 
    ''' # More from DEVELOPING
    df1 = pd.read_csv(StringIO(list(sections[0].values())[0]),
        delim_whitespace = True, skiprows = 2, names=column_names)
    df1.index = df1.index.astype('int64')
    # add the type of interaction which comes from the key
    df1['type'] = list(sections[0].keys())[0]
    print(df1)
    df2 = pd.read_csv(StringIO(list(sections[1].values())[0]),
        delim_whitespace = True, skiprows = 2, names=column_names)
    df2.index = df2.index.astype('int64')
    df2['type'] = list(sections[1].keys())[0]
    print(df2)
    print(df2.index)
    '''
    dfs = []
    for indx,section in enumerate(sections):
        df_per_section = pd.read_csv(StringIO(list(sections[indx].values())[0]),
            delim_whitespace = True, skiprows = 2, names=column_names)
        df_per_section.index = df_per_section.index.astype('int64')
        df_per_section['type'] = list(sections[indx].keys())[0]
        dfs.append(df_per_section)


    # Make collected data tables into single dataframe:
    #---------------------------------------------------------------------------
    # df = pd.concat([df1,df2], ignore_index=True) # from developing
    df = pd.concat(dfs, ignore_index=True)
    #print(df)


        

    # feedback
    sys.stderr.write("Provided interactions data read and converted to a dataframe...")


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
    pdbsum_prot_interactions_list_to_df(data_file,**kwargs)
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
    parser = argparse.ArgumentParser(prog='pdbsum_prot_interactions_list_to_df.py',
        description="pdbsum_prot_interactions_list_to_df.py \
        Takes a list of protein-protein interactions from PDBsum and brings it \
        into Python as a dataframe and \
        saves a file of that dataframe for use elsewhere. Optionally, it can \
        also return that dataframe for use inside a Jupyter notebook. \
        Meant to be a utility script for working \
        with PDBsum and Python.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")
    parser.add_argument("interactions_file", help="Name of file of interactions \
        file to parse.\
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
