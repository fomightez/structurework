# PDBsum-utilities

Utility scripts for working with data from [PDBsum](http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=index.html).

Associated demonstrations launchable in active form right in your browser available at my [pdbsum-binder](https://github.com/fomightez/pdbsum-binder).

Among this set of tools are several meant to facilitate highlighting differences & similarities in protein-protein interactions of the same protein pairs in different, related complexes. For example, several of these scripts aid in highlighting differences & similarities in protein-protein interactions when comparing macromolecular structures solved with different ligands or substrates or when comparing structures that share subsets of the same protein components. 

Note to self: **MENTION AS COMMENT at https://www.biostars.org/p/11880/#12024 WHEN ADD SOME CONTENT HERE**

# The scripts

* pdsum_prot_interactions_list_to_df.py
> PDBsum data for protein-protein interactions --> dataframe of data for use in Python

Takes PDBsum data for protein-protein interactions and makes a dataframe from it for use with Python.

Verified compatible with both Python 2.7 and Python 3.8.

Written to run from command line or pasted/loaded inside a Jupyter notebook cell.  
The main ways to run the script are demonstrated in the notebook `Working with PDBsum in Jupyter Basics.ipynb` that can be found when sessions are launched from [here](https://github.com/fomightez/pdbsum-binder).


Example calls to run the `pdsum_prot_interactions_list_to_df.py` script from command line:
```
python pdsum_prot_interactions_list_to_df.py data.txt
```

(Alternatively, upload the script to a Jupyter environment and use `%run pdsum_prot_interactions_list_to_df.py data.txt` in a Python-backed notebook to run the example.)



#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
import pdsum_prot_interactions_list_to_df from pdsum_prot_interactions_list_to_df
df =pdsum_prot_interactions_list_to_df('data.txt')
```
See [here](https://github.com/fomightez/pdbsum-binder) for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.

* similarities_in_proteinprotein_interactions.py
> PDBsum data for protein-protein interactions of two structures --> report on similarities for a pair of proteins interacting in both structures

This script is a utility script to generate a report on 
Go to my [pdbsum-binder](https://github.com/fomightez/pdbsum-binder) in your browser and click on the `launch binder`. When the session starts up, and the avalable notebooks are shown, double-click to open the one entitled `Using PDBsum data to highlight changes in protein-protein interactions.ipynb` and work through that to see an example that you can then adapt to look at protein-protein interactions in pairs of structures that interest you. (You may want to start with the first notebook in that series so you understand better the context.)

The notebook detailing how to use that script, `similarities_in_proteinprotein_interactions.py`, can be viewed statically [here](https://nbviewer.jupyter.org/github/fomightez/pdbsum-binder/blob/main/notebooks/Using%20PDBsum%20data%20to%20highlight%20changes%20in%20protein-protein%20interactions.ipynb).


Related
-------

- ?
