#! /usr/bin/env python

#SPARTAN08_Fixer_standlone by Wayne Decatur
#ver 0.7
#
#
# To GET HELP/MANUAL, enter on command line:
# python SPARTAN08_Fixer.py --help
#
#*************************************************************************
#USES Python 2.7
# Purpose: Takes a single chain built in Spartan '08 data and exported in
# so-called PDB format and fixes it so it is in proper PDB format for use
# in Jmol.
#
#
# v.0.6. added handling of residue number so never exceeds 9999
# v.0.68 added distinguishing prolines and valines as well as leucine from
# isoleucine. This feature relies on the CONECT records.
# v.06.9 added handling of histidine since Spartan order of atoms differs
# from PDB format.
# v.0.7 added argument for designating file to act on. Also added an
# optional argument to bypass asking user to enter anything and just go with
# default. Also sdded a way to set chain designation and from command line.
#
#
#
# TO RUN:
# For example, enter on the command line, the line
#-----------------------------------
# python SPARTAN08_Fixer.py FILEtoACTon.pdb
#-----------------------------------
# to send the output to the file named'FILEtoACTon_fixed.pdb'.
#
# Note that you can also point it at a directory and then it will process
# all the files ending in '.pdb' in that folder.
#
#*************************************************************************


##################################
#  USER ADJUSTABLE VALUES        #
Default_Chain_Designator = "A"
Default_Start_Residue = 1
##################################










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

#DEBUG CONTROL
#comment line below to turn off debug print statements
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)



def InsureChainDesignatorSingleChar(ChrEntered):
    if ChrEntered != "NoneDesignatedOnCommandLine":
        return ChrEntered[0]
    else:
        return ChrEntered #will be "NoneDesignatedOnCommandLine"

def CheckIfInRange(value):
    if value != "NotDesignatedOnCommandLine":
        number = int(value)
        if number < 1 or number > 9999:
             raise argparse.ArgumentTypeError("%s is invalid as a start number.\nUse a number between 1 and 9999 for StartNo." % value)
        if number > 9999:
             raise argparse.ArgumentTypeError("%s is invalid as a start number.\nResidue numbers cannot be more than 9999.\nEnter a number lower than (or equal to) 9999 for StartNo." % value)
        return number
    else:
        return value #will be "NotDesignatedOnCommandLine"

#argparser from http://docs.python.org/2/library/argparse.html#module-argparse and http://docs.python.org/2/howto/argparse.html#id1
parser = argparse.ArgumentParser(prog='SPARTAN08_Fixer.py',description="SPARTAN08_Fixer is a program that fixes single chain Spartan'08 output\nfiles in so-called PDB format, converting them to be true PDB format.\nThe fixed files can then easily be used in Jmol.\n\nWritten by Wayne Decatur --> Fomightez @ Github or Twitter. \n\nPDB format specification info:\nhttp://www.wwpdb.org/docs.html and http://deposit.rcsb.org/adit/docs/pdb_atom_format.html\n \n \n \nActual example what to enter on command line to run program:\npython SPARTAN_FIXER input_file.pdb\n \n ", formatter_class=RawTextHelpFormatter)
#learned how to control line breaks in description above from http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-the-help-text
#DANG THOUGH THE 'RawTextHelpFormatter' setting seems to apply to all the text then. Not really what I wanted.
parser.add_argument("InputData", help="name of Spartan data file that will be fixed. REQUIRED.\nFiles entered this way do not have any requirement for specific extension as long\nthey are SPARTAN so-called PDB formatted-data.\n\nThe required input data can also be a group of files ending in '.pdb' (case does not matter)\ncontained within a folder. In that case put the folder as the input data.")
parser.add_argument("--ChainDesig", metavar='X', default="NoneDesignatedOnCommandLine", help="Enter in place of 'X' an alphanumeric character\nto use as chain designation, or enter when prompted",
    type=InsureChainDesignatorSingleChar) #error catch from http://stackoverflow.com/questions/14117415/using-argparse-allow-only-positive-integers
parser.add_argument("--StartNo", metavar='Y', default="NotDesignatedOnCommandLine", help="Enter in place of 'Y' a number in the range 1 to 9999\nto be the first residue sequence number\nfor the output, or enter when prompted",
    type=CheckIfInRange) #error catch from http://stackoverflow.com/questions/14117415/using-argparse-allow-only-positive-integers
parser.add_argument("-a", "--auto", help="Run without further prompts for user action, using chain\ndesignation and starting residue on command line or\nthe defaults of '"+Default_Chain_Designator+"' and '"+str(Default_Start_Residue)+"', respectively, for\nthose values if none provided.",action="store_true")
#I would also like trigger help to display if no arguments provided because need at least input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()







old_raw_input = raw_input #For REDIRECTing raw_input prompt from stdout to stderr so it won't show in output file (and while I use redirect in development), from http://stackoverflow.com/questions/21202403/how-to-redirect-the-raw-input-to-stderr-not-stdout
def raw_input(*args):
    old_stdout = sys.stdout
    try:
        sys.stdout = sys.stderr
        return old_raw_input(*args)
    finally:
        sys.stdout = old_stdout








###-----ACQUIRE NEEDED INFORMATION FROM USER IF NOT PROVIDED ON COMMAND LINE----###
chain_collection_preamble = """The program discards all hydrogens. You can add them back in later in Jmol with the command 'calculate hydrogens'

The program handles one chain at a time.
If you have multiple chains, you'll have to do them individually first and restore them as one file via a text editor.

You can designate any alphanumeric character you wish to be the chain identifier.(Capital 'A' is always a good choice, if in doubt.)
"""

if args.auto and (args.ChainDesig == "NoneDesignatedOnCommandLine") and (args.StartNo == "NotDesignatedOnCommandLine"):
    Chain_ID_user_wants = Default_Chain_Designator
    Number_to_start_numbering_with_from_user = Default_Start_Residue
else:
    if args.auto and args.ChainDesig == "NoneDesignatedOnCommandLine":
        Chain_ID_user_wants = Default_Chain_Designator
    elif args.ChainDesig == "NoneDesignatedOnCommandLine":
        Chain_ID_user_wants = "nnnn"
        while Chain_ID_user_wants == "nnnn" or (len(Chain_ID_user_wants) > 1 or len(Chain_ID_user_wants) < 0) :
            try:
                Chain_ID_user_wants = str(raw_input(chain_collection_preamble + "Please enter the character now: "))
                #break   - put a break if you don't won't it to continue the while if any valid number is put - in this case I want it commented out because I want a new value besides the default
            except ValueError:
                #print "Oops!  That was not a valid character.  Try again..."
                sys.stderr.write("\nOops!  That was not a valid character.  Try again...\n")
    else:
        Chain_ID_user_wants = args.ChainDesig
    if args.auto and args.StartNo == "NotDesignatedOnCommandLine":
        Number_to_start_numbering_with_from_user = Default_Start_Residue
    elif args.StartNo == "NotDesignatedOnCommandLine":
        Number_to_start_numbering_with_from_user = 999999999
        while Number_to_start_numbering_with_from_user == 999999999 or (Number_to_start_numbering_with_from_user > 9999 or Number_to_start_numbering_with_from_user < 1) :
            try:
                Number_to_start_numbering_with_from_user = int(raw_input("Please enter a number in the range 1 to 9999 (1 being the most common choice) to be the first residue sequence number for the output: "))
                #break   - put a break if you don't won't it to continue the while if any valid number is put - in this case I want it commented out because I want a new value besides the default
            except ValueError:
                #print "Oops!  That was not a valid option.  Try again..."
                sys.stderr.write("\nOops!  That was not a valid option.  Try again...\n")
    else:
        Number_to_start_numbering_with_from_user = args.StartNo
###--------------------------END OF INFO ACQUISITION---------------------------###










###----DEFINING FUNCTION CALL AND SETTING STAGE FOR MAIN PART OF SCRIPT--------###
def THE_MAIN_FUNCTION(InputFile,Chain_ID_user_wants,Number_to_start_numbering_with_from_user):
    def AtomNameIdentity(atom_line):
        # see http://deposit.rcsb.org/adit/docs/pdb_atom_format.html for slice 12:17 info; plus http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/strings3.html#string-slices
        return (atom_line[12:17]).strip()  # strip is to leave just the text and no spaces in order to make comparisons easier

    def AtomSerialNo(line_input):
        # see http://deposit.rcsb.org/adit/docs/pdb_atom_format.html for slice 12:17 info; plus http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/strings3.html#string-slices
        return (line_input[6:12]).strip()  # strip is to leave just the text and no spaces in order to make comparisons easier

    def AtomSerialConvertedToElement(Connected_atom_no):
        return AtomSerialAndElements_dict.get(Connected_atom_no, "NotAnAtom")

    def VerifyResidueNameForAmbiguousPatterns(amino_acid_abbrev):
        if amino_acid_abbrev == "VAL":
            StartingNitrogen_Atom_Orig_Serial_No = List_of_Atom_Lines_From_Spartan_Data[Reset_Atom_No-1][6:12].strip()
            StartingNitrogenConectPattern = AtomNo_and_ConnectedAtoms_dict[StartingNitrogen_Atom_Orig_Serial_No] #first nitrogen of
            # residue can distinguish proline vs valine. Fortunately List_of_Atom_Lines_From_Spartan_Data[Reset_Atom_No-1]
            # happens to be that atom because nitrogen atom first in residue and  current value of 'Reset_Atom_No'
            # corresponds to the current and first atom but need '-1' because list begins at zero index wheres Atom number
            # in PDB file begins at 1. Not using string count here because it should match this pattern precisely or
            # is not nitrogen of proline. No hydrogen should be involved here, unlike Cbeta of isoleucine in code below.
            if StartingNitrogenConectPattern == "CCC":
                return "PRO"
            else:
                return "VAL"
        if amino_acid_abbrev == "LEU":
            CarbonBeta_Atom_Orig_Serial_No = List_of_Atom_Lines_From_Spartan_Data[(Reset_Atom_No-1)+4][6:12].strip() #Because
            # of start at index 1 for atoms vs zero for a list index, 'Reset_Atom_No-1' is starting nitrogen and so atom
            # fourth after that should be Carbon beta of that residue since relative first nitrogen
            CarbonBetaConectPattern = AtomNo_and_ConnectedAtoms_dict[CarbonBeta_Atom_Orig_Serial_No] #carbon beta of the residue
            # can be used to distinguish ISOLEUCINE FROM LEUCINE BECAUSE ISOLEUCINE Carbon beta will be onected to
            # three carbons, whereas leucine carbon beta only connects to two. Easier to use string count here
            # in code check because that rees me from any concern of where it is placed in CONECT record.
            if CarbonBetaConectPattern.count('C') == 3:
                return "ILE"
            else:
                return "LEU"


    def Print_Lines_Of_Output_List(a_list,OutputFile):
        #from http://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python, see MARCOG's answer and mgold's comments
        # this lets me simply develop with output going to stdout which I can redirect from command line
        # but when I want to add file handing to make nicer user experience just need to add the next line
        # and close stream. SEE ORIGINAL IN v.6.9 for development one
        stdout=sys.stdout
        sys.stdout = open(OutputFile, 'w')
        for the_line in a_list:
            print the_line
        sys.stdout.close()
        sys.stdout = stdout
    #OLD VERSION OF Print_Lines_Of_Output_List WITHOUT FILE HANDLING; OLF VERSION WAS GOOD FOR EASY REDIRECT IN DEVELOPMENT
    '''
    def Print_Lines_Of_Output_List(a_list):
    for the_line in a_list:
        print the_line
    '''

    def Remove_Last_Instance_Of_Element(old_string,element_to_remove):
        idx = old_string.rfind(element_to_remove)
        new_string = old_string[:idx] + old_string[idx+1:] #from http://stackoverflow.com/questions/14496006/finding-last-occurence-of-substring-in-string-replacing-that
        return new_string
    def Remove_Possible_Cterminal_Oxygen(ye_olde_string):
        idx = ye_olde_string.find("OO") + 1
        the_newer_string = ye_olde_string[:idx] + ye_olde_string[idx+1:] #from http://stackoverflow.com/questions/14496006/finding-last-occurence-of-substring-in-string-replacing-that
        return the_newer_string
    def Atom_serial_number_spaced(the_number):
        return (str(the_number)).rjust(5)   #from http://www.tutorialspoint.com/python/string_rjust.htm
    def Atom_Name_spaced(a):
        return " " + a.ljust(3)
    def Element_symbol_spaced(chractr):
        return chractr.rjust(2)
    def Residue_sequence_number_spaced(Res_Seq_No):
        return (str(Res_Seq_No)).rjust(4)   #from http://www.tutorialspoint.com/python/string_rjust.htm


    def AddFixedFileIndication(FileName):
        TheFileNameMainPart, fileExtension = os.path.splitext(FileName) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
        if '.' in FileName:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
            return TheFileNameMainPart+"_fixed"+fileExtension
        else:
            return FileName+"_fixed"





    ###---------------------------DICTIONARIES---------------------------------###
    #Dictionary of amino acid atom patterns made using code 'For Making Dictionary of Amino Acid Patterns.py' and
    # regex from a list of copied amino acids from PDBS, see 'Example of all amino acids from PDB files.txt'
    # THEN ALTERED FOR HISTIDINE! (see after dictionary below)
    Amino_Acids_Pattern_Dict = {
    'NCCOC': 'Alanine (Ala)',
    'NCCOCCCNCNN': 'Arginine (Arg)',
    'NCCOCCON': 'Asparagine (Asn)',
    'NCCOCCOO': 'Aspartic acid  (Asp)',
    'NCCOCS': 'Cysteine (Cys)',
    'NCCOCCCOO': 'Glutamic acid (Glu)',
    'NCCOCCCON': 'Glutamine (Gln)',
    'NCCO': 'Glycine (Gly)',
    'NCCOCCCNCN': 'Histidine (His)',
    'NCCOCCCC': 'Isoleucine (Ile)',
    'NCCOCCCC': 'Leucine (Leu)',
    'NCCOCCCCN': 'Lysine (Lys)',
    'NCCOCCSC': 'Methionine (Met)',
    'NCCOCCCCCCC': 'Phenylalanine (Phe)',
    'NCCOCCC': 'Proline (Pro)',
    'NCCOCO': 'Serine (Ser)',
    'NCCOCOC': 'Threonine (Thr)',
    'NCCOCCCCNCCCCC': 'Tryptophan (Trp)',
    'NCCOCCCCCCCO': 'Tyrosine (Tyr)',
    'NCCOCCC': 'Valine (Val)'
     }
     #NOTE THAT THE HISTIDINE PATTERN IS UNIQUE TO SPARTAN OUTPUT. IT IS
     #actually 'NCCOCCNCCN': 'Histidine (His)' FOR ACTUAL PDB FLES!!!

    #Dictionary of proper atoms in amino acid made using code
    #'For Making Dictionary of Proper Atom Names for PDB amino acids.py' and
    # regex from a list of copied amino acids from PDBS, see 'Example of all amino acids from PDB files.txt'
    Atom_Name_Dict = {
    'Alanine (Ala)': ['N', 'CA', 'C', 'O', 'CB'],
    'Arginine (Arg)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'],
    'Asparagine (Asn)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'ND2'],
    'Aspartic acid  (Asp)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'OD2'],
    'Cysteine (Cys)': ['N', 'CA', 'C', 'O', 'CB', 'SG'],
    'Glutamic acid (Glu)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'OE1', 'OE2'],
    'Glutamine (Gln)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'OE1', 'NE2'],
    'Glycine (Gly)': ['N', 'CA', 'C', 'O'],
    'Histidine (His)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'ND1', 'CD2', 'CE1', 'NE2'],
    'Isoleucine (Ile)': ['N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2', 'CD1'],
    'Leucine (Leu)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2'],
    'Lysine (Lys)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'CE', 'NZ'],
    'Methionine (Met)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'SD', 'CE'],
    'Phenylalanine (Phe)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'],
    'Proline (Pro)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD'],
    'Serine (Ser)': ['N', 'CA', 'C', 'O', 'CB', 'OG'],
    'Threonine (Thr)': ['N', 'CA', 'C', 'O', 'CB', 'OG1', 'CG2'],
    'Tryptophan (Trp)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'],
    'Tyrosine (Tyr)': ['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'OH'],
    'Valine (Val)': ['N', 'CA', 'C', 'O', 'CB', 'CG1', 'CG2']
    }
    ###-----------------------END OF DICTIONARIES---------------------------------###








    ###-----------------Actual Main function of script---------------------------###
    ###---------------GET SPARTAN DATA AND PREP BASED ON IT----------------------###
    #Next bring in the Spartan file data:
    #   -at the same time, collect any header before the atom lines, preparing to be in Output text
    #   - filter out hydrogen lines
    #   - and make a list of just each (non-hydrogen) elements, (which is erroneously in the atom name position in the SPARTAN'08 so-called PDB format.)
    #   - make a list of the atom lines
    Past_Header = False
    pertinent_record_line_no = 0
    List_To_Make_Fixed_Spartan_Output_From = []
    List_of_Atom_Lines_From_Spartan_Data = []
    List_of_Elements_From_Atom_Lines = []
    List_o_CONECT_record_impt_parts = []
    List_of_Orig_Atom_Serial_Nos = []
    List_of_AllElements_From_Lines =[]
    spartan_file_stream = open(InputFile, "r")
    for line in spartan_file_stream:
        line = line.strip ();#this way I have better control of ends ultimately becaue I know there isn't any unless I add
        words = line.split()
        #print line
        #Need CONECT records for deciperhing proline vs valine and leucine vs isoleucine
        if words[0] == "CONECT":
            List_o_CONECT_record_impt_parts.append(line[7:].strip())
        if not Past_Header and words[0] == "HETATM":
            Past_Header = True
        if not Past_Header:
            if line[0:18] == "REMARK Spartan '08":
                List_To_Make_Fixed_Spartan_Output_From.append(line + "; true PDB formatting by SPARTAN08_Fixer")
            else:
                List_To_Make_Fixed_Spartan_Output_From.append(line)
        if Past_Header and words[0] == "HETATM":
            List_of_AllElements_From_Lines.append(AtomNameIdentity(line)) #used to
            # make dictionary of original atom numbers and associated elements for use in resolving the
            #four amino acids for which the CONECT patterns are relied on
            List_of_Orig_Atom_Serial_Nos.append(AtomSerialNo(line)) #used to make dictionary of
            #original atom numbers and associated elements for use in resolving the
            #four amino acids for which the CONECT patterns are utilized.

            #Want to filter out lines that are hydrogens from main atom handling set.
            if (AtomNameIdentity(line)) != "H":
                List_of_Atom_Lines_From_Spartan_Data.append(line)
                List_of_Elements_From_Atom_Lines.append(AtomNameIdentity(line)) #used
                #to make list of amino acid patterns

    spartan_file_stream.close()
    sys.stderr.write("The Spartan data file "+InputFile+" has been read in and processed.\n")
    OutputFile = AddFixedFileIndication(InputFile)

    #make the list of elements as a single string
    String_of_Atom_Elements_in_order = ''.join(List_of_Elements_From_Atom_Lines) #from http://stackoverflow.com/questions/4481724/convert-a-list-of-characters-into-a-string


    #FOR DEBUGGING
    #logging.debug(List_To_Make_Fixed_Spartan_Output_From)
    #logging.debug(List_of_Elements_From_Atom_Lines)
    #logging.debug(String_of_Atom_Elements_in_order)
    #logging.debug(List_of_Orig_Atom_Serial_Nos)
    #logging.debug(List_o_CONECT_record_impt_parts)
    #logging.debug(List_of_AllElements_From_Lines)





    ###---------Preparation for Dealing with Residues That Are Ambiguous From Patterns Alone---------###
    #for ultimately dealing with CONECT records, make a dictionary of original spartan
    # data atom serial numbers (keys) and the element corresponding to the atom (values)
    AtomSerialAndElements_dict = dict(zip(List_of_Orig_Atom_Serial_Nos,List_of_AllElements_From_Lines))
    #FOR DEBUGGING
    #logging.debug(AtomSerialAndElements_dict)


    #Build a dictionary of the CONECT records. Key will be the atom serial number and the values will
    # be the elements that are linked to that atom
    #approach will be to make a list of key and values and then zip it into a dictionary;
    # the atom serial numbers will be easy as it is the first word in the collected part
    # of the CONECT record; the other parts will require determining the corresponding
    # elements from the AtomSerialAndElements_dict
    list_o_conect_record_first_atomNo= []
    list_o_CONECT_elements_after_first= []
    for conect_rec in List_o_CONECT_record_impt_parts:
        conected_atom_nos = conect_rec.split()
        list_o_conect_record_first_atomNo.append(conected_atom_nos[0])
        conected_elements = []
        for atomNo_conected in conected_atom_nos[1:]:
            ElementCorrespondingToInquiry = AtomSerialConvertedToElement(atomNo_conected)
            if ElementCorrespondingToInquiry != "NotAnAtom":
                conected_elements.append(ElementCorrespondingToInquiry)
        list_o_CONECT_elements_after_first.append(''.join(conected_elements))
    AtomNo_and_ConnectedAtoms_dict = dict(zip(list_o_conect_record_first_atomNo,list_o_CONECT_elements_after_first))
    #FOR DEBUGGING
    #logging.debug(AtomNo_and_ConnectedAtoms_dict)








    ###-----------EXTRACT COMPONENTS THAT WILL COMPRISE NEW ATOM RECORDS-----------------###
    #Begin to prep for going though lines of atom records and making them fit standard PDB format as defined at http://deposit.rcsb.org/adit/docs/pdb_atom_format.html and http://www.wwpdb.org/documentation/format33/sect9.html#ATOM
    List_for_Fixed_Atom_Records_Section = []
    CTerminalOxygenNeedsHandling = False
    Problem_Identifying_Cterminal_residue = False
    Problem_Identifying_an_internal_residue = False
    ApparentlyNoCTerminalOxygen = False
    Fixed_Start_Number = False
    Residue_Sequence_Number = Number_to_start_numbering_with_from_user
    Reset_Atom_No = 1

    #split the String_of_Atom_Elements_in_order at each amino acid by recognizing N-C-C-O series, i.e., the peptide backbonem, and splitting where NCCO starts
    #BASED ON NEXT LINE!!!
    List_Of_Amino_Acid_Patterns_In_Order = filter(None, ",NCCO".join(String_of_Atom_Elements_in_order.split('NCCO')).split(',')) # from http://www.gossamer-threads.com/lists/python/python/71964 and http://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings; the filter removes the blank one from the beginning of '  print ",NCCO".join(str.split('NCCO')).split(',')   '
    # WOW, I WISH I HAD FOUND THE ABOVE COMBINATION OF SOLUTION EARLIER BECAUSE I HAD OTHER PLACES I COULD HAVE USED THESE, ESPECIALLY 'FILTER'

    #For DEBUGGING
    logging.debug(List_Of_Amino_Acid_Patterns_In_Order)

    #Need length of the List_Of_Amino_Acid_Patterns_In_Order to use as presumed
    # number of residues to make sure won't go over 9999 since PDB format only
    # allows that
    Presumed_Length_of_Chain = len(List_Of_Amino_Acid_Patterns_In_Order)
    Upper_limit_PDB_residueNos = 9999
    #then correct if residue number plus what user wanted as start will be over 9999
    if Number_to_start_numbering_with_from_user + Presumed_Length_of_Chain > Upper_limit_PDB_residueNos:
        Residue_Sequence_Number = (Upper_limit_PDB_residueNos - Presumed_Length_of_Chain) + 1
        Fixed_Start_Number = True



    #Get residue name (as three letter code)  [I kept full name plus the three letter code in values for dictionary
    # of patterns just for clarity and since source text had it.]
    #Match each amino acid to pattern in dictionary of atom patterns and get the residue name abbreviation
    #enumerate from http://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops , enumerate allows me to get current position in list for using
    for the_index, amino_acid_atom_pattern in enumerate(List_Of_Amino_Acid_Patterns_In_Order):
        AminoAcidInfo = Amino_Acids_Pattern_Dict.get(amino_acid_atom_pattern, "UNKNOWN (UNK)") #'.get' method allows a default value to be returned if no match

        # if no "UNKNOWN" amino acid patterns then  CTerminalOxygenNeedsHandling remains false

        #If pattern didn't match, it may be because it is terminal residue and has C-terminal oxygen that doesn't match pattern
        #so remove the putative C-terminal oxygen and then see if matches. Note this assumes safe to try this because nothing
        #will match unless last amino acid, but I have not verified this 100% (ca. 99% it won't). And allows handling
        #internal issues with same part of code
        if AminoAcidInfo == "UNKNOWN (UNK)":
            amino_acid_atom_pattern_minus_last_oxygen = Remove_Possible_Cterminal_Oxygen(amino_acid_atom_pattern)
            #print amino_acid_atom_pattern_minus_last_oxygen
            AminoAcidInfo = Amino_Acids_Pattern_Dict.get(amino_acid_atom_pattern_minus_last_oxygen, "UNKNOWN (UNK)")
            #print AminoAcidInfo
            #if still unknown set a varibble that notices this
            # and note if it is at end of chain or not that doesn't match
            if  AminoAcidInfo == "UNKNOWN (UNK)":
                #check if on last amino acid in chain
                if the_index == (len(List_Of_Amino_Acid_Patterns_In_Order) - 1):
                    Problem_Identifying_Cterminal_residue = True
                else:
                    Problem_Identifying_an_internal_residue = True
            else:
                #means CARBOXY TERMINAL OXYGEN apparently handled so note and then finish handling later
                #SHOULD VERIFY BY LOOKING AT KNOWN PDB FILE C-TERMINI THAT NO C-TERMINUS LOOKS LIKE A NATURAL AMINO ACID WITHOUT ALTERING!!!
                 CTerminalOxygenNeedsHandling = True


        Residue_name = AminoAcidInfo[AminoAcidInfo.find("(")+1:AminoAcidInfo.find(")")].upper() #want as uppercase to match PDB format.
        #on line above part like str[str.find("(")+1:str.find(")")] deals with grabbing text in between
        # the parantheses or the three letter code of the amino acid.

        #Four amino acids cannot be distinguished based on Pattern Alone and
        # so need an additional check for those. Makes sene to do at end of this
        # section and not earlier so can do once.
        # BOTH VALINE and PROLINE = 'VAL' from Pattern dictionary
        # Both ISOLEUCINE and LEUCINE = 'LEU' from Pattern dicionary
        if Residue_name in  ("VAL","LEU"):
            logging.debug("Verify triggered")
            Residue_name = VerifyResidueNameForAmbiguousPatterns(Residue_name)


        #Hisitidine atoms in Spartan output are ordered differently than true
        # PDB format.
        #The Amino_Acids_Pattern_Dict has already been altered to recognize it
        # as the residue in input from Spartan data.
        #Now also need to rearrange atoms for this residue in list extracted
        # for PDB file so atoms in correct order. This can be done by simply
        # switching order of nitrogen Nd1 and carbon Cd2 in the Spartan data.
        #The switch will make it match PDB format and it will be assigned the
        # correct atoms in the subsequent match when 'The_Proper_Atom_Name' assigned.
        if Residue_name == "HIS":
            List_of_Atom_Lines_From_Spartan_Data[(Reset_Atom_No-1)+6],List_of_Atom_Lines_From_Spartan_Data[(Reset_Atom_No-1)+7] = List_of_Atom_Lines_From_Spartan_Data[(Reset_Atom_No-1)+7], List_of_Atom_Lines_From_Spartan_Data[(Reset_Atom_No-1)+6]
            #For DEBUGGING
            logging.debug("Histidine recognized and order of Cd2 and Nd1 atoms swapped so they will match true PDB atom order.")





        #FOR DEBUGGING
        logging.debug(Residue_name)






        ###-----------C-terminus handling part #1 of 2-----------------###
        #Deal with C-terminal oxygen unless not necessary based on all amino acids being
        # identified without need to remove an oxygen from the pattern in the Spartan data
        # THIS BEGGINING OF DEALING WITH C-TERMINAL OXYGEN
        # Will be easiest to do as handling amino acid that just triggered need to deal with issue.
        # This way I can use the same handling of atom names following because swap out the old one for the one that matches
        if  CTerminalOxygenNeedsHandling:
            List_Of_Amino_Acid_Patterns_In_Order[-1] = amino_acid_atom_pattern_minus_last_oxygen #swap in the new pattern for here in list
            amino_acid_atom_pattern = amino_acid_atom_pattern_minus_last_oxygen #swap new pattern into current pattern buffer; I considered setting this up where I set 'CTerminalOxygenNeedsHandling = True' but thought since iterating on it, might cause probles

            # need to catch terminal oxygen line from the List_of_Atom_Lines_From_Spartan_Data
            Previouslineselements_string = "" # Preparing for checking if NCCO (peptide backbone)
            #occurs before an oxygen atom in the Spartan data because that should be an OXT terminal oxygen
            for atom_lines_index,atom_record_line in enumerate(List_of_Atom_Lines_From_Spartan_Data):
                if AtomNameIdentity(atom_record_line) == "O" and Previouslineselements_string[-4:]=="NCCO":
                    CterminalOxygenLine = atom_record_line
                    Index_of_CterminalOxygenLine = atom_lines_index
                Previouslineselements_string = Previouslineselements_string + AtomNameIdentity(atom_record_line)


            # and now that identified and captured line remove it from
            # List_of_Atom_Lines_From_Spartan_Data so extracting the coordinates
            # later can be performed
            del List_of_Atom_Lines_From_Spartan_Data[Index_of_CterminalOxygenLine]








        #Merge Fixed data with Spartan Coordinate data to make lines for amino acid just analyzed
        #enumerate from http://stackoverflow.com/questions/522563/accessing-the-index-in-python-for-loops , enumerate allows me to get current position in list for using
        for index, character in enumerate(amino_acid_atom_pattern):
            if AminoAcidInfo != "UNKNOWN (UNK)":
                The_Proper_Atom_Name = (Atom_Name_Dict[AminoAcidInfo])[index]
            else:
                The_Proper_Atom_Name = character
            Fixed_Line = "ATOM  " + Atom_serial_number_spaced(Reset_Atom_No) + " "
            Fixed_Line = Fixed_Line + Atom_Name_spaced(The_Proper_Atom_Name) + " "
            Fixed_Line = Fixed_Line + Residue_name + " " + Chain_ID_user_wants
            Fixed_Line = Fixed_Line + Residue_sequence_number_spaced(Residue_Sequence_Number) + "    "
            Fixed_Line = Fixed_Line + List_of_Atom_Lines_From_Spartan_Data[Reset_Atom_No-1][30:54]
            Fixed_Line = Fixed_Line + "  1.00  0.00          " + Element_symbol_spaced(character) + "  "
            List_for_Fixed_Atom_Records_Section.append(Fixed_Line)
            Reset_Atom_No +=1
        Residue_Sequence_Number +=1



    ###-----------C-terminus handling part #2 of 2-----------------###
    #Finish with C-terminal oxygen unless not necessary based on all amino acids being
    # identified without need to remove an oxygen from the pattern in the Spartan data
    # THIS THE OTHER PART OF DEALING WITH C-TERMINAL OXYGEN
    if  CTerminalOxygenNeedsHandling:
        Cterminal_Oxygen_Line = ("ATOM  " + Atom_serial_number_spaced(Reset_Atom_No) +
            "  OXT " + Residue_name + " " + Chain_ID_user_wants +
            Residue_sequence_number_spaced(Residue_Sequence_Number-1)  + "    " +
            CterminalOxygenLine[30:54] + "  1.00  0.00           O  ")
        List_for_Fixed_Atom_Records_Section.append(Cterminal_Oxygen_Line)
        Reset_Atom_No +=1
        #last part of script to deal with C-terminal oxygen will be here



    ###-----------Assembling last lines----------------###
    #Now add in Fixed Atom List to header
    List_To_Make_Fixed_Spartan_Output_From.extend(List_for_Fixed_Atom_Records_Section)  #from http://stackoverflow.com/questions/252703/python-append-vs-extend and http://stackoverflow.com/questions/8177079/python-take-the-content-of-a-list-and-append-it-to-another-list

    #Add 'TER' to end of chain
    List_To_Make_Fixed_Spartan_Output_From.append("TER   " +
        Atom_serial_number_spaced(Reset_Atom_No) +
        "     " + " " + Residue_name + " " + Chain_ID_user_wants +
        Residue_sequence_number_spaced(Residue_Sequence_Number-1) + (" "*54))
    # Above line uses 'Residue_Sequence_Number - 1' because when hit end of pattern processing
    # Residue_Sequence_Number gets increased by one but in case of TER line, actually
    # want the Residue_Sequence_Number the last pattern had.

    #Add 'END' to End of PDB entry
    List_To_Make_Fixed_Spartan_Output_From.append("END")



    ###--------GENERATE OUTPUT AND GIVER USER FEEDBACK---------------###
    #Print the fixed_output (originally this just went to stdout because easy for development and could redirect
    # now added file handling)
    Print_Lines_Of_Output_List(List_To_Make_Fixed_Spartan_Output_From,OutputFile)
    sys.stderr.write("The true PDB-formatted "+OutputFile+" has been created.\n")
    if not Problem_Identifying_an_internal_residue and not Problem_Identifying_Cterminal_residue and not Fixed_Start_Number:
        sys.stderr.write("There were no issues with creation of the file "+OutputFile+".\n \n")
    else:
        sys.stderr.write("There were the following issues with creation of the file "+OutputFile+":\n")


    #GiveFeedback on possible issues
    if Problem_Identifying_an_internal_residue:
        sys.stderr.write("\n***WARNING ********************WARNING ***************** \n")
        sys.stderr.write("Oops!  Unable to identify at least one residue that is not the last one in the chain. \n")
        sys.stderr.write(" The problem residue(s) will be recognizable in the output as")
        sys.stderr.write(" having 'UNK' as the residue name. \n")
        sys.stderr.write("***WARNING ********************WARNING ***************** \n \n")
    if not CTerminalOxygenNeedsHandling:
        if Problem_Identifying_Cterminal_residue:
            sys.stderr.write("\n***WARNING ********************WARNING ***************** \n")
            sys.stderr.write("Oops!  Unable to identify the last residue in the chain. \n")
            sys.stderr.write("The last residue will subsequently have 'UNK' as the residue name in the output. \n")
            sys.stderr.write("\nNOTE: The program only recognizes C-terminal oxygens for files built")
            sys.stderr.write(" by SPARTAN.\nIf the original source differs, such as being")
            sys.stderr.write(" from a PDB file,\nyou'll need to edit your SPARTAN data file ")
            sys.stderr.write("by using cut and paste in a text editor \nin order to place the record line")
            sys.stderr.write(" corresponding to the C-termial oxygen atom following\nthe four 'N-C-C-O'")
            sys.stderr.write("atoms at the start of the final residue. This alteration will make it\n")
            sys.stderr.write("match where SPARTAN places that atom during builds.\nThe fact")
            sys.stderr.write(" this disrupts the order of the record numbers doesn't matter.\n")
            sys.stderr.write("\nUpon completion of editing, input the new edited file into the SPARTAN08_Fixer.")
            sys.stderr.write("\nHopefully that will result in proper handling of such data and no warning.")
            sys.stderr.write("\n***END OF WARNING ***************END OF WARNING************* \n \n")
        else:
            sys.stderr.write("\n***NOTICE********************NOTICE****************** \n")
            sys.stderr.write("No Carboxy-terminal oxygen identified. \n")
            sys.stderr.write("Hopefully the omission of that atom was your intention and ")
            sys.stderr.write("the output is usable. \n")
            sys.stderr.write("***NOTICE*********************NOTICE****************** \n \n")
    if Fixed_Start_Number:
        sys.stderr.write("\n***NOTICE********************NOTICE****************** \n")
        sys.stderr.write("The start number of the residues has been adjusted down from what you had designated. \n")
        sys.stderr.write("PDB format limits residue numbers to 9999. The adjustment insures the data\n")
        sys.stderr.write("conforms to the PDB data format. \n")
        sys.stderr.write("***NOTICE*********************NOTICE****************** \n \n")


###-----DETERMINE IF INPUT IS FILE TO DO MAIN PART ON OR DIRECTORY ----------###
# If it is a DIRECTORY loop through doing main part on each PDB file
#from http://stackoverflow.com/questions/3204782/how-to-check-if-a-file-is-a-directory-or-regular-file-in-python
if os.path.isfile(args.InputData):
    THE_MAIN_FUNCTION(args.InputData,Chain_ID_user_wants, Number_to_start_numbering_with_from_user)
elif os.path.isdir(args.InputData):
    for f in os.listdir(args.InputData):
        pathname = os.path.join(args.InputData, f)
        mode = os.stat(pathname).st_mode
        if S_ISREG(mode) and pathname[-4:].upper() == ".PDB":
            # It's a PDB file, call the function
            THE_MAIN_FUNCTION(pathname,Chain_ID_user_wants,Number_to_start_numbering_with_from_user)
