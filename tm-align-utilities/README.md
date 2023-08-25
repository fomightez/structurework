# TM-align-utilities

Utility scripts for working with data from [Tm-align](https://zhanggroup.org/TM-align/), an algorithm for protein structure alignment and comparison.

Be sure to see the 'Related' section below, as some of these utility scripts (or the ideas behind them) are also used to layer on structure information to equivalent residues and conservation.


# The scripts or utility code

* utility to reformat sequence alignment in result of TM-align structural alignment from all one long sequence to blocks of paired sequences
> alignment as three long lines --> alignment as blocks of defined lentgh

Notebook [available in sessions launched from here](https://github.com/fomightez/cl_demo-binder) demonstrates code to convert the alignment TM-align returns as part of its results page and reformats it into blocks of aligned sequences. The reformatted version fits better in other documents & reports and is easier to view & compare the N- and C-terminal sequences at the same time. To use it, go to that link, click `launch binder` and select 'Conversion from single-line to multi-line blocks of alignment showing residue pairs made by TM-align' from the list of notebooks that come up.    



Related
-------

* Notebook [available in sessions launched from here](https://github.com/fomightez/cl_demo-binder).  
For example, there is a demo of code to use part of a sequence alignment to construct fit/compare commands for PyMOL and Jmol

	- Using Biopython to list resolved residues and construct fit commands for chains shared by two structures  (<---Probably using TM-Align is easier than this?)
	- Determine residues that match to a reference from multiple sequence alignment and use to construct fit commands

* [a gist](https://gist.github.com/fomightez/2601c0f5a13b85cd21b9377169c79836) I forked from [Joao Rodrigues](https://gist.github.com/JoaoRodrigues/e3a4f2139d10888c679eb1657a4d7080) for aligning structures using Biopython. See [here](http://thread.gmane.org/gmane.comp.python.bio.general/8782/focus=8783) about it.


* Installing TM-align for use on command line (tmalign):
what is stated at https://zhanggroup.org/TM-align/ under the section 'TM-align download' didn't look overly user-friendly but 
https://anaconda.org/bioconda/tmalign  says conda command is:

```shell
conda install -c bioconda tmalign
``` 
