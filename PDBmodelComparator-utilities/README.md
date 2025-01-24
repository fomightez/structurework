# PDBMmodelCompator-utilities

Utility scripts for working with the PDBMmodelComparator.

A set of Jupyter notebooks that include demonstrations of all these scripts is launchable in active form right in your browser is at my [PDBMmodelComparator repo](https://github.com/fomightez/PDBmodelComparator). Just go [there](https://github.com/fomightez/pdbepisa-binder) and click the `launch binder` badge to get started.

Be sure to see the 'Related' section below as well.


# The scripts

* missing_residue_detailer.py
> PDB identifier code ---> information on missing residues per chain

Meant to use Python code to recapitulate what Eric Martz's FirstGlance in Jmol gives in its report on missing residues pane.  
Note that to make sure this recapitulates what Eric Martz's FirstGlance in Jmol gives, some tests are run for a few PDB files on my [PDBMmodelCompator repo](https://github.com/fomightez/PDBMmodelCompator). (This is planned to be made to be automated for any commit eventually.) To explore the tests, go [here](https://github.com/fomightez/PDBMmodelCompator), click '`launch binder`', and then open the notebook [(Technical) Jupyter Notebook testing if output of utility script `missing_residue_detailer.py` makes same content as FirstGlance in Jmol](additional_nbs/test_missing_residue_detailer.ipynb) under the 'Technical Section'. Also see [here](https://github.com/fomightez/PDBmodelComparator/tree/main/additional_nbs/tests/README.md).

This script works with browser-based computing environments powered by WebAssembly, like Pyodide / JupyterLite!

Because getting the header for the structure from the Protein Data Bank is a critical initial step in this script functioning every effort has been made to make that retrieval automatic & robust. However, as it involves a network connection, it is subject to the intricacies that can be involved in web traffic, such as firewalls and dropped connections. To make it so getting the PDB header isn't an impassable hurdle to using this script, there is the option to supply the header content as text in a file. **Importantly, being able to supply a file with the equivalent header details allows one to use structure models not yet released along with those that are with the [PDBMmodelCompator](https://github.com/fomightez/PDBMmodelCompator).** (The use of `missing_residue_detailer.py` is actually the first step in the [PDBMmodelCompator](https://github.com/fomightez/PDBMmodelCompator) process.) The 'header' file doesn't even need to contain the official text that will be available along with the structure on the Protein Data Bank site. You can edit two sections of a header to have the equivalent data for the structure of interest. This is because as long as two sections, `REMARK 465` and `SEQRES` section are valid PDB header format and composed of data salient to the structure of interest, the script `missing_residue_detailer.py` will work. (Note if the structure file in PDB format includes the header, the entire structure file PDB format file can be used as well and just renamed to match the convention; having the coordinate data there is moot though as only the header is utilized.)

To supply the PDB header text in a file, place the text obtained from the Protein Data Bank (or equivalent for unreleased structures) in your current working directory with the file name with the content matching the convention of the PDB id code following by `_header4missing.txt`; case doesn't matter for the PDB identifier portion. (By the way, every PDB entry has the option on the 'Structure Summary' page under '`Display Files`' in the upper right corner to display '`PDB Format (Header)`' from the that drop-down. The content that comes up in that view is what you'd place in this file.) For example, for [PDB entry 1D66](https://www.rcsb.org/structure/1d66) the file to place in your current working directory would have a name looking like:

```text
1d66_header4missing.txt
```
With that file in place, you'd then call the script like normal using the same PDB id code as in the file name. For example, issue the command:

```text
python missing_residue_detailer.py 1d66
```

The unique file suffix `_header4missing.txt` as part of the signal of which file to ise is to make it less likely you'd have a file that would match the convention without you having opted to use this approach.  




* ???????.py
> Placeholder for example input ---> Placeholder for example result


#### For running in a Jupyter notebook:

To use this script after pasting or loading into a cell in a Jupyter notebook, in the next cell define the URL and then call the main function similar to below:
```
import ?????
df = ?????
```
See [here](https://github.com/fomightez/PDBMmodelCompator) for notebooks demonstrating use within a Jupyter notebook; click `launch binder` to launch a session that will allow you to use the notebooks from there.


Related items by me
-------------------
- The PDBePISA has good summaries of data involving protein chains in structues of complexes. See the related series of demo notebooks available at my repo [pdbepisa-binder](https://github.com/fomightez/pdbepisa-binder) for demonstrations of related scripts (scripts listed [here](https://github.com/fomightez/structurework/tree/master/pdbepisa-utilities)).
- The PDBsum has good summaries of data involving protein chains in structues of complexes. See the related series of demo notebooks available at my repo [pdbsum-binder](https://github.com/fomightez/pdbsum-binder) for demonstration of related scripts (scripts listed [here](https://github.com/fomightez/structurework/tree/master/pdbsum-utilities)).
- [My humap3-binder repo](https://github.com/fomightez/humap3-binder)

## Related items by others

???
