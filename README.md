# ValidityChecker

To run the Validity Checker please install the following dependencies:
- tkinter (https://www.tutorialspoint.com/how-to-install-tkinter-in-python)

To execute the code please run the following file:
- validity_checker.py

When run, the Validity Checker will prompt the user to input a file from their file explorer. There is an example data file in the /Datasets/ folder within the Validity Checker named: 1530_dataset_overview.csv

The file chosen should be a .csv file. 

The program can either:
1. Show the errors found within the file (type: error or e)
2. Show the warnings found within the file (type: warning or w)
3. Quit the program (type: quit or q)

The checks performed by the validity checker are:
1. Check headers for spelling mistakes, missing headers 
2. Check if a field is empty within the csv. Will give an error if the field is mandatory. Will give a warning if the field is empty but not mandatory.
3. Check if the requires field has a value and makes sure that that value is backwards complicit with the isRequiredBy value within the ID it points to. E.g. ID 11 requires points to IDs 21 and 197. IDs 21 and 197 have a isRequiredBy value of 11. Will add an error if an ID is missing. 

TBD:
- Test cases
- Circular logic check 
