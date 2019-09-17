# jupyter-notebooks
Repo for Juypter Notebooks

# A few notes
* Because Jupyter notebooks don't have the odd naming convention the way Zeppelin notebooks do, each notebooks name will be the correct title of that note, not simply <code>node.json</code>
* There are 2 sets of notebooks that we use, cloud service and training. They will be separated by the two main directories here aptly named
* All notebooks that have Scala are not yet fully tested as Spark-Scala is not yet implemented fully, but pyspark/sql/markdown cells should be fully operational
* There are 3 "Setup" cells at the top of each notebook: Setting up the Jar for SQL and creating the PySpark interpreter. The  cells will be removed once those functions are natively working
* IMPORTANT: splice hints (--splice-properties) does not currently work.
* For Data Scientists/c. Using Spark in Jupyter Notebooks and i. ETL Pipeline and j. Examples need to be fixed due to specific data imports
