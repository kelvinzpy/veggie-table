# veggie-table
Python script for committing food data into tables - this script should be functional cross-platform (windows, OSX, linux) to the best of my knowledge

This script allows the user to make LEFT/RIGHT inputs when viewing a series of videos, and collect the data generated during each video (e.g. LLRRLRL binary) in an Excel sheet for easy analysis

On running the script, there will be a box for the user to enter the number of samples expected to be collected during the duration of each video (e.g. if 10 is entered, then 10 total recordings of LEFT or RIGHT should be carried out during the duration of each video). Type in a number, press Enter and then ESC to confirm.

Before each video plays, the user will be asked to identify the food from each side (left and right), given a preview frame (the first frame of the video).

Functionality during video playback:
  - LEFT/RIGHT arrow keys: records a "left" or "right" selection
  - ESC: skips the video (and the program if it is the last video)
  

EXTRACTING DATA INTO EXCEL

You should obtain a .txt file as the end of the program. In order to properly extract the data into an Excel sheet, please follow these steps:

For Excel 2016:
1) Open Excel
2) Go to Data -> From Text/CSV
3) Select the .txt file
4) Under "Data Type Detection", select "Do not detect data types“
5) Press "Load" to import the table into Excel

For Excel 2007:
1) Open Excel
2) Select File -> Open and select the .txt file. The Text Import Wizard will open
3) In Step 1 of the Text Import Wizard, select "delimited" as the original data type and click Next
4) In Step 2 of the Text Import Wizard, select "comma" as the delimiter and click Next
5) In Step 3 of the Text Import Wizard, select "text" as the column data format and click Finish

