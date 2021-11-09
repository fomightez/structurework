#!/usr/bin/env python
# pisa_interface_list_to_df.py
__author__ = "Wayne Decatur" #fomightez on GitHub
__license__ = "MIT"
__version__ = "0.1.5"


# pisa_interface_list_to_df.py by Wayne Decatur
# ver 0.1.5
#
#*******************************************************************************
# Verified compatible with both Python 2.7 and Python 3.8; written initially in 
# Python 3. 
#
#
# PURPOSE: Takes an alphanumeric accession id code for a PDB entry and gets the
# list of inter-chain interactions as text from PDBePISA Interfaces page, unless
# that text is provided as a file, & brings it into Python as a dataframe and 
# saves a file of that dataframe for use elsewhere. 
# Optionally, it can also return that dataframe for use inside a Jupyter 
# notebook.
# 
# A user can also provide in the working directory the copied text of a PDBePISA 
# Interfaces page if it is named with the corresponding accession code id 
# followed immediately by the suffix listed as 
# `suffix_for_input_data_file` below. To get the text from the interface page, 
# select with your mouse the text that begins with `##` through to before the
# buttons below it & save that as a text file with a text editor with the name 
# that description would generate. The idea is this gives a way to supply table 
# content that was previously obtainted or has been edited. This should help
# if there's any edge cases that don't get processed to a dataframe without 
# hiccups or if this needs to be used offline. If no such file is provided, the
# data is obtained from PDBePISA, corresponding to the accession code provided,
# saved as an intermediate with a name corresponding to that described above &
# that gets used to generate the corresponding dataframe.
#
# This script is meant to be a utility script for working with PDBePISA server
# and Python, see a demonstration of use in
# https://github.com/fomightez/pdbepisa-binder
# It will be part of a larger set of tools meant to facilitate analysis of
# interactions in complexes, using 
# data from PDBePISA, as well. The PDBePISA-utilizing code is demonstrated in 
# https://github.com/fomightez/pdbepisa-binder
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
# Developed by adapting backbone of `pdbsum_prot_interactions_list_to_df.py` to 
# handle the text data.
#
#
# Dependencies beyond the mostly standard libraries/modules:
# - html2text
# - rich
#
#
#
# VERSION HISTORY:
# v.0.1.0 basic working version
# v.0.1.2 now gets data from PDBePISA if not provided & handles crystal 
#         structure interface lists/reports with symmetry op info
# v.0.1.3 now handles crystal & cryo-EM structure lists/reports with 'Average' 
#         rows
# v.0.1.4 keeps the column that may have symbol indicating interface 
#         properties
# v.0.1.5 no longer assumes true rows that comes in from retrieving HTML of 
#         report from PDBePISA (in `make_data_input_file_name`) are split over 
#         three lines
#         
#

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
# python pisa_interface_list_to_df.py <pdb_code>
#-----------------------------------
# Issue `pisa_interface_list_to_df.py -h` for details.
# 
# More examples from running from the command line are at the links below: 
# https://github.com/fomightez/structurework/tree/master/pdbepisa-utilities
# https://github.com/fomightez/pdbepisa-binder
#
#
#
# To use this after importing/pasting or loading into a cell in a Jupyter 
# notebook, specify the PDB identifier code as a string in the 
# call to the main function similar to below:
# df = pisa_interface_list_to_df("6agb")
# df
#
#
# A more in-depth series of examples of using this script within a notebook 
# is found at:
# https://github.com/fomightez/pdbepisa-binder/notebooks/Working%20with%20PDBePISA%20interfacelists%20in%20Jupyter%20Basics.ipynb
#
# 
#
'''
CURRENT ACTUAL CODE FOR RUNNING/TESTING IN A NOTEBOOK WHEN IMPORTED/LOADED OR 
PASTED IN ANOTHER CELL:
df = pisa_interface_list_to_df("6agb")
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

suffix_for_input_data_file = "_interface_list.txt" # the rest of the file name, 
# after the PDB id code, that the retrieved interface table text will be saved 
# as an intermediate to be read in tp create the dataframe.
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
import fnmatch
import pandas as pd
import numpy as np
# I need StringIO so string handled as file document. Also need to deal 
# with whether Python 3 or 2 because StringIO source differs for Python 2.
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Try rich for replacing std.err feedback I generally use?
from rich.console import Console
console = Console(width=60)

###---------------------------HELPER FUNCTIONS--------------------------------###

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

def print_separator_lines_to_console(num_lines=1,skip=0):
    '''
    Takes an optional integer as input to be the number of Rich 'rules' or 
    horizonal lines to print to the console.

    Defaults to 1 line.

    Optionally, you can provide a number of initial colors to skip if you don't
    like the ones you are seeing come up first.
    '''
    import itertools
    color_list = (['bright_yellow','bright_green','bright_blue','bright_cyan', 
        'bright_magenta', 'bright_red','yellow','green','blue','cyan' 'magenta', 
        'red'])
    color_generator_emitter = itertools.cycle(color_list)
    if skip:
        for s in range(skip):
            next(color_generator_emitter)
    for x in range(num_lines):
        console.rule(style=next(color_generator_emitter))

replacement_header = ''' ##      Structure 1     ×   Structure 2     interface 
 area, Å2    ΔiG 
 kcal/mol    ΔiG 
 P-value     NHB     NSB     NDS     CSS 
 NN      «»      Range   iNat    iNres   Surface Å2      Range   iNat    iNres   Surface Å2 '''
repl_header_with_sym = ''' ##   Structure 1     ×   Structure 2     interface 
 area, Å2    ΔiG 
 kcal/mol    ΔiG 
 P-value     NHB     NSB     NDS     CSS 
 NN      «»      Range   iNat    iNres   Surface Å2      Range   Symmetry op-n   Sym.ID      iNat    iNres   Surface Å2 ''' #Even though 
# this won't get used for making the dataframe, but baking in the extra 
# 'Symmetry' columns makes it easy to signal downstream such extra columns are 
# there & keeps things consistent because it makes what you'd get if you copied 
# it from the page using your mouse.

def make_data_input_file_name(data_input_file_name):
    '''
    Takes the name of the `data_input_file_name` which will begin with the code 
    id of the corresponding PDB entry and gets from PDBePISA the interface list
    data for that entry. Then saves that as a file with the provided 
    `data_input_file_name` string as it's name.

    Doesn't return anything. Just makes the file with the contents of the 
    interface file in a form that would be the same if the text was copied 
    directly from the interface list page.
    '''
    pdb_code =  data_input_file_name.split("_",1)[0].strip() # it will already
    # be lowercase when this function is triggered & so that step isn't needed 
    # here
    # Use request to get the interface data page as html
    import urllib.request
    site_for_retrieving_from = ("http://www.ebi.ac.uk/pdbe/pisa/cgi-bin/"
        "piserver?qi={}".format(pdb_code))
    retrieval_string = ("[bold bright_magenta]Retrieving interface list page"
    " from PDBePISA...")
    retrieval_string = ("Retrieving interface list page"
    " from PDBePISA...")
    with console.status(retrieval_string, 
        spinner = 'dots12', spinner_style='bold red on white') as status:
        stream_handle = urllib.request.urlopen(site_for_retrieving_from)
    extr_string = ("[bold bright_green]Extracting interface list from"
    " the page..")
    extr_string = ("Extracting interface list from"
    " the page..")
    console.print(extr_string,style="bold red on white")
    pg_html = stream_handle.read().decode("utf-8") # so it isn't bytes; from 
    # `find_mito_fungal_lsu_rRNA_and_check_for_omega_intron.py`.
    # Convert the table contents to text
    import html2text
    h = html2text.HTML2Text()
    h.ignore_links = True
    page_contents_as_text = h.handle(pg_html)
    # Parse the raw html to just get the table contents
    start_delimiter = 'XML    View\nDetails    Download Search'
    end_delimiter = 'View    Details    Download Search'
    intrf_tbl_text = page_contents_as_text.split(
        start_delimiter,1)[1].split(end_delimiter,1)[0]
    # The tables with the 'Average' rows and 'Id' columns (see below) don't have
    # anything representing the 'Id' column on the lines without entries in that
    # column and so the '##' number (row #) gets placed there incorrectly. 
    # Luckily the rows like this in tables with the 'Id' columns, begin with 
    # ticks & matches tick-space-integer-space-tick, but don't match '` 0.' and 
    # the lines are longer than 40 characters
    # and don't look like start with `` 3_656`, i.e. with underscore 3 after 
    # tick, and doesn't lool like `` |`.
    # Actually matching start of line with 'tick-space-integer-space-tick' will
    # cover most of those cases. Since potentially number could get double 
    # digits, don't limit to single. So use 
    # https://stackoverflow.com/a/8586432/8508004
    if '**_Average:_**' in intrf_tbl_text:
        import re
        int_flanked_by_ticks_pattern = re.compile("` [0-9]+ `")
        intrf_tbl_text_edited_to_account_for_id = ""
        for line in intrf_tbl_text.split("\n"):
            if line.count("`") >= 2 and line[:7].count("`") >= 2:
                at_start_between_ticks = line[:7].split("`",2)[1]
                at_start_bound_by_ticks = "`"+at_start_between_ticks+"`" #put 
                # back delimiter, ticks in this case to restore string to what 
                # it really is at start of the line.
                # Check match using https://stackoverflow.com/a/12595082/8508004 .
                if (line.strip().startswith("`")) and (
                    int_flanked_by_ticks_pattern.match(at_start_bound_by_ticks)
                    ) and (len(line)>40):
                    to_add = "  |  " + at_start_bound_by_ticks
                    to_add_in_plus_rest_o_line = to_add + line.split("`",2)[2]
                    intrf_tbl_text_edited_to_account_for_id += (
                        to_add_in_plus_rest_o_line + "\n")
                else:
                    intrf_tbl_text_edited_to_account_for_id += line + "\n"
            else:
                intrf_tbl_text_edited_to_account_for_id += line + "\n"
        #now that done iterating on lines of 'intrf_tbl_text', replace 
        # 'intrf_tbl_text' with new version
        intrf_tbl_text = intrf_tbl_text_edited_to_account_for_id
    # now safe to remove ticks if used for '**_Average:_**' and need removing
    # in typical handling.
    intrf_tbl_text = intrf_tbl_text.replace("`","")
    # remove the header because formatting that is a nightmare and will be just
    # easier to swap in one later
    end_of_header_text = "**  iNres ** | **  Surface Å2 **  \n"
    # In case of apparent edge case, 6nt8, the header ended with
    # ` **  iNres ** | **  Surface\nÅ2 **  \n` instead.
    if end_of_header_text not in intrf_tbl_text:
        intrf_tbl_text = intrf_tbl_text.replace(
            " **  iNres ** | **  Surface\nÅ2 **  \n",end_of_header_text)
    main_table_text = intrf_tbl_text.split(end_of_header_text,1)[1]
    # Adjust the table contents to match closer what would be obtained if copied 
    # from page by someone using a mouse to highlight the text. This way the 
    # input for the dataframe will be the same whether retrieved or provided as 
    # file made from the interface list page by a user.
    #---------------------------------------------------------------------------
    # Going from the html to text resuls in the table having the true rows 
    # broken up with one or two internal end of line signals and then one at the 
    # true end. 
    ''' WHAT IS IN THIS SMALL BLOCK COMMEBNT BELOW IS WHAT I HAD BEEN DOING 
    BEFORE REALIXING NOT ALWAYS EXACTLY TWO INTERNAL END OF LINE SIGNALS. 
    EXAMPLE IN LAST FEW ROWS OF 6nt8 WHERE CONTENTS OF ROW SHORT ENOUGH 
    APPARENTLY TO ONLY SPAN 2 LINES BECAUSE NUMBERS ON LEFT SIDE ALL VERY SHORT.
    #So this next step split on every end of line signal and stitch 
    # back together only using each third one so that it just leaves what would 
    # have been every third end of line before this step, 
    # based on https://stackoverflow.com/a/25978384/8508004
    spl = main_table_text.split("\n")
    raw_tbl_content = "\n".join(
        ["".join(spl[i:i+3]) for i in range(0,len(spl),3)])
    '''
    # Now going to count the columns in the raw state and remove line endings 
    # that won't correspond to last column. I think I had hesitated doing this 
    # earlier because I wasn't sure I had sampled a lot to know I had full 
    # understanding of the number of columns and I thought true rows spanned 3 
    # lines.
    raw_column_num = 18
    # Preparation for removing the 'internal' line endings:
    # The '**_Average:_**' lines though are a problem for the approach where 
    # remove line endings that don't correspond to last column and so going to 
    # add in correct number of `|` and spaces to the left of '**_Average:_**' so 
    # those have same number of columns.
    spacing_needed_b4_average = 11
    # account for symmetry columns in 'spacing_needed_b4_average' if have
    if 'Symmetry op-n' in intrf_tbl_text:
            spacing_needed_b4_average += 2
    correct_Avg_text = ' |' *spacing_needed_b4_average + '**_Average:_**'
    main_table_text = main_table_text.replace(
        '**_Average:_**', correct_Avg_text)
    # Adjust 'raw_column_num' to account for 'Average' rows that have 'Id' 
    # column or for 'Symmetry' columns
    if '**_Average:_**' in intrf_tbl_text:
        raw_column_num += 1
    if 'Symmetry op-n' in intrf_tbl_text:
        raw_column_num += 2
    # Now should be ready to remove the 'internal' line endings. Doing that by
    # iterating on the elements from splitting at '|' and making a new list of
    # those elements where line endings are removed unless they correspond to 
    # being in the last column.
    collected_split_parts_without_internal_line_endings = []
    correction_value = 0 # this will be use to add in an additional column count 
    # for each end of row encountered since the end of the actual row line doesn't
    # have a `|` on the right side like all the other columns. So the end of each
    # row, other than the last, should actually count as two columns. Otherwise, 
    # `indx+1`, which is meant to mirror the column count in total, continually 
    # gets more and more off with each row beyond the first actual row.
    for indx,split_content in enumerate(main_table_text.split("|")):
        if ((indx+1)+correction_value) % raw_column_num == 0:
            # leave any line ending as this should be a 'last' column. Unless 
            # there is the rare case where there are two line endings like I 
            # encountered in a row for 1rpn of `'\n 0.000   \n 5  ' or for 6agb 
            # of `' \n0.000   \n 2  '` or several for for 6agb like
            # `'  0.000\n  \n 14  '` caused by an internal end of line falling 
            # or in fact sometimes multiples end of lines falling in among the 
            # ONE that is the actual ending. In such a case I need to delete all
            # the line endings except the one after the first number.
            if split_content.count("\n") > 1:
                split_content_simplifying = split_content.replace("\n","")
                # now that all end of line characters are removed, while keeping 
                # all additional content, put an end of line character after the 
                # first content that isn't a space and join everything back 
                # together
                # Identify first element that isn't a space
                first_value = ""
                for x in split_content_simplifying.split():
                    if x:
                        first_value = x
                        break
                # now break it it apart on that 'first_value' and put it back
                # together putting an end of line character after that 
                # first_value
                spl = split_content_simplifying.split(first_value,1)
                split_content_simplified = spl[0] + first_value+"\n"+spl[1]
                collected_split_parts_without_internal_line_endings.append(
                    split_content_simplified)
            else:
                collected_split_parts_without_internal_line_endings.append(
                    split_content)
            correction_value += 1 #Because each `split_content` that corresponds
            # to the end of a row, except the very last of the entire table, 
            # actually corresponds to two columns in total.
        else:
            # delete the line ending as it is 'internal'
            collected_split_parts_without_internal_line_endings.append(
                split_content.replace("\n",""))
    # With 'internal' line endings removed put the list back together to have 
    # the '|' that indicate column boundaries in the table from the interface 
    # data page retrieved as html.
    raw_tbl_content = "|".join(
        collected_split_parts_without_internal_line_endings)
    # Change delimiter to tabs, not '|', so that it will resemble closely what I
    # saw  when I copied text directly from web page by highlighting with mouse
    # and pasting elsewhere. This way can read data later with same processing 
    # steps whether directly copied from webpage or if retrieved via 
    # http://www.ebi.ac.uk/pdbe/pisa/cgi-bin/piserver
    tab_sep_main_table_part = raw_tbl_content.replace("|","\t")
    # Put the header back. There seems to be a variety of headers. At least 
    # four that I've found now. For the 'main' two: there is
    # the header like the interface list report page for 6agb has, which I 
    # suspect is tpyical for cyro-EMs. Then there is also an expanded header 
    # that has two additional columns 'Symmetry op-n' & 'Sym.ID' in the middle 
    # section of reports for PDB entries like 4gfg, which I suspect is typical 
    # for crystal structures.
    # The third and fourth I recently found are one with additional 'Id' column 
    # as well as two additional columns 'Symmetry op-n' & 'Sym.ID' and then one
    # with just an additonal 'Id' column. The one I found first has the 
    # two additional columns 'Symmetry op-n' & 'Sym.ID' and ALSO starts out with 
    # 'Id' before 'Row #'' like the interface list report pages for 1trn & 1rpn. 
    # Seem Cryo-EM structures can gave the 'Id' column too, example 6nt8. Seems 
    # when you have the same chains also in another conformation, for example in 
    # tetramer of 6nt8. 
    # The other tell-tale characteristic of these ones with 'Id' in the columns 
    # is that they have rows with 'Average' that need special handling, some of
    # which has already been done above.
    correct_header = replacement_header 
    if 'Symmetry op-n' in intrf_tbl_text:
        correct_header = repl_header_with_sym
    if '**_Average:_**' in intrf_tbl_text:
        correct_header = ' Id   ' + correct_header[1:] # fix header to add 'Id'
    rebuilt_int_tbl_text = correct_header + "\n"+ tab_sep_main_table_part
    # Save the produced text as a file 
    with open(data_input_file_name, 'w') as output_file:
        output_file.write(rebuilt_int_tbl_text)
    sv_string = ("[bold bright_cyan]Extracted interface list data saved as "
        "the file '{}'".format(data_input_file_name))
    sv_string = ("Extracted interface list data saved as the file "
        "'{}'".format(data_input_file_name))
    console.print(sv_string,style="bold red on white")
    #print_separator_lines_to_console(1,skip=2) # moved line adding

def handle_pickling_the_dataframe(df, pickle_df, pdb_code, df_save_as_name):
    '''
    Was at end but moved to a function because will be used when 'empty' data
    provided where no interaction occurs.
    '''
    if pickle_df == False:
        '''
        sys.stderr.write("\n\nA dataframe of the data "
        "was not stored for use\nelsewhere "
        "because `no_pickling` was specified.")
        '''
        nsdf_string = ("A dataframe of the data "
        "was not stored for use elsewhere "
        "because `no_pickling` was specified.")
        console.print(nsdf_string,style="bold red on white")
    else:
        df_save_as_name = pdb_code + "_"+ df_save_as_name
        df.to_pickle(df_save_as_name )
        # Let user know
        '''
        sys.stderr.write("\n\nA dataframe of the data "
        "has been saved as a file\nin a manner where other "
        "Python programs can access it (pickled form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}'".format(df_save_as_name ))
        '''
        hpdf_string = ("A dataframe of the data "
        "has been saved as a file in a manner where other "
        "Python programs can access it (pickled form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}'".format(df_save_as_name ))
        console.print(hpdf_string,style="bold red on white")


def arrange_returning_the_dataframe_and_info(
    df,pdb_code_id,return_df,return_pdb_code):
    '''
    Was at end but moved to a function because will be used when 'empty' data
    provided where no interaction occurs.
    '''
    if return_df and return_pdb_code:
        '''
        sys.stderr.write("\n\nReturning both the PDB code identifier and a "
            "dataframe with the information as well.")
        '''
        rcndf_string = ("Returning both the PDB code identifier and a "
            "dataframe with the information as well.")
        console.print(rcndf_string,style="bold red on white")
        return pdb_code_id,df
    elif return_df:
        '''
        sys.stderr.write("\n\nReturning a dataframe with the information "
                "as well.")
        '''
        rdfo_string = ("Returning a dataframe with the information "
                "as well.")
        console.print(rdfo_string,style="bold red on white")
        return df
def endwrapup():
    '''
    Doesn't take anything or return anything.
    Just prints to console, but because need to call twice, trying to lessen
    repeating.
    '''
    console.rule(
        "[bold red]End of Storing & Wrapping-Up",
        style = "bold red on white")

def insert_position(position, list1, list2):
    '''
    takes two lists and places the second list into the first list at the 
    specified position.
    from https://stackoverflow.com/a/39542557/8508004
    '''
    return list1[:position] + list2 + list1[position:]


###--------------------------END OF HELPER FUNCTIONS---------------------------###
###--------------------------END OF HELPER FUNCTIONS---------------------------###

#*******************************************************************************
###------------------------'main' function of script---------------------------##

def pisa_interface_list_to_df(pdb_code, return_df = True, 
    pickle_df=True, return_pdb_code=False, adv_debugging=False):
    '''
    Main function of script. 
    PDBsum list of interactions to Pandas dataframe.
    Optionally also returns a dataframe of the data. 
    Optionally can also return the PDB identification code as well.
    Meant for use in a Jupyter notebook.

    Adapted from the main function in `pdbsum_prot_interactions_list_to_df.py`
    '''

    # Set rich to handle tracebacks
    #---------------------------------------------------------------------------
    # Set up traceback to be nice by using Will McGugan's rich & allow a debug 
    # setting that make error tracebacks more informative with display of 
    # local variables
    from rich.traceback import install
    if adv_debugging:
        install(show_locals=True) # so much better for debugging because in the 
        # traceback it reports local variables; however,imagine it may be 
        # overwheming to typical users. Maybe put this here as an option & ask 
        # users to toggle on if they report a particularly vexxing bug.
    else:
        install()

    # Determine if input data already saved as a file and retrieve, if not:
    #---------------------------------------------------------------------------
    # If retrieving, it will need to be formatted and saved as if it would be
    # provided.
    console.rule("[bold red]Input Preparation",style = "bold red on white")
    # check if pdb_code provided actually looks like an id for a pdb entry.
    # I'm going to think ahead and build in the future version they'll use, see
    # 'Future Plans for Expanded PDB Codes' at 
    # https://proteopedia.org/wiki/index.php/PDB_code
    # and https://www.wwpdb.org/news/news?year=2017#5910c8d8d3b1d333029d4ea8 ,
    # so 'pdb_00001abc' or the older 4 character alphanumeric
    good_pdb_code = False
    if len(pdb_code) == 4 and pdb_code.isalnum():
        good_pdb_code = True
    elif pdb_code.startswith("pdb_") and (len(pdb_code) == 12):
        if pdb_code[4:9].isnumeric() and pdb_code[9:12].isalnum():
            good_pdb_code = True
            npc_string = ("Oh! Expanded PDB Code! Hopeully this works at PDBe.")
            console.print(npc_string,style="bold red on white")
    if not good_pdb_code:
        bc_string = ("It doesn't look like you provided a valid PDB code?")
        console.print(bc_string,style="bold white on blue")
        console.rule(
        "[bold red]**EXITING ON INVALID PDB CODE ERROR**",
        style = "bold red on white")
        sys.exit(66)
    data_local = False # set-up a variable in case want to report
    data_input_file_name = pdb_code.lower() + suffix_for_input_data_file # if 
    # this isn't located in the working directory, it will get made. If the case 
    # doesn't match that is okay, but then `data_input_file_name` will then get
    # reassigned to match the one provided.

    # Scan current working directory for the input data. Allow it to be 
    # case-insensitive by using lowercase name of file, & then 
    # if it matches, adjust `data_input_file_name` to match the provided file 
    # name so that the case gets matched no matter what it is.
    for file in os.listdir("."):
        if fnmatch.fnmatch(file.lower(), data_input_file_name):
            data_input_file_name = file # switching to the name provided in case 
            # thename isn't all lower case as I made it bey default. This makes 
            # it so this is NOT case sensitive when a file is provided as long 
            # as the pattern matches.
            data_local = True # adjust variable that is used to monitor status
            use_string = ("File '{}' provided as source of interface "
                "data.".format(data_input_file_name))
            console.print(use_string,style="bold red on white")
            break # if encountered, for loop breaks without running the 'else'
    else:
        make_data_input_file_name(data_input_file_name)
    console.rule(
        "[bold red]End of Input Preparation",style = "bold red on white")


    
    # Prepare for getting necessary data by setting up column names:
    #---------------------------------------------------------------------------
    console.rule("[bold red]Dataframe Generation",style = "bold red on white")
    column_names = (['row #','dropHERE', 'Chain 1', 'Number_InterfacingAtoms1', 
        'Number_InterfacingResidues1', 'Surface area1', 'x',
        'Chain 2', 'Number_InterfacingAtoms2',
        'Number_InterfacingResidues2','Surface area2', 'Interface area', 
        'Solvation free energy gain', 'Solvation gain P-value', 
        'Interface Hydrogen bonds', 'Interface Salt Bridges',
        'Interface Disuflides','CSS'])
    # column naming for multiindex handling borrows from things worked out in `make_table_of_missing_residues_for_related_PDB_structures.py`
    # Get first five lines of the input file & see if need to add the symmetry 
    # columns.
    N = 6
    with open(data_input_file_name) as quickchk:
        top_few_lines_input = "".join([next(quickchk) for x in range(N)])# based 
        # on https://stackoverflow.com/a/1767589/8508004
    id_col_insert_pt = 0
    symmetry_cols_insert_pt = 8
    # with most I saw 'Id   ##   Structure 1', but with 6nt8 I saw at start of
    # top_few_lines_input 'Id   ##      Structure 1'. So instead of testing
    # explicitly for those 2 strings & not knowing if there  may be more 
    # variations decided to remove spaces from begining and test for that 
    # sequence.
    if 'Id' in top_few_lines_input[:14] and (
        top_few_lines_input[:26].split() == ['Id', '##', 'Structure', '1']):
        # add as columns     Id
        column_names = insert_position(
            id_col_insert_pt, column_names, ['Id'])
        symmetry_cols_insert_pt += 1 # want to insert them moved over 1 to allow
        # 'Id' column as first column now; this adjustment will be moot if don't 
        # have symmetry columns, and so no need to test
    if 'Symmetry op-n' in top_few_lines_input:
        # add as columns     Symmetry op-n   & Sym.ID
        column_names = insert_position(
            symmetry_cols_insert_pt, column_names, ['Symmetry op-n','Sym.ID'])
    column_names_list = column_names


    # Bring in the input data and make the dataframe:
    #---------------------------------------------------------------------------
    ir_string = ("Interactions data being read from "
        "{}...".format(data_input_file_name))
    console.print(ir_string,style="bold red on white")
    df = pd.read_csv(
        data_input_file_name, sep='\t',index_col=False , 
        skiprows =5, names = column_names_list) # brings in text of the table 
    # that startswith `## and ends before the buttons below that table on the 
    # PISA server Interfaces page.
    # Drop the column that got tagged with special names during bring in.
    #df = df.drop(['dropHERE','dropHEREb'],axis=1) # ended up that some of the 
    # second one I have dropping have info. Best kept.
    df = df.drop(['dropHERE'],axis=1)
    #symmetry_cols_insert_pt -= 2 # lower by two since dropping columns marked
    # with 'dropHERE' tag # see above for when it was two!!
    symmetry_cols_insert_pt -= 1 # lower by one since dropping column marked
    # with 'dropHERE' tag 
    # Improve on column headers by making multiindex:
    upper_level_list = [' ','Chain 1','Chain 1','Chain 1'
                    ,'Chain 1', 'x', 'Chain 2', 'Chain 2'
                   , 'Chain 2', 'Chain 2','Interface'
                   ,'Interface','Interface','Interface','Interface'
                   ,'Interface', 'Interface'] # based on 
    # https://stackoverflow.com/a/24225106/8508004
    #With multiindex, I can use duplicates of the bottom level column names
    # so I can now simplify column names
    column_names_simplified = (['row #','Chain label','Number_InterfacingAtoms', 
            'Number_InterfacingResidues', 'Surface (Å$^2$)', ' ', 
            'Chain label', 'Number_InterfacingAtoms',
            'Number_InterfacingResidues','Surface (Å$^2$)', 'Area (Å$^2$)', 
            'Solvation free energy gain', 
            'Solvation gain P-value', 'Hydrogen bonds', 'Salt Bridges',
            'Disuflides','CSS'])
    # superscript in column names based on https://stackoverflow.com/q/45291459/8508004
    # Add the extra 'Id' column, if needed. (See above for why this conditional 
    # test went from `if 'Id   ##   Structure 1' in top_few_lines_input` to more 
    # complex b/c of 6nt8)
    if 'Id' in top_few_lines_input[:14] and (
        top_few_lines_input[:26].split() == ['Id', '##', 'Structure', '1']):
        upper_level_list = insert_position(
            id_col_insert_pt, upper_level_list, [' '])
        column_names_simplified = insert_position(
            id_col_insert_pt, column_names_simplified, ['Id'])
    # Add the extra 'symmetry' columns, if needed.
    if 'Symmetry op-n' in top_few_lines_input:
        upper_level_list = insert_position(
            symmetry_cols_insert_pt, upper_level_list, ['Chain 2','Chain 2'])
        column_names_simplified = insert_position(
            symmetry_cols_insert_pt, column_names_simplified, ['SymOp','SymID'])
    cols = pd.MultiIndex.from_arrays([upper_level_list, column_names_simplified])
    df = df.set_axis(cols, axis=1, inplace=False)

    
    pdb_code_id = pdb_code.lower() #make it lower case for returning, if return 
    # of pdb code id opted for.

    

    # feedback
    #sys.stderr.write("Interactions data read and converted to a dataframe...")
    cr_string = ("Interactions data read and converted to a dataframe.")
    console.print(cr_string,style="bold red on white")
    console.rule(
        "[bold red]End of Dataframe Generation",style = "bold red on white")


    # Saving/Storing and Returning
    #---------------------------------------------------------------------------
    console.rule(
        "[bold red]Storing For Later Use & Wrapping-Up",
        style = "bold red on white")
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
    handle_pickling_the_dataframe(df, pickle_df,pdb_code, df_save_as_name)

    
    # Return dataframe and pdb code(options)
    #---------------------------------------------------------------------------
    if return_df:
        returned = arrange_returning_the_dataframe_and_info(
            df,pdb_code,return_df,return_pdb_code)
        endwrapup()
        return returned

    endwrapup()
    

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
    kwargs['adv_debugging'] = False #intended only for advanced 
    # debugging/development
    if adv_debugging:
        kwargs['adv_debugging'] = True #intended only for advanced 
    # debugging/development
    pisa_interface_list_to_df(pdb_code,**kwargs)
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
        Takes an alphanumeric accession id code for a PDB entry and gets the\
        list of chain interactions from PDBePISA, unless provided locally, & \
        brings the data into Python as a dataframe and \
        saves a file of that dataframe for use elsewhere. Optionally, it can \
        also return that dataframe for use inside a Jupyter notebook. \
        Meant to be a utility script for working \
        with PDBePISA and Python.\
        **** Script by Wayne Decatur   \
        (fomightez @ github) ***")
    parser.add_argument("pdb_code", help="The alphanumeric accession id code \
        for a PDB entry for which to format the corresponding PDBePISA \
        interactions list into a dataframe. The corresponding interface list \
        will be automatically retrieved from PDBePISA, unless you you already \
        have the copied text of the interface list. You can signal to the \
        script to use the provided copied text by naming it the accession \
        code followed by '{}', for example '4fgf{}', and placing \
        it in your working directory & then the local data in that file \
        will be used.".format(suffix_for_input_data_file, 
            suffix_for_input_data_file), metavar="PDB_CODE")
    parser.add_argument('-dfo', '--df_output', action='store', type=str, 
    default= df_save_as_name, help="OPTIONAL: Set file name for saving pickled \
    dataframe. If none provided, '{}' will be used. To force no dataframe to \
    be saved, enter `-dfo no_pickling` without quotes as output file \
    (ATYPICAL).".format(df_save_as_name))
    parser.add_argument("-ad", "--adv_debugging",help=
        "Optional flag intended only for advanced debugging/development.",
        action="store_true")



    #I would also like trigger help to display if no arguments provided because 
    # need at least one for url
    if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    pdb_code = args.pdb_code
    df_save_as_name = args.df_output
    adv_debugging = args.adv_debugging


    main()

#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
