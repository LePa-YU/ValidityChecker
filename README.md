# ValidityChecker

To run the Validity Checker please install the following dependencies:
- tkinter

Instructions to installing tkinter
- Make sure you have python 3.x installed: python --version
- Note: The code is tested on Python 3.10.0
- Make sure you have pip installed: pip -V
- See if tkinter is already installed: python -m tkinter
- Install using: pip install tk
- See further instructions: https://www.tutorialspoint.com/how-to-install-tkinter-in-python


To execute the code please run the following file:
- validity_checker.py

When run, the Validity Checker will prompt the user to input a file from their file explorer. There are a few example data files in the /Datasets/ folder within the Validity Checker.

The file chosen should be a .csv file. 

The program can either:
1. Show the errors found within the file (input: error or e)
2. Show the warnings found within the file (input: warning or w)
3. Show any empty fields found within the file (input: field or f)
3. Quit the program (input: quit or q)

The checks performed by the validity checker are:
1. Check the header of the csv file given. The header should have the following columns: identifier, title, type. All other columns are optional.
2. Check the header for spelling mistakes. This only works for simple spelling mistakes such as incorrect capitalization.
3. Check if a field is empty within the csv. Will give an error only if the field is mandatory (ID, title or type). The other empty fields will be recorded and can be viewed with the empty field (f) command.
4. Check for start or end nodes. These nodes are special and should not have any other relationships except for comesAfter (end node). There should only be one start or end node in the dataset.
5. Check for empty rows with only identifier present. Empty rows with no identifier within the dataset should be deleted.
6. Check for each aER and iER for a comesAfter or requires relationship.
7. Check for each rER for an assesses relationship.

TBD:
- Test cases
- Circular logic check 


#Dataset Updater
To run the Dataset Updater please install the following dependencies:
- tkinter

Instructions to installing tkinter
- Make sure you have python 3.x installed: python --version
- Note: The code is tested on Python 3.10.0
- Make sure you have pip installed: pip -V
- See if tkinter is already installed: python -m tkinter
- Install using: pip install tk
- See further instructions: https://www.tutorialspoint.com/how-to-install-tkinter-in-python

To execute the code please run the following file:
- update_dataset.py

When run, the Dataset Updater will prompt the user to input a file from their file explorer. There are a few example data files in the /Datasets/ folder within the ValidityChecker.

The file chosen should be a .csv file. 

The program can either:
1. Add row (input: a). This is TBD
2. Delete row (input: d)
3. Delete empty rows (input: del)
4. Edit row (input: e). This is TBD 
5. Print current (input: p)
6. Save current (input: s)
7. Quit (input: q)