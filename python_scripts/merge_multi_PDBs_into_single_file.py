#! /usr/bin/env python

# merge_multi_PDBs_into_single_file by Wayne Decatur
# ver 0.3
#
# fuse_pdbs function code from Claudia Millan Nebot
#
# To GET HELP/MANUAL, enter on command line:
# python merge_multi_PDBs_into_single_file.py --help
#
#*************************************************************************
# USES Python 2.7
#
# DEPENDENCIES:
# Biopython and other typical modules like argparse, os
#
# Purpose: Takes a directory containing structures in the PDB format and
# combines them all into a single PDB file with each structure as an individual
# model.
#
#
# v.0.1.
# basics done
# v.0.2.
# Made so the default numbering for first model is 1 and not zero. Since
# `model 0` has special meaning as select all models in Jmol as described at
#  http://www.bioinformatics.org/pipermail/molvis-list/2007q2/000427.html .
# v.0.3.
# Added a mechanism where you can specify an order of models within final file by
# putting a whole number after underscore in front of the `.pdb` suffix. If every
# PDB file in the directory follows that pattern, the ascending order of those
# numbers will be used to sequence the models in the produced file. Note: The
# specific number used after the underscore is disregarded when numbering the
# models; you still need to provide the initial number for the models if you want
# anything other than 1 and the numbering will be incremented automatically.
# For example, calling the program to run with
# `python merge_multi_PDBs_into_single_file.py test_folder`, if `test_folder`
# contains `1crn_3.pdb`, `1tup_5.pdb`, and `1ehz_7.pdb`, the final file will
# have three models numbered 1 through 3 and they will correspond to 1crn, 1tup,
# and 1ehz.
#
# To do:
# How do we add "End" to end of file but not in middle?
#
#
# TO RUN:
# For example, when in the directory containing the directory with the PDB files
# `DIRECTORYcontainingPDBs`, enter on the command line, the line
#-----------------------------------
# python merge_multi_PDBs_into_single_file.py DIRECTORYcontainingPDBs
#-----------------------------------
# to generate the file named'DIRECTORYcontainingPDBs.pdb' in your working
# directory.
#
# Meaning that you can point it at a directory and then it will process
# all the files ending in '.pdb' or '.PDB' in that folder.
#
#*************************************************************************












#*************************************************************************
#*************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###
import os
import sys
from stat import *
#from urllib import urlopen
import logging
import argparse
from argparse import RawTextHelpFormatter
from Bio.PDB import *

#DEBUG CONTROL
#comment line below to turn off debug print statements
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)





#argparser from http://docs.python.org/2/library/argparse.html#module-argparse and http://docs.python.org/2/howto/argparse.html#id1
parser = argparse.ArgumentParser(prog='merge_multi_PDBs_into_single_file.py',description="merge_multi_PDBs_into_single_file is a program that takes\nstructures in the PDB format and combines them all into\na single PDB file with each structure as an individual model.\n\nBy providing a whole number following the '--initial' flag when calling the program\nyou can specify any value for numbering first model in the sequence of models.\nIf nothing is provided, the first model will be 'mode 1' by default.\n\nYou can control the order of the models in final file by placing an underscore followed by a\nwhole number in front of the '.pdb' portion of the file names. This must be done to all PDB files\nand then the order of the numbers will be mirrored in the order in the final file. The\nactual numbers used are not regarded when numbering the models in the final file; they are only\nused to determine the sequence.\n \nWritten by Wayne Decatur --> Fomightez @ Github or Twitter. \n\n\nActual example what to enter on command line to run program:\npython merge_multi_PDBs_into_single_file DIRECTORYcontainingPDBs", formatter_class=RawTextHelpFormatter)
#learned how to control line breaks in description above from http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-the-help-text
#DANG THOUGH THE 'RawTextHelpFormatter' setting seems to apply to all the text then. Not really what I wanted.
parser.add_argument("Directory", help=
    "directory containing PDB files to merge into single file. REQUIRED.")
parser.add_argument("-i", "--initial", type=int,default=1,help=
    "If not to be 1, provide a whole number to assign first model.\n It will be incremented for each subsequent model.")
#I would also like trigger help to display if no arguments provided because need at least a directory
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()



###---------------------------HELPER FUNCTIONS---------------------------------###
def extract_ordering_number(filepath):
    '''
    extacts the number after an underscore in front of ".pdb" in filepath and
    returns it as an integer.
    '''
    extracted_string = filepath.split("_")[1][0:-4]
    try:
        return int(extracted_string)
    except ValueError:
        return None

def after_underscore_is_integer(filepath):
    '''
    returns true only if there is an integer after an underscore in front of
    ".pdb" at end of file path
    '''
    if "_" not in filepath:
        return False
    else:
        return True if extract_ordering_number(filepath) is int else False


def order_the_list_based_on_user_specifications(list_of_filepaths):
    '''
    function takes a list of filepaths and orders them based on the number after
    an underscore in front of ".pdb" in filepath.
    That list is then returned.
    '''
    return sorted(list_of_filepaths, key=extract_ordering_number)


def fuse_pdbs(list_of_filepaths,current_path, initial_model_number=1):
    '''
    Original function written by Claudia Millan Nebot. It has been adapted to
    enable different

    The function takes as input a list of filepaths for several individual PDB
    files and combines them into a single file that is saved as path_pdb, where
    the path portion of the name specifies the directory to save the file.

    This updated version of this function defaults to the initial model number
    being one to avoid it being zero since `model O` is used to select all models
    in the popular structure viewing tool Jmol, as described at
    http://www.bioinformatics.org/pipermail/molvis-list/2007q2/000427.html .
    The default can be changed though as an argument to the program.
    '''
    list_of_structures=[]
    parser=PDBParser()
    for pdb_file in list_of_filepaths:
        structure=parser.get_structure(pdb_file[:-4],pdb_file)
        list_of_structures.append(structure)
    main_structure=list_of_structures[0]
    for indx,structure in enumerate(list_of_structures):
        #print "Processing ",structure,"; it will be model #",str(initial_model_number + indx)
        sys.stderr.write("\nProcessing "+ str(structure) +"; it will be model #"+ str(initial_model_number + indx))
        model=structure[0]
        model.id=initial_model_number + indx
        model.serial_num=initial_model_number + indx
        # Next comparison is so the first structure doesn't get added again since
        # ohe first was assigned in order to make the `main_structure` above.
        if indx !=0:
            main_structure.add(model)
    #print Selection.unfold_entities(main_structure,'M')
    io=PDBIO()
    io.set_structure(main_structure)
    io.save(current_path,write_end=False)
    sys.stderr.write("\n\nThe PDB-formatted file "+current_path+" has been created.\n")

###--------------------------END OF HELPER FUNCTIONS---------------------------###






###----------------------MAIN PART OF SCRIPT--------------------------------###
current_path = str(args.Directory) + ".pdb"
list_of_filepaths_for_PDB_files = []
initial_number_for_model = args.initial

# If provided argument is a DIRECTORY loop through collecting information on
# each PDB file.
#from http://stackoverflow.com/questions/3204782/how-to-check-if-a-file-is-a-directory-or-regular-file-in-python
if os.path.isfile(args.Directory):
    sys.stderr.write("\n***ERROR ********************ERROR ***************** \n")
    sys.stderr.write("Oops! You only provided a single file.\n This program is for merging multiple structures PDB file format into one.\n This file already exists as a single file.")
    sys.stderr.write("***ERROR ********************ERROR ***************** \n \n")
elif os.path.isdir(args.Directory):
    for f in os.listdir(args.Directory):
        pathname = os.path.join(args.Directory, f)
        #FOR DEBUGGING
        logging.debug(pathname)
        mode = os.stat(pathname).st_mode
        if S_ISREG(mode) and pathname[-4:].upper() == ".PDB":
            # It's a PDB file, collect the path and file name info
            list_of_filepaths_for_PDB_files.append(pathname)


# Determine if pathnames specify any order. ###
# All PDB files need to follow the pattern and so check if all the names have an
# underscore and an interger in front of the '.pdb' portion of name.
# If so, then will never hit `break` of for loop and will sort the list based
# on the integer in front of the the `.pdb`.
# If any lack underscore or don't have an integer, for loop `break`s and
# script continues on to next block of code. ## This is similar to last example
# under `` at http://simeonvisser.com/posts/using-else-in-python.html
for filepath in list_of_filepaths_for_PDB_files:
    #if "_" not in filepath or not after_underscore_is_integer(filepath):
    if not after_underscore_is_integer(filepath):
        break
else:
    list_of_filepaths_for_PDB_files = order_the_list_based_on_user_specifications(
        list_of_filepaths_for_PDB_files)


#Now that the name and path info on each PDB file has been collected, and any
# possible order specified dtermined, extract the data from each and merge into one
fuse_pdbs(list_of_filepaths_for_PDB_files,current_path,initial_number_for_model)
