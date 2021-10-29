structurework
=============

Repository for programs and [Python scripts](https://github.com/fomightez/structurework/tree/master/python_scripts) for molecular structure analysis.

See the sub-folders in this repository for specifics. (Sorely need to improve on this.)


Related 'Binderized' Utilities
----------------------------

Collection of links to launchable Jupyter environment where various structure/function analysis tools work. Many of my recent scripts are built with use in these environments in mind:

- [bio3d-binder](https://github.com/fomightez/bio3d-binder) - launchable, working Jupyter-based environment with the Bio3D package for Macromolecular Structure Analysis running in R+Jupyter (RStudio is an option there, too) with some examples (*R-based*).

- [cl_demo-binder](https://github.com/fomightez/cl_demo-binder) - launchable, working Jupyter-based environment that has a collection of demonstrations of useful resources on command line (or useable in Jupyter sessions) for manipulating structure files.

- [pdbsum-binder](https://github.com/fomightez/pdbsum-binder) - launchable, working Jupyter-based environment that has a collection of demonstrations of my useful resources for analyzing data from [PDBsum](http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=index.html). The [pdbsum-utilities sub-folder in this repo](https://github.com/fomightez/structurework/tree/master/pdbsum_utilities) is related as it host many of the scripts and code backing the data analyses.

- [pymol-binder](https://github.com/fomightez/pymol-binder)

- [Python_basics_on_PDB_file](https://github.com/fomightez/Python_basics_on_PDB_file)


Related 'Docker-ized' Utilities
-------

[Dockerfiles for Structural Analysis (Structural Bioinformatics) Docker images](https://github.com/fomightez/Dockerfiles#dockerfiles-for-structural-analysis-structural-bioinformatics-docker-images).

Related non-Python tips
-----------------------

>"Learned a handy pair of grep flags - "grep -F -f". I find it useful for grabbing the intersection of two #cryoem particle star files, e.g. from masked classification of different domains. (here particle list is just the rlnImageName column of http://class1.star )" [Source](https://twitter.com/OliBClarke/status/1100400145286524928)

    grep -F -f particle_list_class1 class2.star >& class12_instersect.star &


Related resources by others
---------------------------

- [rna-tools (previously rna-pdb-tools): a toolbox to analyze sequences, structures and simulations of RNA](https://github.com/mmagnus/rna-tools/blob/master/index-of-tools.md)

- [PDBrenum: A webserver and program providing PDB renumbered according to their UniProt sequences](http://dunbrack3.fccc.edu/PDBrenum/). The [associated scientific article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0253411) shows how to run it as a Python script in detail. The [Announcement](https://twitter.com/RolandDunbrack/status/1412675616156098562).

- [Converters provided by GEMMI tools in web browser via web assembly](https://project-gemmi.github.io/wasm/) - site can do (More about [Gemmi here](https://github.com/project-gemmi/gemmi)):
    - PDB ➜ mmCIF
    - mmCIF ➜ PDB
    - mmCIF ➜ MTZ
    - MTZ ➜ mmCIF
    - 2 × data files ➜ mmCIF (deposition-ready)
