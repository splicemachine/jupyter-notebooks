# Conversion Scripts
## These are a few scripts written by myself and Nirek to convert notebooks from Zeppelin to Jupyter, and to edit already made jupyter notebooks

* __convert.py__: This takes in a zeppelin notebook file (XXX.json) and and output name for the Jupyter notebook (XXX.ipynb) and converts it.
  - replace %spark.pyspark with nothing
  - %spark with %%scala
  - %splicemachine with %%sql
  - %md to a markdown type cell (jupyter cells have types)
  - It adds a bit more to make it work in the current state
  
* __multiple_zep_to_jup.py__: This function loops through all Zeppelin notebooks assuming the standard format (random HEX string and then `note.json` inside
 and converts all notebooks to Jupyter notebooks with the correct title and file structure
  - This function assumes there are a list of folders in the working directory, all with a file called `note.json`
  - Also assumes the necessary file directory structure is there. It should be modified to create the directory if not there, but when creating the file the directories were already there
  - This will overwrite any existing file with that name

* __add_cell.py__: This function loops through every ipynb file and adds a new cell at the top of each notebook.
  - The specific cell added is the assignment of `os.environ['JSBC_HOST'] = 'XXXX'` but that can/should be modified to your needs
  - This function assumes the working directory is of the same structure as the root of this repo (/jupyter-notebooks)
 
None of these scripts are particularly useful as they currently stand as they were specific to our needs, but they can be easily modified if you need to make a consistent change to a lot of notebooks. 
It's more about understanding the framework of looping through .ipynb cells and making changes. I'm adding them here for that reason.
