SPARTAN_FIXER
=============

SPARTAN08_Fixer is a program that fixes single chain Spartan'08 output
files in so-called PDB format, converting them to be true PDB format.
The fixed files can then easily be used in Jmol.

## Features :

 - Available in [webserver] form so no installation needed, unless you have A LOT of files to convert
 - command line version allows single files or entire folders of PDB files to be converted automagically.
 - conforms to PDB format specifications as described [here][2] and [here][3]

##Webserver
[fomightez.pythonanywhere.com/spartan_fixer/][webserver]
* At the above site, you can find a server where you can paste in a file and have it processed by the SPARTAN08_Fixer program.
* If you have a lot of files to convert or need greater customization in your workflow than you'll want the [command line version SPARTAN08_Fixer_standalone.py DOWNLOADABLE in this repository](https://github.com/fomightez/structurework/blob/master/spartan_fixer/SPARTAN08_Fixer_standalone.py).


## Usage :

###MANUAL/HELP OPTION for command line version

$ `python SPARTAN08_Fixer.py --help`



    usage: SPARTAN08_Fixer.py [-h] [--ChainDesig X] [--StartNo Y] [-a] InputData

    SPARTAN08_Fixer is a program that fixes single chain Spartan'08 output
    files in so-called PDB format, converting them to be true PDB format.
    The fixed files can then easily be used in Jmol.

    Written by Wayne Decatur --> Fomightez @ Github or Twitter.

    PDB format specification info:
    http://www.wwpdb.org/docs.html and http://deposit.rcsb.org/adit/docs/pdb_atom_format.html



    Actual example what to enter on command line to run program:
    python SPARTAN_FIXER input_file.pdb



    positional arguments:
      InputData       name of Spartan data file that will be fixed. REQUIRED.
                      Files entered this way do not have any requirement for specific extension as long
                      they are SPARTAN so-called PDB formatted-data.

                      The required input data can also be a group of files ending in '.pdb' (case does not matter)
                      contained within a folder. In that case put the folder as the input data.

    optional arguments:
      -h, --help      show this help message and exit
      --ChainDesig X  Enter in place of 'X' an alphanumeric character
                      to use as chain designation, or enter when prompted
      --StartNo Y     Enter in place of 'Y' a number in the range 1 to 9999
                      to be the first residue sequence number
                      for the output, or enter when prompted
      -a, --auto      Run without further prompts for user action, using chain
                      designation and starting residue on command line or
                      the defaults of 'A' and '1', respectively, for
                      those values if none provided.

### Typical examples of use of command line version
#### Typical run
$ `python SPARTAN08_Fixer.py spartanPDBfile.pdb`

You'll be prompted to enter chain identifier designation and a number at which to start the residue numbering.

#### Typical run, specifying the options at the command line
$ `python SPARTAN08_Fixer.py spartanPDB.pdb --ChainDesig G --StartNo 7`


#### Running on PDB files in a directory
$ `python SPARTAN08_Fixer.py TheDirectory`

#### Running on PDB files in a directory with default settings without prompts
$ `python SPARTAN08_Fixer.py TheDirectory --auto`

#### Running on PDB files in a directory using command line to designate values
$ `python SPARTAN08_Fixer.py TheDirectory --ChainDesig Z --StartNo 16`


## Development
Developed by [Wayne Decatur](https://github.com/fomightez) in collaboration with [Nick Greeves](http://www.liv.ac.uk/chemistry/staff/nicholas-greeves/) ([@nickgreeves](https://twitter.com/nickgreeves)) and Rui Li.

[home]: https://github.com/fomightez/spartan_fixer
[webserver]: http://fomightez.pythonanywhere.com/spartan_fixer/
[2]: http://deposit.rcsb.org/adit/docs/pdb_atom_format.html
[3]: http://www.wwpdb.org/documentation/format33/sect9.html#ATOM
