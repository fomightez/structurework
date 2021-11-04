# PISA-utilities

Utility scripts for working with data from [PDBePISA](https://www.ebi.ac.uk/pdbe/pisa/).

A set of Jupyter notebooks that include demonstrations of all these scripts is launchable in active form right in your browser is at my [pdbepisa-binder repo](https://github.com/fomightez/pdbepisa-binder). Just go [there](https://github.com/fomightez/pdbepisa-binder) and click the `launch binder` badge to get started.

Be sure to see the 'Related' section below as well.


# The scripts

* pisa_interface_list_to_df.py
> PDB entry accession id ---> Python-based dataframe of Interfaces from PDBePISA for chains interacting

Takes a PDB accession code or a file name of text copied from a PDBePISA Interface list page and produces a dataframe of the interchain reactions detailing the intraction area for each chain as well as the number & types of interactons.  
**Importantly, it handles protein and nucleic acid interactions whereas PDBsum just summarizes interfaces between proteins in its summary tables of interactions.**

Verified compatible with both Python 2.7 and Python 3.8.

Written to run from command line or pasted/loaded inside a Jupyter notebook cell.  
The main ways to run the script are demonstrated in the notebook [Working with PDBePISA interface lists/reports in Jupyter Basics and filtering to nucleic acid chains](notebooks/Working%20with%20PDBePISA%20interfacelists%20in%20Jupyter%20Basics.ipynb) that can be found when sessions are launched from [here](https://github.com/fomightez/pdbepisa-binder).


Example calls to run the `pisa_interface_list_to_df.py` script from command line:
```
python pisa_interface_list_to_df.py 4fgf
python pisa_interface_list_to_df.py 1trn
```

(Alternatively, upload the script to a Jupyter environment and use `%run python pisa_interface_list_to_df.py 4fgf` in a Python-backed notebook to run the example.)

**Impoertantly, if a file already exists that is the PDB code followed by `_interface_list.txt`, such as `4fgf_interface_list.txt`, it will use the corresponding file to extract the information instead of obtaining the data from PDBePISA.** This can be used to supply files, perhaps specially edited ones or for structures not yet publised, locally.


#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
import pdsum_prot_interactions_list_to_df from pdsum_prot_interactions_list_to_df
df =pdsum_prot_interactions_list_to_df('4fgf')
```
See [here](https://github.com/fomightez/pdbepisa-binder) for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.


Related
-------

- The PDBsum has good summaries of data involving all protein chains in structues. See the related series of demo notebooks available at my repo [pdbsum-binder)](https://github.com/fomightez/pdbsum-binder) for demonstration of related scripts (scripts listed [here](https://github.com/fomightez/structurework/tree/master/pdbsum-utilities)).
