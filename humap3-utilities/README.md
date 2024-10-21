# humap3-utilities

Utility scripts for working with data from hu.MAP 3.0.

A set of Jupyter notebooks that include demonstrations of all these scripts is launchable in active form right in your browser is at my [humap3-binder repo](https://github.com/fomightez/humap3-binder). Just go [there](https://github.com/fomightez/pdbepisa-binder) and click the `launch binder` badge to get started.

Be sure to see the 'Related' section below as well.


# The scripts

* complexes_rawCSV_to_df.py
> raw data csv file ---> Python-based dataframe of raw data on all complexes.

   Pickled dataframe saved as `'raw_complexes_pickled_df.pkl'`. ('pickled' just means stored in a special serialized form easy for Python to access.)  
   The script is meant to be run with`uv` using  `uv run complexes_rawCSV_to_df.py hu.MAP3.0_complexes_wConfidenceScores_total15326_wGenenames_20240922.csv`.

* ???????.py
> gene name ---> Python-based dataframe of genes with proteins int the complex


#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
import ?????
df = ?????
```
See [here](https://github.com/fomightez/humap3-binder) for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.


Related items by me
-------------------
- I use the Unipressed package a lot with working with this data, see my [Unipressed-binder repo](https://github.com/fomightez/Unipressed-binder) for more on working with this package.
- The PDBePISA has good summaries of data involving all protein chains in structues. See the related series of demo notebooks available at my repo [pdbepisa-binder](https://github.com/fomightez/pdbepisa-binder) for demonstrations of related scripts (scripts listed [here](https://github.com/fomightez/structurework/tree/master/pdbepisa-utilities)).
- The PDBsum has good summaries of data involving all protein chains in structues. See the related series of demo notebooks available at my repo [pdbsum-binder](https://github.com/fomightez/pdbsum-binder) for demonstration of related scripts (scripts listed [here](https://github.com/fomightez/structurework/tree/master/pdbsum-utilities)).

## Related items by others

There is also jsPISA, which is [supposedly](https://pubmed.ncbi.nlm.nih.gov/25908787/) an improved user interface; however, I don't see a way to use access as an API, several PDB entries I put in gave the error that they did not exist, and when I tried with [4fgf that shows a very informative interface table and PDBePISA](http://www.ebi.ac.uk/pdbe/pisa/cgi-bin/piserver?qi=4fgf), I was not able to see equivalent at jsPISA. jsPISA is maintained by CCP4 [here](http://www.ccp4.ac.uk/pisa).

[Louis](https://www.biostars.org/u/9020/) has [a script](https://gist.github.com/lmmx/91515d38a1fc0644268f#file-getxml-py) that gets HTML (or is it XML?) for a lot of PDB indentifiers. It allows for interrupted/resumed download.
