# A dynamic review of graph databases in bioinformatics and systems biology

This repository hosts a dynamic review of the use of graph databases in bioinformatics and systems biology. The list of graph databases was formed based on the [DB-Engines](https://db-engines.com/en/) initiative with the list of popular [graph database management systems](https://db-engines.com/en/ranking/graph+dbms) ranked. 

The **[output](https://github.com/ilyamazein/gdbreview/tree/main/output)** folder contains CSV files with query results.

The **[annotated](https://github.com/ilyamazein/gdbreview/tree/main/annotated)** folder contains a CSV file with a complete list of annotated articles.

The **[code](https://github.com/ilyamazein/gdbreview/tree/main/code)** folder contains the Python code used for exporting publication data and integrating search results into a single table. The corresponding search queries are provided in the TXT files.

Requirements: the Python code needs the 'requests' and 'pandas' modules to run. They can be installed using pip:
```
pip install requests
pip install pandas
```
