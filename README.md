# AutoDatabaseRefresh
AutoDatabaseRefresh - Development to use PBI to refresh data in SQL database


Context:

	1.Need to get new data stored in excel sheet on Sharepoint 

	2.Need to write this data into SQL database by appending to the existing dataset
	
	3.SQL database, with IDENTITY column

Remark: New data must be on sharepoint due to data security reason


Decision:

	1.Don't know how to use Python to download excel spreadsheet from Sharepoint => Use PBI to read new data from sharepoint and then use embedded python script to append new data to existing one in SQL database


Script:

	1.Test the script to be embedded on Power BI by reading in the dummy excel sheet
	
	2.Test writing new data to existing table by making sure no same data existed on the database before writing


Remark: PBI will run embedded python script around two times at every refresh so there is a need to check rewriting at every refresh to prevent creating duplicates
