
This is a plug and run script. Meaning that you just need to update a few file paths, then run it right away. No coding knowledge or extra setup required. Though coding
logic explanations are included in the parsing code.

A few things in order to adjust this code to your system.

1: Edit the Script’s File Paths to adhere to your own computer/device

You need to tell the script two things:
    Where your IRS XML folders are located (the parent folder)
    Where to save your final spreadsheet file (the CSV output file)

Find the following two lines near the top of the script:
    parent_folder = r"C:\IRS990H_Parser\EIN zip files 20xx"
    output_csv = r"C:\IRS990H_Parser\csv output\IRS 990H 20xx.csv"

You will need to change both lines so they match:
    The folder where your IRS XML files are stored
    The folder (and filename) where your final CSV should be saved

Please don’t type the paths yourself. Just use the built-in “Copy as path” tool:
    1. Open File Explorer and go to the parent folder where your IRS XML subfolders are stored (in your C: drive)
            NOTE: You can ALSO just "copy path" from the VSCode explorer on the left hand side
   
    2. Right-click that folder (e.g., EIN zip files 2017)
   
    3. Click “Copy as path”
   
    4. Paste that into the script after parent_folder =

Repeat these steps for where you want the CSV to go:
    1. LEFT-click your csv output folder (e.g., csv output)
   
    2. Choose the csv file that's associated with your XMLs that you're about to parse
   
    3. Click “Copy as path”
   
    4. Paste it into the script after output_csv =
  
    5. Be sure to add a filename at the end (e.g., IRS 990H 2019.csv)


A Few Key Notes:
    Keep the r before the path: This tells Python to read the backslashes correctly (a "raw string").

    Keep quotes around the path ("like this")

    You can use either \\ or \ inside the path. Python understands both when using r"".



2: How to Add a New IRS Filing Year
    If you want to extract Schedule H data for a future year like 2026, you’ll need to add a few new lines to a specific part of the script.
    Don’t worry, it’s just copying and pasting with some edits.


    Scroll down in the script until you find a big section called release_info_for_subfolder =
    You’ll see blocks labeled by year — like #2017, #2018, #2019, and so on up until 2025
    This is where the script matches each folder of XML files to metadata about that ZIP release


If you download a 2026 ZIP file from the IRS, you’ll need to add a block that looks like this to the script under the 2025 block. Label it:

#2026

"2026_TEOS_XML_01A": {
    "ReleaseYear": "2026",
    "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_01A.zip",
    "ReleaseDownload": "20xx-01-01"                                                                 <-- use the actual date you downloaded the zip file
    "ReleaseFileName": "2026_TEOS_XML_01A.zip"
},

    Adjust the csv output path to adhere to the new year, and don't forget to add a new csv file in the csv output folder. In order to do so, click on the csv output
    dropdown in the VSCode Explorer. You will see multiple green files that represents the csv files. To add a new one, just right click "csv output" and click "New File".
    Name this new file "IRS 990H 2026.csv"

    Remember: This one block adheres to ONLY one zip file. i.e. "2026_TEOS_XML_01A". Multiple zip files will be available for download each year, so please adjust
    ccordingly for each zip file.

Lastly two more things.

First, as of right now it is currently May 10th, 2025. Meaning that there will be more 2025 downloads available eventually. Please be mindful for these new
zip files. The logic still applies, download the zip file, extract it to the proper subfolder in the parent folder, add a new block we just did for the new zip file.


Secondly, the subfolders are currently empty. If you already have a specific zip file downloaded or have the files already extracted in another folder, I recommend
two things.
    One, locate the folder where the XML files are in, CTRL + A --> Copy --> Go to the proper subfolder in the parent folder and then paste. All files will
    transfer into the new subfolder.
    
    Or two (I recommend this method more) move the whole entire folder that the files are in, and relocate them into the parent folder and rename
    it so it adheres to the script's mapping logic.

Remember that its much faster if you parse the files locally rather than through OneDrive,  so completely moving it is recommended since the first method copied the XMLs
which just takes up more storage.


If you have any questions, please reach out to my personal email. Good luck!

Jack Sheridan
sheridanjack38@gmail.com
