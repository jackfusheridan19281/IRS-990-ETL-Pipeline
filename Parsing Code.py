
"""
This script extracts financial and community benefit data from IRS 990 Schedule H XML files.
All the XML files live inside subfolders under a parent folder named "EIN zip files xxxx".
Each subfolder corresponds to one ZIP release (e.g. "xxxx_TEOS_XML_01A").
"""
    # These lines bring in external functionality:
    #  - os (operating system): to work with file paths and directories
    #  - pandas (pd): to build and save tables of data
    #  - BeautifulSoup: to parse XML content
    #  - tqdm: to show a progress bar when looping through many files
import os
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

    # 1) PARENT FOLDER and output CSV
    # Here we tell the script where to find the XML folders (parent_folder)
    # and where to save the final combined data (output_csv)
    # You must change these paths to match your own computer (Refer to README.txt for further clarification)
parent_folder = r"C:\IRS990H_Parser\EIN zip files 2025"
output_csv = r"C:\IRS990H_Parser\csv output\IRS 990H 2025.csv"

    # This big dictionary maps each subfolder name to metadata about that release:
    #  - ReleaseYear: the IRS data year
    #  - ReleaseSource: the URL where the ZIP originally came from
    #  - ReleaseDownload: the date the ZIP was downloaded locally
    #  - ReleaseFileName: the ZIP file’s name when downloaded
    # When looping through the xml folders through the parent folders, the script looks up these details
        # For example, if you have an xml folder i.e. "2017_TEOS_XML_CT1" inside of a parent folder i.e. "EIN zip files 2017"
        # It will automatically map the "2017_TEOS_XML_CT1" folder to
                                                                #    "ReleaseYear": "2017",
                                                                #    "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/2017_TEOS_XML_CT1.zip",
                                                                #    "ReleaseDownload": "2025-03-05",
                                                                #    "ReleaseFileName": "2017_TEOS_XML_CT1.zip"
                                                                #
                                                                #     Which will populate the data inside of the csv file output
release_info_for_subfolder = {
    
    #2017

    "2017_TEOS_XML_CT1": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/2017_TEOS_XML_CT1.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "2017_TEOS_XML_CT1.zip"
    },

    "download990xml_2017_1": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/download990xml_2017_1.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_1.zip"
    },

    "download990xml_2017_2": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/download990xml_2017_2.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2017_2.zip"
    },

    "download990xml_2017_3": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/download990xml_2017_3.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2017_3.zip"
    },

    "download990xml_2017_4": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/download990xml_2017_4.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2017_4.zip"
    },

    "download990xml_2017_5": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/download990xml_2017_5.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2017_5.zip"
    },

    "download990xml_2017_6": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/download990xml_2017_6.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2017_6.zip"
    },

    "download990xml_2017_7": {
        "ReleaseYear": "2017",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2017/download990xml_2017_7.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2017_7.zip"
    },

    #2018

    "2018_TEOS_XML_CT1": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/2018_TEOS_XML_CT1.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "2018_TEOS_XML_CT1.zip"
    },

    "2018_TEOS_XML_CT2": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/2018_TEOS_XML_CT2.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2018_TEOS_XML_CT2.zip"
    },

     "2018_TEOS_XML_CT3": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/2018_TEOS_XML_CT3.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2018_TEOS_XML_CT3.zip"
    },

    "download990xml_2018_1": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_1.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_1.zip"
    },

    "download990xml_2018_2": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_2.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_2.zip"
    },

    "download990xml_2018_3": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_3.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_3.zip"
    },

    "download990xml_2018_4": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_4.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_4.zip"
    },

    "download990xml_2018_5": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_5.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_5.zip"
    },

    "download990xml_2018_6": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_6.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_6.zip"
    },

    "download990xml_2018_7": {
        "ReleaseYear": "2018",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_7.zip",
        "ReleaseDownload": "2025-03-05",
        "ReleaseFileName": "download990xml_2018_7.zip"
    },


    #2019

    "2019_TEOS_XML_CT1": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/2019_TEOS_XML_CT1.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "2019_TEOS_XML_CT1.zip"
    },
    
     "download990xml_2019_1": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_1.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_1.zip"
    },

    "download990xml_2019_2": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_2.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_2.zip"
    },
    
    "download990xml_2019_3": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_3.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_3.zip"
    },

    "download990xml_2019_4": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_4.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_4.zip"
    },

    "download990xml_2019_5": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_5.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_5.zip"
    },

    "download990xml_2019_6": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_6.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_6.zip"
    },

    "download990xml_2019_7": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_7.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_7.zip"
    },

    "download990xml_2019_8": {
        "ReleaseYear": "2019",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_8.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2019_8.zip"
    },

    #2020

    "2020_TEOS_XML_CT1": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/2020_TEOS_XML_CT1.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "2020_TEOS_XML_CT1.zip"
    },

     "download990xml_2020_1": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_1.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_1.zip"
    },
    
    "download990xml_2020_2": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_2.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_2.zip"
    },
    
    "download990xml_2020_3": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_3.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_3.zip"
    },
    
    "download990xml_2020_4": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_4.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_4.zip"
    },
    
    "download990xml_2020_5": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_5.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_5.zip"
    },
    
    "download990xml_2020_6": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_6.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_6.zip"
    },
    
    "download990xml_2020_7": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_7.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_7.zip"
    },
    
    "download990xml_2020_8": {
        "ReleaseYear": "2020",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_8.zip",
        "ReleaseDownload": "2025-04-16",
        "ReleaseFileName": "download990xml_2020_8.zip"
    },
    
    #2021 (I recommend to not open up the parent folder as it contains over 700,000 files and might crash VSCode)

    "2021Redo_allCycles": {
        "ReleaseYear": "2021",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2021_TEOS_XML_01A.zip"
    },

    #2022

    "2022Redo_cycle01_41": {
        "ReleaseYear": "2022",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2022_TEOS_XML_01A.zip"
    },
    "2022_TEOS_XML_11A": {
        "ReleaseYear": "2022",
        "ReleaseSource": "https://web.archive.org/web/20240806044052/https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_11A.zip",
        "ReleaseDownload": "2025-03-20",
        "ReleaseFileName": "2022_TEOS_XML_11A.zip"
    },
    "2022_TEOS_XML_11B": {
        "ReleaseYear": "2022",
        "ReleaseSource": "https://web.archive.org/web/20240806044052/https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_11B.zip",
        "ReleaseDownload": "2025-03-20",
        "ReleaseFileName": "2022_TEOS_XML_11B.zip"
    },
    "2022_TEOS_XML_11C": {
        "ReleaseYear": "2022",
        "ReleaseSource": "https://web.archive.org/web/20240806044052/https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_11C.zip",
        "ReleaseDownload": "2025-03-20",
        "ReleaseFileName": "2022_TEOS_XML_11C.zip"
    },

    #2023

    "2023_TEOS_XML_01A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_01A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_01A.zip"
    },
    "2023_TEOS_XML_02A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_02A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_02A.zip"
    },
    "2023_TEOS_XML_03A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_03A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_03A.zip"
    },
    "2023_TEOS_XML_04A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_04A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_04A.zip"
    },
    "2023_TEOS_XML_05A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_05A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_05A.zip"
    },
    "2023_TEOS_XML_06A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_06A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_06A.zip"
    },
    "2023_TEOS_XML_07A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_07A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_07A.zip"
    },
    "2023_TEOS_XML_08A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_08A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_08A.zip"
    },
    "2023_TEOS_XML_09A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_09A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_09A.zip"
    },
    "2023_TEOS_XML_10A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_10A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_10A.zip"
    },
    "2023_TEOS_XML_11A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_11A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_11A.zip"
    },
    "2023_TEOS_XML_12A": {
        "ReleaseYear": "2023",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_12A.zip",
        "ReleaseDownload": "2025-03-09",
        "ReleaseFileName": "2023_TEOS_XML_12A.zip"
    },

    #2024

    "2024_TEOS_XML_01A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_01A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_01A.zip"
    },
    "2024_TEOS_XML_02A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_02A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_02A.zip"
    },
    "2024_TEOS_XML_03A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_03A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_03A.zip"
    },
    "2024_TEOS_XML_04A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_04A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_04A.zip"
    },
    "2024_TEOS_XML_05A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_05A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_05A.zip"
    },
    "2024_TEOS_XML_06A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_06A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_06A.zip"
    },
    "2024_TEOS_XML_07A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_07A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_07A.zip"
    },
    "2024_TEOS_XML_08A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_08A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_08A.zip"
    },
    "2024_TEOS_XML_09A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_09A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_09A.zip"
    },
    "2024_TEOS_XML_10A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_10A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_10A.zip"
    },
    "2024_TEOS_XML_11A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_11A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_11A.zip"
    },
    "2024_TEOS_XML_12A": {
        "ReleaseYear": "2024",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_12A.zip",
        "ReleaseDownload": "2025-03-11",
        "ReleaseFileName": "2024_TEOS_XML_12A.zip"
    },

    #2025

    "2025_TEOS_XML_01A": {
        "ReleaseYear": "2025",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_01A.zip",
        "ReleaseDownload": "2025-04-29",
        "ReleaseFileName": "2025_TEOS_XML_01A.zip"
    },
    "2025_TEOS_XML_02A": {
        "ReleaseYear": "2025",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_02A.zip",
        "ReleaseDownload": "2025-04-29",
        "ReleaseFileName": "2025_TEOS_XML_02A.zip"
    },
    "2025_TEOS_XML_03A": {
        "ReleaseYear": "2025",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_03A.zip",
        "ReleaseDownload": "2025-04-29",
        "ReleaseFileName": "2025_TEOS_XML_03A.zip"  
    },
    "2025_TEOS_XML_04A": {
        "ReleaseYear": "2025",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_04A.zip",
        "ReleaseDownload": "2025-07-17",
        "ReleaseFileName": "2025_TEOS_XML_04A.zip"
    },
    "2025_TEOS_XML_05A": {
        "ReleaseYear": "2025",
        "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2025/2025_TEOS_XML_05A.zip",
        "ReleaseDownload": "2025-07-17",
        "ReleaseFileName": "2025_TEOS_XML_05A.zip"
    },
}

    # These lists ("release_columns" all the way to "columns_order") tell pandas which columns to include and in what order
    # They correspond to pieces of data we will pull out of each XML file
# Release columns
release_columns = [
    "ReleaseYear",
    "ReleaseSource",
    "ReleaseDownload",
    "ReleaseFileName",
]

# Base Metadata
base_columns = [
    "FileName", "TaxPeriodBeginDt", "TaxPeriodEndDt", "TaxYr", "PreparationDt",
    "Filer_EIN", "Filer_BusinessName", "Filer_BusinessNameControlTxt", "Filer_PhoneNum",
    "Filer_AddressLine1Txt", "Filer_CityNm", "Filer_StateAbbreviationCd", "Filer_ZIPCd", "Filer_Country"
]

# “Outside” core 990 fields
outside_fields = [
    "TotalEmployeeCnt",
    "TotalGrossUBIAmt",
    "NetUnrelatedBusTxblIncmAmt",
    "PYContributionsGrantsAmt",
    "CYContributionsGrantsAmt",
    "PYProgramServiceRevenueAmt",
    "CYProgramServiceRevenueAmt",
    "PYInvestmentIncomeAmt",
    "CYInvestmentIncomeAmt",
    "PYOtherRevenueAmt",
    "CYOtherRevenueAmt",
    "PYTotalRevenueAmt",
    "CYTotalRevenueAmt",
    "PYGrantsAndSimilarPaidAmt",
    "CYGrantsAndSimilarPaidAmt",
    "PYBenefitsPaidToMembersAmt",
    "CYBenefitsPaidToMembersAmt",
    "PYSalariesCompEmpBnftPaidAmt",
    "CYSalariesCompEmpBnftPaidAmt",
    "PYTotalProfFndrsngExpnsAmt",
    "CYTotalProfFndrsngExpnsAmt",
    "CYTotalFundraisingExpenseAmt",
    "PYOtherExpensesAmt",
    "CYOtherExpensesAmt",
    "PYTotalExpensesAmt",
    "CYTotalExpensesAmt",
    "PYRevenuesLessExpensesAmt",
    "CYRevenuesLessExpensesAmt",
    "TotalAssetsBOYAmt",
    "TotalAssetsEOYAmt",
    "TotalLiabilitiesBOYAmt",
    "TotalLiabilitiesEOYAmt",
    "NetAssetsOrFundBalancesBOYAmt",
    "NetAssetsOrFundBalancesEOYAmt",
]

# Part I – Basic FAP & Inds
part1_basic_fields = [
    "FinancialAssistancePolicy",
    "WrittenPolicyInd",
    "HospitalPolicyInd_AllHospitalsPolicyInd",
    "HospitalPolicyInd_MostHospitalsPolicyInd",
    "HospitalPolicyInd_IndivHospitalTailoredPolicyInd",
    "FPGReferenceFreeCareInd_Percent100Ind",
    "FPGReferenceFreeCareInd_Percent150Ind",
    "FPGReferenceFreeCareInd_Percent200Ind",
    "FPGReferenceFreeCareInd_FreeCareOtherPct",
    "FPGReferenceDiscountedCareInd_Percent200DInd",
    "FPGReferenceDiscountedCareInd_Percent250Ind",
    "FPGReferenceDiscountedCareInd_Percent300Ind",
    "FPGReferenceDiscountedCareInd_Percent350Ind",
    "FPGReferenceDiscountedCareInd_Percent400Ind",
    "FPGReferenceDiscountedCareInd_DiscountedCareOthPercentageGrp",
    "FreeCareMedicallyIndigentInd",
    "FinancialAssistanceBudgetInd",
    "ExpensesExceedBudgetInd",
    "UnableToProvideCareInd",
    "AnnualCommunityBnftReportInd",
    "ReportPublicallyAvailableInd",
]

fa_at_cost_fields = [
    "FinancialAssistanceAtCostTyp_TotalCommunityBenefitExpnsAmt",
    "FinancialAssistanceAtCostTyp_DirectOffsettingRevenueAmt",
    "FinancialAssistanceAtCostTyp_NetCommunityBenefitExpnsAmt",
    "FinancialAssistanceAtCostTyp_TotalExpensePct"
]
unreimbursed_fields = [
    "UnreimbursedMedicaidGrp_TotalCommunityBenefitExpnsAmt",
    "UnreimbursedMedicaidGrp_DirectOffsettingRevenueAmt",
    "UnreimbursedMedicaidGrp_NetCommunityBenefitExpnsAmt",
    "UnreimbursedMedicaidGrp_TotalExpensePct"
]
other_means_tested_fields = [
    "UnreimbursedCostsGrp_TotalCommunityBenefitExpnsAmt",
    "UnreimbursedCostsGrp_DirectOffsettingRevenueAmt",
    "UnreimbursedCostsGrp_NetCommunityBenefitExpnsAmt",
    "UnreimbursedCostsGrp_TotalExpensePct"
]
total_fa_fields = [
    "TotalFinancialAssistanceTyp_TotalCommunityBenefitExpnsAmt",
    "TotalFinancialAssistanceTyp_DirectOffsettingRevenueAmt",
    "TotalFinancialAssistanceTyp_NetCommunityBenefitExpnsAmt",
    "TotalFinancialAssistanceTyp_TotalExpensePct"
]
community_health_fields = [
    "CommunityHealthServicesGrp_TotalCommunityBenefitExpnsAmt",
    "CommunityHealthServicesGrp_DirectOffsettingRevenueAmt",
    "CommunityHealthServicesGrp_NetCommunityBenefitExpnsAmt",
    "CommunityHealthServicesGrp_TotalExpensePct"
]
health_prof_fields = [
    "HealthProfessionsEducationGrp_TotalCommunityBenefitExpnsAmt",
    "HealthProfessionsEducationGrp_DirectOffsettingRevenueAmt",
    "HealthProfessionsEducationGrp_NetCommunityBenefitExpnsAmt",
    "HealthProfessionsEducationGrp_TotalExpensePct"
]
subsidized_fields = [
    "SubsidizedHealthServicesGrp_TotalCommunityBenefitExpnsAmt",
    "SubsidizedHealthServicesGrp_DirectOffsettingRevenueAmt",
    "SubsidizedHealthServicesGrp_NetCommunityBenefitExpnsAmt",
    "SubsidizedHealthServicesGrp_TotalExpensePct"
]
research_fields = [
    "ResearchGrp_TotalCommunityBenefitExpnsAmt",
    "ResearchGrp_DirectOffsettingRevenueAmt",
    "ResearchGrp_NetCommunityBenefitExpnsAmt",
    "ResearchGrp_TotalExpensePct"
]
cash_in_kind_fields = [
    "CashAndInKindContributionsGrp_TotalCommunityBenefitExpnsAmt",
    "CashAndInKindContributionsGrp_DirectOffsettingRevenueAmt",
    "CashAndInKindContributionsGrp_NetCommunityBenefitExpnsAmt",
    "CashAndInKindContributionsGrp_TotalExpensePct"
]
total_other_fields = [
    "TotalOtherBenefitsGrp_TotalCommunityBenefitExpnsAmt",
    "TotalOtherBenefitsGrp_DirectOffsettingRevenueAmt",
    "TotalOtherBenefitsGrp_NetCommunityBenefitExpnsAmt",
    "TotalOtherBenefitsGrp_TotalExpensePct"
]
total_community_fields = [
    "TotalCommunityBenefitsGrp_TotalCommunityBenefitExpnsAmt",
    "TotalCommunityBenefitsGrp_DirectOffsettingRevenueAmt",
    "TotalCommunityBenefitsGrp_NetCommunityBenefitExpnsAmt",
    "TotalCommunityBenefitsGrp_TotalExpensePct"
]

# Part II – Detailed Community Building
part2_cb_physical = [
    "PhysicalImprvAndHousingGrp_TotalCommunityBenefitExpnsAmt",
    "PhysicalImprvAndHousingGrp_DirectOffsettingRevenueAmt",
    "PhysicalImprvAndHousingGrp_NetCommunityBenefitExpnsAmt",
    "PhysicalImprvAndHousingGrp_TotalExpensePct"
]
part2_cb_economic = [
    "EconomicDevelopmentGrp_TotalCommunityBenefitExpnsAmt",
    "EconomicDevelopmentGrp_DirectOffsettingRevenueAmt",
    "EconomicDevelopmentGrp_NetCommunityBenefitExpnsAmt",
    "EconomicDevelopmentGrp_TotalExpensePct"
]
part2_cb_communitysupport = [
    "CommunitySupportGrp_TotalCommunityBenefitExpnsAmt",
    "CommunitySupportGrp_DirectOffsettingRevenueAmt",
    "CommunitySupportGrp_NetCommunityBenefitExpnsAmt",
    "CommunitySupportGrp_TotalExpensePct"
]
part2_cb_environment = [
    "EnvironmentalImprovementsGrp_TotalCommunityBenefitExpnsAmt",
    "EnvironmentalImprovementsGrp_DirectOffsettingRevenueAmt",
    "EnvironmentalImprovementsGrp_NetCommunityBenefitExpnsAmt",
    "EnvironmentalImprovementsGrp_TotalExpensePct"
]
part2_cb_leadership = [
    "LeadershipDevelopmentGrp_TotalCommunityBenefitExpnsAmt",
    "LeadershipDevelopmentGrp_DirectOffsettingRevenueAmt",
    "LeadershipDevelopmentGrp_NetCommunityBenefitExpnsAmt",
    "LeadershipDevelopmentGrp_TotalExpensePct"
]
part2_cb_coalition = [
    "CoalitionBuildingGrp_TotalCommunityBenefitExpnsAmt",
    "CoalitionBuildingGrp_DirectOffsettingRevenueAmt",
    "CoalitionBuildingGrp_NetCommunityBenefitExpnsAmt",
    "CoalitionBuildingGrp_TotalExpensePct"
]
part2_cb_healthadv = [
    "HealthImprovementAdvocacyGrp_TotalCommunityBenefitExpnsAmt",
    "HealthImprovementAdvocacyGrp_DirectOffsettingRevenueAmt",
    "HealthImprovementAdvocacyGrp_NetCommunityBenefitExpnsAmt",
    "HealthImprovementAdvocacyGrp_TotalExpensePct"
]
part2_cb_workforce = [
    "WorkforceDevelopmentGrp_TotalCommunityBenefitExpnsAmt",
    "WorkforceDevelopmentGrp_DirectOffsettingRevenueAmt",
    "WorkforceDevelopmentGrp_NetCommunityBenefitExpnsAmt",
    "WorkforceDevelopmentGrp_TotalExpensePct"
]
part2_cb_otheracty = [
    "OtherCommuntityBuildingActyGrp_TotalCommunityBenefitExpnsAmt",
    "OtherCommuntityBuildingActyGrp_DirectOffsettingRevenueAmt",
    "OtherCommuntityBuildingActyGrp_NetCommunityBenefitExpnsAmt",
    "OtherCommuntityBuildingActyGrp_TotalExpensePct"
]
part2_cb_total = [
    "TotalCommuntityBuildingActyGrp_TotalCommunityBenefitExpnsAmt",
    "TotalCommuntityBuildingActyGrp_DirectOffsettingRevenueAmt",
    "TotalCommuntityBuildingActyGrp_NetCommunityBenefitExpnsAmt",
    "TotalCommuntityBuildingActyGrp_TotalExpensePct"
]

# Part III – Bad Debt, Medicare & Collection
part3_fields = [
    "BadDebtExpenseReportedInd",
    "BadDebtExpenseAmt",
    "BadDebtExpenseAttributableAmt",
    "ReimbursedByMedicareAmt",
    "CostOfCareReimbursedByMedcrAmt",
    "MedicareSurplusOrShortfallAmt",
    "CostAccountingSystemInd",
    "CostToChargeRatioInd",
    "CostingMethodologyOtherInd",
    "CHNAOtherInd",
    "WrittenDebtCollectionPolicyInd",
    "FinancialAssistancePrvsnInd",
]

# Part IV – Management Companies & Joint Ventures
part4_fields = [
    "ManagementCompany_BusinessNameLine1Txt",
    "ManagementCompany_PrimaryActivitiesTxt",
    "ManagementCompany_OrgProfitOrOwnershipPct",
    "ManagementCompany_OfcrEtcProfitOrOwnershipPct",
    "ManagementCompany_PhysiciansProfitOrOwnershipPct",
]

# Part V – Facility Info
facility_info_fields = [
    "HospitalFacilitiesCnt",
    "HospitalFacilitiesGrp",
    "FacilityNum1BusinessName",
    "FacilityNum1Street",
    "FacilityNum1City",
    "FacilityNum1State",
    "FacilityNum1ZIP",
    "FacilityNum1Country",
    "FacilityNum2BusinessName",
    "FacilityNum2Street",
    "FacilityNum2City",
    "FacilityNum2State",
    "FacilityNum2ZIP",
    "FacilityNum2Country",
    "SubordinateHospitalName",
    "SubordinateHospitalEIN",
    "LicensedHospitalInd",
    "GeneralMedicalAndSurgicalInd",
    "ChildrensHospitalInd",
    "TeachingHospitalInd",
    "CriticalAccessHospitalInd",
    "ResearchFacilityInd",
]

# Additional Facility Policy fields
policy_extra_fields = [
    "FirstLicensedCYOrPYInd",
    "TaxExemptHospitalCYOrPYInd",
    "CHNAConductedInd",
    "CommunityDefinitionInd",
    "CommunityDemographicsInd",
    "ExistingResourcesInd",
    "HowDataObtainedInd",
    "CommunityHealthNeedsInd",
    "OtherHealthIssuesInd",
    "CommunityHlthNeedsIdProcessInd",
    "ConsultingProcessInd",
    "PriorCHNAImpactInd",
    "CHNAConductedYr",
    "TakeIntoAccountOthersInputInd",
    "CHNAConductedWithOtherFcltsInd",
    "CHNAConductedWithNonFcltsInd",
    "CHNAReportWidelyAvailableInd",
    "RptAvailableOnOwnWebsiteInd",
    "OwnWebsiteURLTxt",
    "OtherWebsiteInd",
    "OtherWebsiteURLTxt",
    "PaperCopyPublicInspectionInd",
    "RptAvailableThruOtherMethodInd",
    "ImplementationStrategyAdoptInd",
    "ImplementationStrategyAdptYr",
    "StrategyPostedWebsiteInd",
    "StrategyWebsiteURLTxt",
    "StrategyAttachedInd",
    "BinaryAttachment",
    "OrganizationIncurExciseTaxInd",
    "Form4720FiledInd",
    "ExciseReportForm4720ForAllAmt",
    "EligCriteriaExplainedInd",
    "FPGFamilyIncmLmtFreeDscntInd",
    "FPGFamilyIncmLmtFreeCarePct",
    "FPGFamilyIncmLmtDscntCarePct",
    "IncomeLevelCriteriaInd",
    "AssetLevelCriteriaInd",
    "MedicalIndigencyCriteriaInd",
    "InsuranceStatusCriteriaInd",
    "UnderinsuranceStatCriteriaInd",
    "ResidencyCriteriaInd",
    "OtherCriteriaInd",
    "ExplainedBasisInd",
    "AppFinancialAsstExplnInd",
    "DescribedInfoInd",
    "DescribedSuprtDocInd",
    "ProvidedHospitalContactInd",
    "ProvidedNonprofitContactInd",
    "OtherMethodInd",
    "IncludesPublicityMeasuresInd",
    "FAPAvailableOnWebsiteInd",
    "FAPAvailableOnWebsiteURLTxt",
    "FAPAppAvailableOnWebsiteInd",
    "FAPAppAvailableOnWebsiteURLTxt",
    "FAPSummaryOnWebsiteInd",
    "FAPSummaryOnWebsiteURLTxt",
    "FAPAvlblOnRequestNoChargeInd",
    "FAPAppAvlblOnRequestNoChrgInd",
    "FAPSumAvlblOnRequestNoChrgInd",
    "NotifiedFAPCopyBillDisplayInd",
    "CommuntityNotifiedFAPInd",
    "FAPTranslatedInd",
    "OtherPublicityInd",
    "FAPActionsOnNonpaymentInd",
    "PermitReportToCreditAgencyInd",
    "PermitSellingDebtInd",
    "PermitDeferDenyRqrPaymentInd",
    "PermitLegalJudicialProcessInd",
    "PermitOtherActionsInd",
    "PermitNoActionsInd",
    "CollectionActivitiesInd",
    "ReportingToCreditAgencyInd",
    "EngagedSellingDebtInd",
    "EngageDeferDenyRqrPaymentInd",
    "EngagedLegalJudicialProcessInd",
    "OtherActionsInd",
    "ProvidedWrittenNoticeInd",
    "MadeEffortOrallyNotifyInd",
    "ProcessedFAPApplicationInd",
    "MadePresumptiveEligDetermInd",
    "OtherActionsTakenInd",
    "NoneMadeInd",
    "NondisEmergencyCarePolicyInd",
    "NoEmergencyCareInd",
    "NoEmergencyCarePolicyInd",
    "EmergencyCareLimitedInd",
    "OtherReasonInd",
    "LookBackMedicareInd",
    "LookBackMedicarePrivateInd",
    "LookBackMedicaidMedcrPrvtInd",
    "ProspectiveMedicareMedicaidInd",
    "AmountsGenerallyBilledInd",
    "GrossChargesInd",
]

# Part V – Non-Hospital Healthcare Facilities
other_facilities_fields = [
    "OthHlthCareFcltsGrp_BusinessName",
    "OthHlthCareFcltsGrp_AddressLine1Txt",
    "OthHlthCareFcltsGrp_CityNm",
    "OthHlthCareFcltsGrp_StateAbbreviationCd",
    "OthHlthCareFcltsGrp_ZIPCd",
]

# Final column order
columns_order = (
    release_columns
    + base_columns
    + outside_fields
    + part1_basic_fields
    + fa_at_cost_fields
    + unreimbursed_fields
    + other_means_tested_fields
    + total_fa_fields
    + community_health_fields
    + health_prof_fields
    + subsidized_fields
    + research_fields
    + cash_in_kind_fields
    + total_other_fields
    + total_community_fields
    + part2_cb_physical
    + part2_cb_economic
    + part2_cb_communitysupport
    + part2_cb_environment
    + part2_cb_leadership
    + part2_cb_coalition
    + part2_cb_healthadv
    + part2_cb_workforce
    + part2_cb_otheracty
    + part2_cb_total
    + part3_fields
    + part4_fields
    + facility_info_fields
    + policy_extra_fields
    + ["SupplementalFacilityNum"]
    + other_facilities_fields
)

    # Mapping Dictionary: Long XML variable names to abbreviated SAS variable names
    # After extracting data with the long XML tag names,
    # we rename columns (variables) to more concise identifiers for output.
rename_dict = {
    "ReleaseYear": "IRS_RELEASEYEAR",
    "ReleaseSource": "IRS_RELEASESITE",
    "ReleaseDownload": "IRS_RELEASEDOWN",
    "ReleaseFileName": "IRS_RELEASETEOS",
    "FileName": "IRS_RELEASEXML",
    "TaxPeriodBeginDt": "IRS_TAXPERBEGDT",
    "TaxPeriodEndDt": "IRS_TAXPERENDDT",
    "TaxYr": "IRS_TAXYEAR",
    "PreparationDt": "IRS_PREPAREDT",
    "Filer_EIN": "IRS_FILER_EIN",
    "Filer_BusinessName": "IRS_FLRBUSNAME",
    "Filer_BusinessNameControlTxt": "IRS_FLRBUSNMTXT",
    "Filer_PhoneNum": "IRS_FLRPHONENUM",
    "Filer_AddressLine1Txt": "IRS_FLRADDRESS",
    "Filer_CityNm": "IRS_FLRCITYNAME",
    "Filer_StateAbbreviationCd": "IRS_FLRSTATEABB",
    "Filer_ZIPCd": "IRS_FLRZIPCODE",
    "Filer_Country": "IRS_FLRCOUNTRY",
    "TotalEmployeeCnt": "IRS_TOTEMPCNT",
    "TotalGrossUBIAmt": "IRS_TOTGRUBIAMT",
    "NetUnrelatedBusTxblIncmAmt": "IRS_NETUBIAMT",
    "PYContributionsGrantsAmt": "IRS_PYCNTGRTAMT",
    "CYContributionsGrantsAmt": "IRS_CYCNTGRTAMT",
    "PYProgramServiceRevenueAmt": "IRS_PYPSREVAMT",
    "CYProgramServiceRevenueAmt": "IRS_CYPSREVAMT",
    "PYInvestmentIncomeAmt": "IRS_PYINVINCAMT",
    "CYInvestmentIncomeAmt": "IRS_CYINVINCAMT",
    "PYOtherRevenueAmt": "IRS_PYOTHREVAMT",
    "CYOtherRevenueAmt": "IRS_CYOTHREVAMT",
    "PYTotalRevenueAmt": "IRS_PYTOTREVAMT",
    "CYTotalRevenueAmt": "IRS_CYTOTREVAMT",
    "PYGrantsAndSimilarPaidAmt": "IRS_PYGASPAIAMT",
    "CYGrantsAndSimilarPaidAmt": "IRS_CYGASPAIAMT",
    "PYBenefitsPaidToMembersAmt": "IRS_PYBENPTMAMT",
    "CYBenefitsPaidToMembersAmt": "IRS_CYBENPTMAMT",
    "PYSalariesCompEmpBnftPaidAmt": "IRS_PYSCEBPAMT",
    "CYSalariesCompEmpBnftPaidAmt": "IRS_CYSCEBPAMT",
    "PYTotalProfFndrsngExpnsAmt": "IRS_PYTPFEXPAMT",
    "CYTotalProfFndrsngExpnsAmt": "IRS_CYTPFEXPAMT",
    "CYTotalFundraisingExpenseAmt": "IRS_CYTFEXPAMT",
    "PYOtherExpensesAmt": "IRS_PYOTHEXPAMT",
    "CYOtherExpensesAmt": "IRS_CYOTHEXPAMT",
    "PYTotalExpensesAmt": "IRS_PYTOTEXPAMT",
    "CYTotalExpensesAmt": "IRS_CYTOTEXPAMT",
    "PYRevenuesLessExpensesAmt": "IRS_PYREVLEXAMT",
    "CYRevenuesLessExpensesAmt": "IRS_CYREVLEXAMT",
    "TotalAssetsBOYAmt": "IRS_TLASSBOYAMT",
    "TotalAssetsEOYAmt": "IRS_TLASSEOYAMT",
    "TotalLiabilitiesBOYAmt": "IRS_TLLBLBOYAMT",
    "TotalLiabilitiesEOYAmt": "IRS_TLLBLEOYAMT",
    "NetAssetsOrFundBalancesBOYAmt": "IRS_NAOFBBOYAMT",
    "NetAssetsOrFundBalancesEOYAmt": "IRS_NAOFBEOYAMT",
    "FinancialAssistancePolicy": "IRS_FNASPOLYN",
    "WrittenPolicyInd": "IRS_FAPWRTNYN",
    "HospitalPolicyInd_AllHospitalsPolicyInd": "IRS_FAPALLHSP",
    "HospitalPolicyInd_MostHospitalsPolicyInd": "IRS_FAPMSTHSP",
    "HospitalPolicyInd_IndivHospitalTailoredPolicyInd": "IRS_FAPTLRHSP",
    "FPGReferenceFreeCareInd_Percent100Ind": "IRS_FAPFCPG100",
    "FPGReferenceFreeCareInd_Percent150Ind": "IRS_FAPFCPG150",
    "FPGReferenceFreeCareInd_Percent200Ind": "IRS_FAPFCPG200",
    "FPGReferenceFreeCareInd_FreeCareOtherPct": "IRS_FAPFCPGOTH",
    "FPGReferenceDiscountedCareInd_Percent200DInd": "IRS_FAPDCPG200",
    "FPGReferenceDiscountedCareInd_Percent250Ind": "IRS_FAPDCPG250",
    "FPGReferenceDiscountedCareInd_Percent300Ind": "IRS_FAPDCPG300",
    "FPGReferenceDiscountedCareInd_Percent350Ind": "IRS_FAPDCPG350",
    "FPGReferenceDiscountedCareInd_Percent400Ind": "IRS_FAPDCPG400",
    "FPGReferenceDiscountedCareInd_DiscountedCareOthPercentageGrp": "IRS_FAPDCPGOTH",
    "FreeCareMedicallyIndigentInd": "IRS_FDCRMEDIND",
    "FinancialAssistanceBudgetInd": "IRS_FNASBDGT",
    "ExpensesExceedBudgetInd": "IRS_EXPEXCBDGT",
    "UnableToProvideCareInd": "IRS_UNTOPRFDCR",
    "AnnualCommunityBnftReportInd": "IRS_PRANCMBNRT",
    "ReportPublicallyAvailableInd": "IRS_CBRPUBAVL",
    "FinancialAssistanceAtCostTyp_TotalCommunityBenefitExpnsAmt": "IRS_FAACTCBEA",
    "FinancialAssistanceAtCostTyp_DirectOffsettingRevenueAmt": "IRS_FAACDORVA",
    "FinancialAssistanceAtCostTyp_NetCommunityBenefitExpnsAmt": "IRS_FAACNCBEA",
    "FinancialAssistanceAtCostTyp_TotalExpensePct": "IRS_FAACNCBEP",
    "UnreimbursedMedicaidGrp_TotalCommunityBenefitExpnsAmt": "IRS_UMCDTCBEA",
    "UnreimbursedMedicaidGrp_DirectOffsettingRevenueAmt": "IRS_UMCDDORVA",
    "UnreimbursedMedicaidGrp_NetCommunityBenefitExpnsAmt": "IRS_UMCDNCBEA",
    "UnreimbursedMedicaidGrp_TotalExpensePct": "IRS_UMCDNCBEP",
    "UnreimbursedCostsGrp_TotalCommunityBenefitExpnsAmt": "IRS_OMTGTCBEA",
    "UnreimbursedCostsGrp_DirectOffsettingRevenueAmt": "IRS_OMTGDORVA",
    "UnreimbursedCostsGrp_NetCommunityBenefitExpnsAmt": "IRS_OMTGNCBEA",
    "UnreimbursedCostsGrp_TotalExpensePct": "IRS_OMTGNCBEP",
    "TotalFinancialAssistanceTyp_TotalCommunityBenefitExpnsAmt": "IRS_TFMTCBEA",
    "TotalFinancialAssistanceTyp_DirectOffsettingRevenueAmt": "IRS_TFMTDORVA",
    "TotalFinancialAssistanceTyp_NetCommunityBenefitExpnsAmt": "IRS_TFMTNCBEA",
    "TotalFinancialAssistanceTyp_TotalExpensePct": "IRS_TFMTNCBEP",
    "CommunityHealthServicesGrp_TotalCommunityBenefitExpnsAmt": "IRS_CHISTCBEA",
    "CommunityHealthServicesGrp_DirectOffsettingRevenueAmt": "IRS_CHISDORVA",
    "CommunityHealthServicesGrp_NetCommunityBenefitExpnsAmt": "IRS_CHISNCBEA",
    "CommunityHealthServicesGrp_TotalExpensePct": "IRS_CHISNCBEP",
    "HealthProfessionsEducationGrp_TotalCommunityBenefitExpnsAmt": "IRS_HPEDTCBEA",
    "HealthProfessionsEducationGrp_DirectOffsettingRevenueAmt": "IRS_HPEDDORVA",
    "HealthProfessionsEducationGrp_NetCommunityBenefitExpnsAmt": "IRS_HPEDNCBEA",
    "HealthProfessionsEducationGrp_TotalExpensePct": "IRS_HPEDNCBEP",
    "SubsidizedHealthServicesGrp_TotalCommunityBenefitExpnsAmt": "IRS_SBHSTCBEA",
    "SubsidizedHealthServicesGrp_DirectOffsettingRevenueAmt": "IRS_SBHSDORVA",
    "SubsidizedHealthServicesGrp_NetCommunityBenefitExpnsAmt": "IRS_SBHSNCBEA",
    "SubsidizedHealthServicesGrp_TotalExpensePct": "IRS_SBHSNCBEP",
    "ResearchGrp_TotalCommunityBenefitExpnsAmt": "IRS_RSCHTCBEA",
    "ResearchGrp_DirectOffsettingRevenueAmt": "IRS_RSCHDORVA",
    "ResearchGrp_NetCommunityBenefitExpnsAmt": "IRS_RSCHNCBEA",
    "ResearchGrp_TotalExpensePct": "IRS_RSCHNCBEP",
    "CashAndInKindContributionsGrp_TotalCommunityBenefitExpnsAmt": "IRS_CIKCTCBEA",
    "CashAndInKindContributionsGrp_DirectOffsettingRevenueAmt": "IRS_CIKCDORVA",
    "CashAndInKindContributionsGrp_NetCommunityBenefitExpnsAmt": "IRS_CIKCNCBEA",
    "CashAndInKindContributionsGrp_TotalExpensePct": "IRS_CIKCNCBEP",
    "TotalOtherBenefitsGrp_TotalCommunityBenefitExpnsAmt": "IRS_TOBNTCBEA",
    "TotalOtherBenefitsGrp_DirectOffsettingRevenueAmt": "IRS_TOBNDORVA",
    "TotalOtherBenefitsGrp_NetCommunityBenefitExpnsAmt": "IRS_TOBNNCBEA",
    "TotalOtherBenefitsGrp_TotalExpensePct": "IRS_TOBNNCBEP",
    "TotalCommunityBenefitsGrp_TotalCommunityBenefitExpnsAmt": "IRS_TCBNTCBEA",
    "TotalCommunityBenefitsGrp_DirectOffsettingRevenueAmt": "IRS_TCBNDORVA",
    "TotalCommunityBenefitsGrp_NetCommunityBenefitExpnsAmt": "IRS_TCBNNCBEA",
    "TotalCommunityBenefitsGrp_TotalExpensePct": "IRS_TCBNNCBEP",
    "PhysicalImprvAndHousingGrp_TotalCommunityBenefitExpnsAmt": "IRS_PIAHTCBEA",
    "PhysicalImprvAndHousingGrp_DirectOffsettingRevenueAmt": "IRS_PIAHDORVA",
    "PhysicalImprvAndHousingGrp_NetCommunityBenefitExpnsAmt": "IRS_PIAHNCBEA",
    "PhysicalImprvAndHousingGrp_TotalExpensePct": "IRS_PIAHNCBEP",
    "EconomicDevelopmentGrp_TotalCommunityBenefitExpnsAmt": "IRS_ECDVTCBEA",
    "EconomicDevelopmentGrp_DirectOffsettingRevenueAmt": "IRS_ECDVDORVA",
    "EconomicDevelopmentGrp_NetCommunityBenefitExpnsAmt": "IRS_ECDVNCBEA",
    "EconomicDevelopmentGrp_TotalExpensePct": "IRS_ECDVNCBEP",
    "CommunitySupportGrp_TotalCommunityBenefitExpnsAmt": "IRS_CSPTTCBEA",
    "CommunitySupportGrp_DirectOffsettingRevenueAmt": "IRS_CSPTDORVA",
    "CommunitySupportGrp_NetCommunityBenefitExpnsAmt": "IRS_CSPTNCBEA",
    "CommunitySupportGrp_TotalExpensePct": "IRS_CSPTNCBEP",
    "EnvironmentalImprovementsGrp_TotalCommunityBenefitExpnsAmt": "IRS_ENVITCBEA",
    "EnvironmentalImprovementsGrp_DirectOffsettingRevenueAmt": "IRS_ENVIDORVA",
    "EnvironmentalImprovementsGrp_NetCommunityBenefitExpnsAmt": "IRS_ENVINCBEA",
    "EnvironmentalImprovementsGrp_TotalExpensePct": "IRS_ENVINCBEP",
    "LeadershipDevelopmentGrp_TotalCommunityBenefitExpnsAmt": "IRS_LDATTCBEA",
    "LeadershipDevelopmentGrp_DirectOffsettingRevenueAmt": "IRS_LDATDORVA",
    "LeadershipDevelopmentGrp_NetCommunityBenefitExpnsAmt": "IRS_LDATNCBEA",
    "LeadershipDevelopmentGrp_TotalExpensePct": "IRS_LDATNCBEP",
    "CoalitionBuildingGrp_TotalCommunityBenefitExpnsAmt": "IRS_CBLDTCBEA",
    "CoalitionBuildingGrp_DirectOffsettingRevenueAmt": "IRS_CBLDDORVA",
    "CoalitionBuildingGrp_NetCommunityBenefitExpnsAmt": "IRS_CBLDNCBEA",
    "CoalitionBuildingGrp_TotalExpensePct": "IRS_CBLDNCBEP",
    "HealthImprovementAdvocacyGrp_TotalCommunityBenefitExpnsAmt": "IRS_CHAITCBEA",
    "HealthImprovementAdvocacyGrp_DirectOffsettingRevenueAmt": "IRS_CHAIDORVA",
    "HealthImprovementAdvocacyGrp_NetCommunityBenefitExpnsAmt": "IRS_CHAINCBEA",
    "HealthImprovementAdvocacyGrp_TotalExpensePct": "IRS_CHAINCBEP",
    "WorkforceDevelopmentGrp_TotalCommunityBenefitExpnsAmt": "IRS_WKDVTCBEA",
    "WorkforceDevelopmentGrp_DirectOffsettingRevenueAmt": "IRS_WKDVDORVA",
    "WorkforceDevelopmentGrp_NetCommunityBenefitExpnsAmt": "IRS_WKDVNCBEA",
    "WorkforceDevelopmentGrp_TotalExpensePct": "IRS_WKDVNCBEP",
    "OtherCommuntityBuildingActyGrp_TotalCommunityBenefitExpnsAmt": "IRS_OCBATCBEA",
    "OtherCommuntityBuildingActyGrp_DirectOffsettingRevenueAmt": "IRS_OCBADORVA",
    "OtherCommuntityBuildingActyGrp_NetCommunityBenefitExpnsAmt": "IRS_OCBANCBEA",
    "OtherCommuntityBuildingActyGrp_TotalExpensePct": "IRS_OCBANCBEP",
    "TotalCommuntityBuildingActyGrp_TotalCommunityBenefitExpnsAmt": "IRS_TCBATCBEA",
    "TotalCommuntityBuildingActyGrp_DirectOffsettingRevenueAmt": "IRS_TCBADORVA",
    "TotalCommuntityBuildingActyGrp_NetCommunityBenefitExpnsAmt": "IRS_TCBANCBEA",
    "TotalCommuntityBuildingActyGrp_TotalExpensePct": "IRS_TCBANCBEP",
    "BadDebtExpenseReportedInd": "IRS_RPBDHFMA15",
    "BadDebtExpenseAmt": "IRS_BADDBTTLAMT",
    "BadDebtExpenseAttributableAmt": "IRS_BADDBTATFAP",
    "ReimbursedByMedicareAmt": "IRS_TTLMCRREV",
    "CostOfCareReimbursedByMedcrAmt": "IRS_TTLMCRCST",
    "MedicareSurplusOrShortfallAmt": "IRS_TTLMCRSRPLS",
    "CostAccountingSystemInd": "IRS_MCRCMUCAS",
    "CostToChargeRatioInd": "IRS_MCRCMUCCR",
    "CostingMethodologyOtherInd": "IRS_MCRCMUOTH",
    "WrittenDebtCollectionPolicyInd": "IRS_DBTCOLWRT",
    "FinancialAssistancePrvsnInd": "IRS_DBTCOLFAP",
    "ManagementCompany_BusinessNameLine1Txt": "IRS_MCJVNAME",
    "ManagementCompany_PrimaryActivitiesTxt": "IRS_MCJVDOPA",
    "ManagementCompany_OrgProfitOrOwnershipPct": "IRS_MJORGPRFPCT",
    "ManagementCompany_OfcrEtcProfitOrOwnershipPct": "IRS_MJODTPRFPCT",
    "ManagementCompany_PhysiciansProfitOrOwnershipPct": "IRS_MJMDSPRFPCT",
    "HospitalFacilitiesCnt": "IRS_TOTCNTFCLTY",
    "HospitalFacilitiesGrp": "IRS_LSTALLFCLTY",
    "FacilityNum1BusinessName": "IRS_FC1BUSNAME",
    "FacilityNum1Street": "IRS_FC1ADDRESS",
    "FacilityNum1City": "IRS_FC1CITYNAME",
    "FacilityNum1State": "IRS_FC1STATEABB",
    "FacilityNum1ZIP": "IRS_FC1ZIPCODE",
    "FacilityNum1Country": "IRS_FC1COUNTRY",
    "FacilityNum2BusinessName": "IRS_FC2BUSNAME",
    "FacilityNum2Street": "IRS_FC2ADDRESS",
    "FacilityNum2City": "IRS_FC2CITYNAME",
    "FacilityNum2State": "IRS_FC2STATEABB",
    "FacilityNum2ZIP": "IRS_FC2ZIPCODE",
    "FacilityNum2Country": "IRS_FC2COUNTRY",
    "SubordinateHospitalName": "IRS_SUBHSPNAME",
    "SubordinateHospitalEIN": "IRS_SUBHSPEIN",
    "LicensedHospitalInd": "IRS_FCISLICHSP",
    "GeneralMedicalAndSurgicalInd": "IRS_FCISGMSHSP",
    "ChildrensHospitalInd": "IRS_FCISCLDHSP",
    "TeachingHospitalInd": "IRS_FCISTCHHSP",
    "CriticalAccessHospitalInd": "IRS_FCISCRAHSP",
    "ResearchFacilityInd": "IRS_FCISRSRCHF",
    "FirstLicensedCYOrPYInd": "IRS_CHNAVB1",
    "TaxExemptHospitalCYOrPYInd": "IRS_CHNAVB2",
    "CHNAConductedInd": "IRS_CHNAVB3",
    "CommunityDefinitionInd": "IRS_CHNAVB3A",
    "CommunityDemographicsInd": "IRS_CHNAVB3B",
    "ExistingResourcesInd": "IRS_CHNAVB3C",
    "HowDataObtainedInd": "IRS_CHNAVB3D",
    "CommunityHealthNeedsInd": "IRS_CHNAVB3E",
    "OtherHealthIssuesInd": "IRS_CHNAVB3F",
    "CommunityHlthNeedsIdProcessInd": "IRS_CHNAVB3G",
    "ConsultingProcessInd": "IRS_CHNAVB3H",
    "PriorCHNAImpactInd": "IRS_CHNAVB3I",
    "CHNAOtherInd": "IRS_CHNAVB3J",
    "CHNAConductedYr": "IRS_CHNAVB4",
    "TakeIntoAccountOthersInputInd": "IRS_CHNAVB5",
    "CHNAConductedWithOtherFcltsInd": "IRS_CHNAVB6A",
    "CHNAConductedWithNonFcltsInd": "IRS_CHNAVB6B",
    "CHNAReportWidelyAvailableInd": "IRS_CHNAVB7",
    "RptAvailableOnOwnWebsiteInd": "IRS_CHNAVB7A",
    "OwnWebsiteURLTxt": "IRS_CHNAVB7AURL",
    "OtherWebsiteInd": "IRS_CHNAVB7B",
    "OtherWebsiteURLTxt": "IRS_CHNAVB7BURL",
    "PaperCopyPublicInspectionInd": "IRS_CHNAVB7C",
    "RptAvailableThruOtherMethodInd": "IRS_CHNAVB7D",
    "ImplementationStrategyAdoptInd": "IRS_CHNAVB8",
    "ImplementationStrategyAdptYr": "IRS_CHNAVB9",
    "StrategyPostedWebsiteInd": "IRS_CHNAVB10",
    "StrategyWebsiteURLTxt": "IRS_CHNAVB10A",
    "StrategyAttachedInd": "IRS_CHNAVB10B",
    "BinaryAttachment": "IRS_CHNAVB10B2",
    "OrganizationIncurExciseTaxInd": "IRS_CHNAVB12A",
    "Form4720FiledInd": "IRS_CHNAVB12B",
    "ExciseReportForm4720ForAllAmt": "IRS_CHNAVB12C",
    "EligCriteriaExplainedInd": "IRS_FAPVB13",
    "FPGFamilyIncmLmtFreeDscntInd": "IRS_FAPVB13A",
    "FPGFamilyIncmLmtFreeCarePct": "IRS_FAPVB13AFC",
    "FPGFamilyIncmLmtDscntCarePct": "IRS_FAPVB13ADC",
    "IncomeLevelCriteriaInd": "IRS_FAPVB13B",
    "AssetLevelCriteriaInd": "IRS_FAPVB13C",
    "MedicalIndigencyCriteriaInd": "IRS_FAPVB13D",
    "InsuranceStatusCriteriaInd": "IRS_FAPVB13E",
    "UnderinsuranceStatCriteriaInd": "IRS_FAPVB13F",
    "ResidencyCriteriaInd": "IRS_FAPVB13G",
    "OtherCriteriaInd": "IRS_FAPVB13H",
    "ExplainedBasisInd": "IRS_FAPVB14",
    "AppFinancialAsstExplnInd": "IRS_FAPVB15",
    "DescribedInfoInd": "IRS_FAPVB15A",
    "DescribedSuprtDocInd": "IRS_FAPVB15B",
    "ProvidedHospitalContactInd": "IRS_FAPVB15C",
    "ProvidedNonprofitContactInd": "IRS_FAPVB15D",
    "OtherMethodInd": "IRS_FAPVB15E",
    "IncludesPublicityMeasuresInd": "IRS_FAPVB16",
    "FAPAvailableOnWebsiteInd": "IRS_FAPVB16A",
    "FAPAvailableOnWebsiteURLTxt": "IRS_FAPVB16AURL",
    "FAPAppAvailableOnWebsiteInd": "IRS_FAPVB16B",
    "FAPAppAvailableOnWebsiteURLTxt": "IRS_FAPVB16BURL",
    "FAPSummaryOnWebsiteInd": "IRS_FAPVB16C",
    "FAPSummaryOnWebsiteURLTxt": "IRS_FAPVB16CURL",
    "FAPAvlblOnRequestNoChargeInd": "IRS_FAPVB16D",
    "FAPAppAvlblOnRequestNoChrgInd": "IRS_FAPVB16E",
    "FAPSumAvlblOnRequestNoChrgInd": "IRS_FAPVB16F",
    "NotifiedFAPCopyBillDisplayInd": "IRS_FAPVB16G",
    "CommuntityNotifiedFAPInd": "IRS_FAPVB16H",
    "FAPTranslatedInd": "IRS_FAPVB16I",
    "OtherPublicityInd": "IRS_FAPVB16J",
    "FAPActionsOnNonpaymentInd": "IRS_BACVB17",
    "PermitReportToCreditAgencyInd": "IRS_BACVB18A",
    "PermitSellingDebtInd": "IRS_BACVB18B",
    "PermitDeferDenyRqrPaymentInd": "IRS_BACVB18C",
    "PermitLegalJudicialProcessInd": "IRS_BACVB18D",
    "PermitOtherActionsInd": "IRS_BACVB18E",
    "PermitNoActionsInd": "IRS_BACVB18F",
    "CollectionActivitiesInd": "IRS_BACVB19",
    "ReportingToCreditAgencyInd": "IRS_BACVB19A",
    "EngagedSellingDebtInd": "IRS_BACVB19B",
    "EngageDeferDenyRqrPaymentInd": "IRS_BACVB19C",
    "EngagedLegalJudicialProcessInd": "IRS_BACVB19D",
    "OtherActionsInd": "IRS_BACVB19E",
    "ProvidedWrittenNoticeInd": "IRS_BACVB20A",
    "MadeEffortOrallyNotifyInd": "IRS_BACVB20B",
    "ProcessedFAPApplicationInd": "IRS_BACVB20C",
    "MadePresumptiveEligDetermInd": "IRS_BACVB20D",
    "OtherActionsTakenInd": "IRS_BACVB20E",
    "NoneMadeInd": "IRS_BACVB20F",
    "NondisEmergencyCarePolicyInd": "IRS_EMCVB21",
    "NoEmergencyCareInd": "IRS_EMCVB21A",
    "NoEmergencyCarePolicyInd": "IRS_EMCVB21B",
    "EmergencyCareLimitedInd": "IRS_EMCVB21C",
    "OtherReasonInd": "IRS_EMCVB21D",
    "LookBackMedicareInd": "IRS_EMCVB22A",
    "LookBackMedicarePrivateInd": "IRS_EMCVB22B",
    "LookBackMedicaidMedcrPrvtInd": "IRS_EMCVB22C",
    "ProspectiveMedicareMedicaidInd": "IRS_EMCVB22D",
    "AmountsGenerallyBilledInd": "IRS_EMCVB23",
    "GrossChargesInd": "IRS_EMCVB24",
    "SupplementalFacilityNum": "IRS_TOTCNTOHF",
    "OthHlthCareFcltsGrp_BusinessName": "IRS_OHFBUSNAME",
    "OthHlthCareFcltsGrp_AddressLine1Txt": "IRS_OHFADDRESS",
    "OthHlthCareFcltsGrp_CityNm": "IRS_OHFCITYNAME",
    "OthHlthCareFcltsGrp_StateAbbreviationCd": "IRS_OHFSTATEABB",
    "OthHlthCareFcltsGrp_ZIPCd": "IRS_OHFZIPCODE",
}

    # Helper functions
    # These small functions each do one job:
    #  - get_text: Safely read text from an XML element
    #  - parse_bool, parse_fpg_reference, parse_dcop: Standardize certain values
    #  - extract_group_fields: Pull a set of sub-elements from one XML group
    #  - check_policy: Detect if a policy tag is marked with an X
    #  - check_policy: Typically indicicates a variable thats "checked" in the IRS filing rather than a numerical line item
def get_text(tag):
    return tag.text.strip() if tag and tag.text else None

def parse_bool(value):
    """Convert raw tag text to a standardized 'Yes' or 'No'."""
    if value is None:
        return "No"
    val = str(value).strip().upper()
    if val in {"X", "1", "TRUE"}:
        return "Yes"
    return "No"

def parse_fpg_reference(value):
    if value is None or value.strip() == "":
        return "Not Provided"
    v = value.strip().lower()
    if v in {"true", "1", "x"}:
        return "TRUE"
    elif v in {"false", "0"}:
        return "FALSE"
    else:
        return value

def parse_dcop(value):
    if value is None or value.strip() == "":
        return "Not Provided"
    return value

def extract_group_fields(soup, group_name, subfields, prefix):
    """
    Generic function to find a group (e.g. <CommunitySupportGrp>)
    and extract subfields (<TotalCommunityBenefitExpnsAmt>, etc.)
    """
    group = soup.find(group_name)
    data = {}
    if group:
        for sub in subfields:
            data[f"{prefix}_{sub}"] = get_text(group.find(sub))
    else:
        for sub in subfields:
            data[f"{prefix}_{sub}"] = None
    return data

def check_policy(tag):
    """Return True if the tag exists and its text contains an 'X'."""
    text = get_text(tag)
    return text is not None and "X" in text

    # SCHEDULE H EXTRACTION
    # This function handles the many Schedule H sections in one place.
    # It returns a dictionary of all Schedule H variables for one filing
def extract_scheduleH_data(soup):
    """
    Extract variables from the IRS990ScheduleH XML.
    """
    sch_data = {}

    # PART I: Basic FAP & Inds
    sch_data["FinancialAssistancePolicy"] = get_text(soup.find("FinancialAssistancePolicyInd"))
    sch_data["WrittenPolicyInd"] = get_text(soup.find("WrittenPolicyInd"))
    sch_data["HospitalPolicyInd_AllHospitalsPolicyInd"] = get_text(soup.find("AllHospitalsPolicyInd"))
    sch_data["HospitalPolicyInd_MostHospitalsPolicyInd"] = get_text(soup.find("MostHospitalsPolicyInd"))
    sch_data["HospitalPolicyInd_IndivHospitalTailoredPolicyInd"] = get_text(soup.find("IndivHospitalTailoredPolicyInd"))

    sch_data["FPGReferenceFreeCareInd_Percent100Ind"] = get_text(soup.find("Percent100Ind"))
    sch_data["FPGReferenceFreeCareInd_Percent150Ind"] = get_text(soup.find("Percent150Ind"))
    sch_data["FPGReferenceFreeCareInd_Percent200Ind"] = get_text(soup.find("Percent200Ind"))
    sch_data["FPGReferenceFreeCareInd_FreeCareOtherPct"] = get_text(soup.find("FreeCareOtherPct"))

    sch_data["FPGReferenceDiscountedCareInd_Percent200DInd"] = get_text(soup.find("Percent200DInd"))
    sch_data["FPGReferenceDiscountedCareInd_Percent250Ind"] = get_text(soup.find("Percent250Ind"))
    sch_data["FPGReferenceDiscountedCareInd_Percent300Ind"] = get_text(soup.find("Percent300Ind"))
    sch_data["FPGReferenceDiscountedCareInd_Percent350Ind"] = get_text(soup.find("Percent350Ind"))
    sch_data["FPGReferenceDiscountedCareInd_Percent400Ind"] = get_text(soup.find("Percent400Ind"))

    disc_grp = soup.find("DiscountedCareOthPercentageGrp")
    if disc_grp:
        raw_dcop = get_text(disc_grp.find("DiscountedCareOtherPct"))
        sch_data["FPGReferenceDiscountedCareInd_DiscountedCareOthPercentageGrp"] = parse_dcop(raw_dcop)
    else:
        sch_data["FPGReferenceDiscountedCareInd_DiscountedCareOthPercentageGrp"] = None

    sch_data["FreeCareMedicallyIndigentInd"] = get_text(soup.find("FreeCareMedicallyIndigentInd"))
    sch_data["FinancialAssistanceBudgetInd"] = get_text(soup.find("FinancialAssistanceBudgetInd"))
    sch_data["ExpensesExceedBudgetInd"] = get_text(soup.find("ExpensesExceedBudgetInd"))
    sch_data["UnableToProvideCareInd"] = get_text(soup.find("UnableToProvideCareInd"))
    sch_data["AnnualCommunityBnftReportInd"] = get_text(soup.find("AnnualCommunityBnftReportInd"))
    sch_data["ReportPublicallyAvailableInd"] = get_text(soup.find("ReportPublicallyAvailableInd"))

    # PART I: Lines 7a - 7k
    sch_data.update(extract_group_fields(
        soup, "FinancialAssistanceAtCostTyp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "FinancialAssistanceAtCostTyp"
    ))
    sch_data.update(extract_group_fields(
        soup, "UnreimbursedMedicaidGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "UnreimbursedMedicaidGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "UnreimbursedCostsGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "UnreimbursedCostsGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "TotalFinancialAssistanceTyp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "TotalFinancialAssistanceTyp"
    ))
    sch_data.update(extract_group_fields(
        soup, "CommunityHealthServicesGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "CommunityHealthServicesGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "HealthProfessionsEducationGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "HealthProfessionsEducationGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "SubsidizedHealthServicesGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "SubsidizedHealthServicesGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "ResearchGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "ResearchGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "CashAndInKindContributionsGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "CashAndInKindContributionsGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "TotalOtherBenefitsGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "TotalOtherBenefitsGrp"
    ))
    sch_data.update(extract_group_fields(
        soup, "TotalCommunityBenefitsGrp",
        ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
        "TotalCommunityBenefitsGrp"
    ))

    # PART II – Detailed Community Building
    for grp_name in [
        "PhysicalImprvAndHousingGrp", "EconomicDevelopmentGrp", "CommunitySupportGrp",
        "EnvironmentalImprovementsGrp", "LeadershipDevelopmentGrp", "CoalitionBuildingGrp",
        "HealthImprovementAdvocacyGrp", "WorkforceDevelopmentGrp", "OtherCommuntityBuildingActyGrp",
        "TotalCommuntityBuildingActyGrp"
    ]:
        sch_data.update(extract_group_fields(
            soup, grp_name,
            ["TotalCommunityBenefitExpnsAmt", "DirectOffsettingRevenueAmt", "NetCommunityBenefitExpnsAmt", "TotalExpensePct"],
            grp_name
        ))

    # PART III – Bad Debt, Medicare & Collection
    sch_data["BadDebtExpenseReportedInd"] = get_text(soup.find("BadDebtExpenseReportedInd"))
    sch_data["BadDebtExpenseAmt"] = get_text(soup.find("BadDebtExpenseAmt"))
    sch_data["BadDebtExpenseAttributableAmt"] = get_text(soup.find("BadDebtExpenseAttributableAmt"))
    sch_data["ReimbursedByMedicareAmt"] = get_text(soup.find("ReimbursedByMedicareAmt"))
    sch_data["CostOfCareReimbursedByMedcrAmt"] = get_text(soup.find("CostOfCareReimbursedByMedcrAmt"))
    sch_data["MedicareSurplusOrShortfallAmt"] = get_text(soup.find("MedicareSurplusOrShortfallAmt"))
    sch_data["CostAccountingSystemInd"] = get_text(soup.find("CostAccountingSystemInd"))
    sch_data["CostToChargeRatioInd"] = get_text(soup.find("CostToChargeRatioInd"))
    

    # 1) Medicare‐“Other” comes from <CostingMethodologyUsedGrp><OtherInd>
    cmu_grp = soup.find("CostingMethodologyUsedGrp")
    sch_data["CostingMethodologyOtherInd"]      = get_text(cmu_grp.find("OtherInd")) if cmu_grp else None

    # 2) CHNA “Other” comes from <HospitalFcltyPoliciesPrctcGrp><OtherInd>
    policy_grp = soup.find("HospitalFcltyPoliciesPrctcGrp")
    sch_data["CHNAOtherInd"]                    = get_text(policy_grp.find("OtherInd")) if policy_grp else None

    sch_data["WrittenDebtCollectionPolicyInd"]  = get_text(soup.find("WrittenDebtCollectionPolicyInd"))
    sch_data["FinancialAssistancePrvsnInd"]     = get_text(soup.find("FinancialAssistancePrvsnInd"))

    # PART IV – Management Companies
    mngmt = soup.find("ManagementCoAndJntVenturesGrp")
    if mngmt:
        sch_data["ManagementCompany_BusinessNameLine1Txt"] = get_text(mngmt.find("BusinessNameLine1Txt"))
        sch_data["ManagementCompany_PrimaryActivitiesTxt"] = get_text(mngmt.find("PrimaryActivitiesTxt"))
        sch_data["ManagementCompany_OrgProfitOrOwnershipPct"] = get_text(mngmt.find("OrgProfitOrOwnershipPct"))
        sch_data["ManagementCompany_OfcrEtcProfitOrOwnershipPct"] = get_text(mngmt.find("OfcrEtcProfitOrOwnershipPct"))
        sch_data["ManagementCompany_PhysiciansProfitOrOwnershipPct"] = get_text(mngmt.find("PhysiciansProfitOrOwnershipPct"))
    else:
        for key in [
            "ManagementCompany_BusinessNameLine1Txt",
            "ManagementCompany_PrimaryActivitiesTxt",
            "ManagementCompany_OrgProfitOrOwnershipPct",
            "ManagementCompany_OfcrEtcProfitOrOwnershipPct",
            "ManagementCompany_PhysiciansProfitOrOwnershipPct"
        ]:
            sch_data[key] = None

    # PART V – Facility Info
    sch_data["HospitalFacilitiesCnt"] = get_text(soup.find("HospitalFacilitiesCnt"))
    facilities_grp = soup.find_all("HospitalFacilitiesGrp")
    if facilities_grp:
        fac_list = []
        for fac in facilities_grp:
            fnum = get_text(fac.find("FacilityNum"))
            bn_tag = fac.find("BusinessName")
            bn = get_text(bn_tag.find("BusinessNameLine1Txt")) if bn_tag else ""
            fac_list.append(f"{fnum}|{bn}")
        sch_data["HospitalFacilitiesGrp"] = ";".join(fac_list)
    else:
        sch_data["HospitalFacilitiesGrp"] = None

    for i in range(2):
        sch_data[f"FacilityNum{i+1}BusinessName"] = None
        sch_data[f"FacilityNum{i+1}Street"] = None
        sch_data[f"FacilityNum{i+1}City"] = None
        sch_data[f"FacilityNum{i+1}State"] = None
        sch_data[f"FacilityNum{i+1}ZIP"] = None
        sch_data[f"FacilityNum{i+1}Country"] = None

    for idx, fac in enumerate(facilities_grp[:2]):
        bn_tag = fac.find("BusinessName")
        bn = get_text(bn_tag.find("BusinessNameLine1Txt")) if bn_tag else None
        addr = fac.find("USAddress")
        if addr:
            street = get_text(addr.find("AddressLine1Txt"))
            city = get_text(addr.find("CityNm"))
            state = get_text(addr.find("StateAbbreviationCd"))
            zip_code = get_text(addr.find("ZIPCd"))
            country = "USA"
        else:
            street = city = state = zip_code = country = None
        sch_data[f"FacilityNum{idx+1}BusinessName"] = bn
        sch_data[f"FacilityNum{idx+1}Street"] = street
        sch_data[f"FacilityNum{idx+1}City"] = city
        sch_data[f"FacilityNum{idx+1}State"] = state
        sch_data[f"FacilityNum{idx+1}ZIP"] = zip_code
        sch_data[f"FacilityNum{idx+1}Country"] = country

    sch_data["SubordinateHospitalName"] = get_text(soup.find("SubordinateHospitalName"))
    sch_data["SubordinateHospitalEIN"] = get_text(soup.find("SubordinateHospitalEIN"))
    sch_data["LicensedHospitalInd"] = get_text(soup.find("LicensedHospitalInd"))
    sch_data["GeneralMedicalAndSurgicalInd"] = get_text(soup.find("GeneralMedicalAndSurgicalInd"))
    sch_data["ChildrensHospitalInd"] = get_text(soup.find("ChildrensHospitalInd"))
    sch_data["TeachingHospitalInd"] = get_text(soup.find("TeachingHospitalInd"))
    sch_data["CriticalAccessHospitalInd"] = get_text(soup.find("CriticalAccessHospitalInd"))
    sch_data["ResearchFacilityInd"] = get_text(soup.find("ResearchFacilityInd"))

    # PART V – Facility Policies
    policy_grp = soup.find("HospitalFcltyPoliciesPrctcGrp")
    if policy_grp:
        for field in policy_extra_fields:
            sch_data[field] = get_text(policy_grp.find(field))
    else:
        for field in policy_extra_fields:
            sch_data[field] = None

    # PART V – Non-Hospital Healthcare Facilities
    not_hosp_grp = soup.find("OthHlthCareFcltsNotHospitalGrp")
    if not_hosp_grp:
        ohc_grp = not_hosp_grp.find("OthHlthCareFcltsGrp")
        if ohc_grp:
            sch_data["OthHlthCareFcltsGrp_BusinessName"] = get_text(ohc_grp.find("BusinessNameLine1Txt"))
            addr = ohc_grp.find("USAddress")
            if addr:
                sch_data["OthHlthCareFcltsGrp_AddressLine1Txt"] = get_text(addr.find("AddressLine1Txt"))
                sch_data["OthHlthCareFcltsGrp_CityNm"] = get_text(addr.find("CityNm"))
                sch_data["OthHlthCareFcltsGrp_StateAbbreviationCd"] = get_text(addr.find("StateAbbreviationCd"))
                sch_data["OthHlthCareFcltsGrp_ZIPCd"] = get_text(addr.find("ZIPCd"))
            else:
                sch_data["OthHlthCareFcltsGrp_AddressLine1Txt"] = None
                sch_data["OthHlthCareFcltsGrp_CityNm"] = None
                sch_data["OthHlthCareFcltsGrp_StateAbbreviationCd"] = None
                sch_data["OthHlthCareFcltsGrp_ZIPCd"] = None
        else:
            for x in [
                "OthHlthCareFcltsGrp_BusinessName",
                "OthHlthCareFcltsGrp_AddressLine1Txt",
                "OthHlthCareFcltsGrp_CityNm",
                "OthHlthCareFcltsGrp_StateAbbreviationCd",
                "OthHlthCareFcltsGrp_ZIPCd",
            ]:
                sch_data[x] = None
    else:
        for x in [
            "OthHlthCareFcltsGrp_BusinessName",
            "OthHlthCareFcltsGrp_AddressLine1Txt",
            "OthHlthCareFcltsGrp_CityNm",
            "OthHlthCareFcltsGrp_StateAbbreviationCd",
            "OthHlthCareFcltsGrp_ZIPCd",
        ]:
            sch_data[x] = None

    return sch_data

    # EXTRACT DATA
    # This function ties together reading one XML, pulling metadata,
    # calling extract_scheduleH_data, and packaging everything as one row
def extract_data(xml_file, ReleaseYear, ReleaseSource, ReleaseDownload, ReleaseFileName):
    try:
        with open(xml_file, "r", encoding="utf-8") as file:
            content = file.read()
        soup = BeautifulSoup(content, "xml")

        # BASE METADATA
        base = {}
        base["FileName"] = os.path.basename(xml_file)
        base["TaxPeriodBeginDt"] = get_text(soup.find("TaxPeriodBeginDt"))
        base["TaxPeriodEndDt"] = get_text(soup.find("TaxPeriodEndDt"))
        base["TaxYr"] = get_text(soup.find("TaxYr"))
        base["PreparationDt"] = get_text(soup.find("PreparationDt"))

        filer = soup.find("Filer")
        if filer:
            base["Filer_EIN"] = get_text(filer.find("EIN"))
            bn = filer.find("BusinessName")
            base["Filer_BusinessName"] = get_text(bn.find("BusinessNameLine1Txt")) if bn else None
            base["Filer_BusinessNameControlTxt"] = get_text(filer.find("BusinessNameControlTxt"))
            base["Filer_PhoneNum"] = get_text(filer.find("PhoneNum"))
            us_addr = filer.find("USAddress")
            foreign_addr = filer.find("ForeignAddress")
            if us_addr:
                base["Filer_AddressLine1Txt"] = get_text(us_addr.find("AddressLine1Txt"))
                base["Filer_CityNm"] = get_text(us_addr.find("CityNm"))
                base["Filer_StateAbbreviationCd"] = get_text(us_addr.find("StateAbbreviationCd"))
                base["Filer_ZIPCd"] = get_text(us_addr.find("ZIPCd"))
                base["Filer_Country"] = "USA"
            elif foreign_addr:
                base["Filer_AddressLine1Txt"] = get_text(foreign_addr.find("AddressLine1Txt"))
                base["Filer_CityNm"] = get_text(foreign_addr.find("CityNm"))
                base["Filer_StateAbbreviationCd"] = get_text(foreign_addr.find("ProvinceOrStateNm"))
                base["Filer_ZIPCd"] = get_text(foreign_addr.find("ForeignPostalCd"))
                base["Filer_Country"] = get_text(foreign_addr.find("CountryCd"))
            else:
                for key in [
                    "Filer_AddressLine1Txt", "Filer_CityNm", "Filer_StateAbbreviationCd",
                    "Filer_ZIPCd", "Filer_Country"
                ]:
                    base[key] = None
        else:
            for key in [
                "Filer_EIN", "Filer_BusinessName", "Filer_BusinessNameControlTxt", "Filer_PhoneNum",
                "Filer_AddressLine1Txt", "Filer_CityNm", "Filer_StateAbbreviationCd", "Filer_ZIPCd", "Filer_Country"
            ]:
                base[key] = None
       
        supp_info = soup.find("SupplementalInformationGrp")
        if supp_info:
            fac_tag = supp_info.find_next_sibling("FacilityNum")
            supplemental_facility_num = fac_tag.text.strip() if fac_tag and fac_tag.text else None
        else:
            supplemental_facility_num = None
        base["SupplementalFacilityNum"] = supplemental_facility_num

        # EXTRACT SCHEDULE H
        scheduleH_tag = soup.find("IRS990ScheduleH")
        if not scheduleH_tag:
            return None
        sch_data = extract_scheduleH_data(scheduleH_tag)

        # OUTSIDE fields
        outside_field_names = [
            "TotalEmployeeCnt",
            "TotalGrossUBIAmt",
            "NetUnrelatedBusTxblIncmAmt",
            "PYContributionsGrantsAmt",
            "CYContributionsGrantsAmt",
            "PYProgramServiceRevenueAmt",
            "CYProgramServiceRevenueAmt",
            "PYInvestmentIncomeAmt",
            "CYInvestmentIncomeAmt",
            "PYOtherRevenueAmt",
            "CYOtherRevenueAmt",
            "PYTotalRevenueAmt",
            "CYTotalRevenueAmt",
            "PYGrantsAndSimilarPaidAmt",
            "CYGrantsAndSimilarPaidAmt",
            "PYBenefitsPaidToMembersAmt",
            "CYBenefitsPaidToMembersAmt",
            "PYSalariesCompEmpBnftPaidAmt",
            "CYSalariesCompEmpBnftPaidAmt",
            "PYTotalProfFndrsngExpnsAmt",
            "CYTotalProfFndrsngExpnsAmt",
            "CYTotalFundraisingExpenseAmt",
            "PYOtherExpensesAmt",
            "CYOtherExpensesAmt",
            "PYTotalExpensesAmt",
            "CYTotalExpensesAmt",
            "PYRevenuesLessExpensesAmt",
            "CYRevenuesLessExpensesAmt",
            "TotalAssetsBOYAmt",
            "TotalAssetsEOYAmt",
            "TotalLiabilitiesBOYAmt",
            "TotalLiabilitiesEOYAmt",
            "NetAssetsOrFundBalancesBOYAmt",
            "NetAssetsOrFundBalancesEOYAmt",
        ]
        outside = {}
        for field in outside_field_names:
            outside[field] = get_text(soup.find(field))

        # Combine
        data = {}
        data.update(base)
        data.update(sch_data)
        data.update(outside)

        # Insert the 4 release columns
        data["ReleaseYear"] = ReleaseYear
        data["ReleaseSource"] = ReleaseSource
        data["ReleaseDownload"] = ReleaseDownload
        data["ReleaseFileName"] = ReleaseFileName

        # Return row in correct order
        return [data.get(col) for col in columns_order]

    except Exception as e:
        print(f"Error processing {xml_file}: {e}")
        return None

    # MAIN EXECUTION
    # This final block:
    #  - finds all yearly ZIP folders,
    #  - iterates through each XML in each folder,
    #  - builds a big list of rows,
    #  - then converts to a table and writes it out as a CSV.
print("Extracting...")

results = []

# 1) List all subfolders under parent_folder
subfolders = [
    os.path.join(parent_folder, sf)
    for sf in os.listdir(parent_folder)
    if os.path.isdir(os.path.join(parent_folder, sf))
]

# 2) Loop through each release folder
for subfolder_path in subfolders:
    subfolder_name = os.path.basename(subfolder_path)

    release_info = release_info_for_subfolder.get(subfolder_name, {
        "ReleaseYear": "",
        "ReleaseSource": "",
        "ReleaseDownload": "",
        "ReleaseFileName": ""
    })
    ReleaseYear     = release_info["ReleaseYear"]
    ReleaseSource   = release_info["ReleaseSource"]
    ReleaseDownload = release_info["ReleaseDownload"]
    ReleaseFileName = release_info["ReleaseFileName"]

    print(f"\nProcessing subfolder: {subfolder_path}")
    print(f" => Release Info: Year={ReleaseYear}, Source={ReleaseSource}, FileName={ReleaseFileName}")
    
    # 3) For each .xml file inside, call extract_data
    for file_name in tqdm(os.listdir(subfolder_path)):
        if not file_name.endswith(".xml"):
            continue
        xml_path = os.path.join(subfolder_path, file_name)
        row = extract_data(
            xml_file        = xml_path,
            ReleaseYear     = ReleaseYear,
            ReleaseSource   = ReleaseSource,
            ReleaseDownload = ReleaseDownload,
            ReleaseFileName = ReleaseFileName
        )
        if row:
            results.append(row)

# 4) After processing all, build a pandas DataFrame, rename columns, reorder, and save to CSV
if results:
    df = pd.DataFrame(results, columns=columns_order)
    df.rename(columns=rename_dict, inplace=True)

    desired_order = [
    "IRS_RELEASEYEAR","IRS_RELEASESITE","IRS_RELEASEDOWN","IRS_RELEASETEOS",
    "IRS_RELEASEXML","IRS_TAXPERBEGDT","IRS_TAXPERENDDT","IRS_TAXYEAR",
    "IRS_PREPAREDT","IRS_FILER_EIN","IRS_FLRBUSNAME","IRS_FLRBUSNMTXT",
    "IRS_FLRPHONENUM","IRS_FLRADDRESS","IRS_FLRCITYNAME","IRS_FLRSTATEABB",
    "IRS_FLRZIPCODE","IRS_FLRCOUNTRY","IRS_TOTEMPCNT","IRS_TOTGRUBIAMT",
    "IRS_NETUBIAMT","IRS_PYCNTGRTAMT","IRS_CYCNTGRTAMT","IRS_PYPSREVAMT",
    "IRS_CYPSREVAMT","IRS_PYINVINCAMT","IRS_CYINVINCAMT","IRS_PYOTHREVAMT",
    "IRS_CYOTHREVAMT","IRS_PYTOTREVAMT","IRS_CYTOTREVAMT","IRS_PYGASPAIAMT",
    "IRS_CYGASPAIAMT","IRS_PYBENPTMAMT","IRS_CYBENPTMAMT","IRS_PYSCEBPAMT",
    "IRS_CYSCEBPAMT","IRS_PYTPFEXPAMT","IRS_CYTPFEXPAMT","IRS_CYTFEXPAMT",
    "IRS_PYOTHEXPAMT","IRS_CYOTHEXPAMT","IRS_PYTOTEXPAMT","IRS_CYTOTEXPAMT",
    "IRS_PYREVLEXAMT","IRS_CYREVLEXAMT","IRS_TLASSBOYAMT","IRS_TLASSEOYAMT",
    "IRS_TLLBLBOYAMT","IRS_TLLBLEOYAMT","IRS_NAOFBBOYAMT","IRS_NAOFBEOYAMT",
    "IRS_FNASPOLYN","IRS_FAPWRTNYN","IRS_FAPALLHSP","IRS_FAPMSTHSP",
    "IRS_FAPTLRHSP","IRS_FAPFCPG100","IRS_FAPFCPG150","IRS_FAPFCPG200",
    "IRS_FAPFCPGOTH","IRS_FAPDCPG200","IRS_FAPDCPG250","IRS_FAPDCPG300",
    "IRS_FAPDCPG350","IRS_FAPDCPG400","IRS_FAPDCPGOTH","IRS_FDCRMEDIND",
    "IRS_FNASBDGT","IRS_EXPEXCBDGT","IRS_UNTOPRFDCR","IRS_PRANCMBNRT",
    "IRS_CBRPUBAVL","IRS_FAACTCBEA","IRS_FAACDORVA","IRS_FAACNCBEA",
    "IRS_FAACNCBEP","IRS_UMCDTCBEA","IRS_UMCDDORVA","IRS_UMCDNCBEA",
    "IRS_UMCDNCBEP","IRS_OMTGTCBEA","IRS_OMTGDORVA","IRS_OMTGNCBEA",
    "IRS_OMTGNCBEP","IRS_TFMTCBEA","IRS_TFMTDORVA","IRS_TFMTNCBEA",
    "IRS_TFMTNCBEP","IRS_CHISTCBEA","IRS_CHISDORVA","IRS_CHISNCBEA",
    "IRS_CHISNCBEP","IRS_HPEDTCBEA","IRS_HPEDDORVA","IRS_HPEDNCBEA",
    "IRS_HPEDNCBEP","IRS_SBHSTCBEA","IRS_SBHSDORVA","IRS_SBHSNCBEA",
    "IRS_SBHSNCBEP","IRS_RSCHTCBEA","IRS_RSCHDORVA","IRS_RSCHNCBEA",
    "IRS_RSCHNCBEP","IRS_CIKCTCBEA","IRS_CIKCDORVA","IRS_CIKCNCBEA",
    "IRS_CIKCNCBEP","IRS_TOBNTCBEA","IRS_TOBNDORVA","IRS_TOBNNCBEA",
    "IRS_TOBNNCBEP","IRS_TCBNTCBEA","IRS_TCBNDORVA","IRS_TCBNNCBEA",
    "IRS_TCBNNCBEP","IRS_PIAHTCBEA","IRS_PIAHDORVA","IRS_PIAHNCBEA",
    "IRS_PIAHNCBEP","IRS_ECDVTCBEA","IRS_ECDVDORVA","IRS_ECDVNCBEA",
    "IRS_ECDVNCBEP","IRS_CSPTTCBEA","IRS_CSPTDORVA","IRS_CSPTNCBEA",
    "IRS_CSPTNCBEP","IRS_ENVITCBEA","IRS_ENVIDORVA","IRS_ENVINCBEA",
    "IRS_ENVINCBEP","IRS_LDATTCBEA","IRS_LDATDORVA","IRS_LDATNCBEA",
    "IRS_LDATNCBEP","IRS_CBLDTCBEA","IRS_CBLDDORVA","IRS_CBLDNCBEA",
    "IRS_CBLDNCBEP","IRS_CHAITCBEA","IRS_CHAIDORVA","IRS_CHAINCBEA",
    "IRS_CHAINCBEP","IRS_WKDVTCBEA","IRS_WKDVDORVA","IRS_WKDVNCBEA",
    "IRS_WKDVNCBEP","IRS_OCBATCBEA","IRS_OCBADORVA","IRS_OCBANCBEA",
    "IRS_OCBANCBEP","IRS_TCBATCBEA","IRS_TCBADORVA","IRS_TCBANCBEA",
    "IRS_TCBANCBEP","IRS_RPBDHFMA15","IRS_BADDBTTLAMT","IRS_BADDBTATFAP",
    "IRS_TTLMCRREV","IRS_TTLMCRCST","IRS_TTLMCRSRPLS","IRS_MCRCMUCAS",
    "IRS_MCRCMUCCR","IRS_MCRCMUOTH","IRS_DBTCOLWRT","IRS_DBTCOLFAP",
    "IRS_MCJVNAME","IRS_MCJVDOPA","IRS_MJORGPRFPCT","IRS_MJODTPRFPCT",
    "IRS_MJMDSPRFPCT","IRS_TOTCNTFCLTY","IRS_LSTALLFCLTY","IRS_FC1BUSNAME",
    "IRS_FC1ADDRESS","IRS_FC1CITYNAME","IRS_FC1STATEABB","IRS_FC1ZIPCODE",
    "IRS_FC1COUNTRY","IRS_FC2BUSNAME","IRS_FC2ADDRESS","IRS_FC2CITYNAME",
    "IRS_FC2STATEABB","IRS_FC2ZIPCODE","IRS_FC2COUNTRY","IRS_SUBHSPNAME",
    "IRS_SUBHSPEIN","IRS_FCISLICHSP","IRS_FCISGMSHSP","IRS_FCISCLDHSP",
    "IRS_FCISTCHHSP","IRS_FCISCRAHSP","IRS_FCISRSRCHF","IRS_CHNAVB1",
    "IRS_CHNAVB2","IRS_CHNAVB3","IRS_CHNAVB3A","IRS_CHNAVB3B","IRS_CHNAVB3C",
    "IRS_CHNAVB3D","IRS_CHNAVB3E","IRS_CHNAVB3F","IRS_CHNAVB3G","IRS_CHNAVB3H",
    "IRS_CHNAVB3I","IRS_CHNAVB3J","IRS_CHNAVB4","IRS_CHNAVB5","IRS_CHNAVB6A",
    "IRS_CHNAVB6B","IRS_CHNAVB7","IRS_CHNAVB7A","IRS_CHNAVB7AURL","IRS_CHNAVB7B",
    "IRS_CHNAVB7BURL","IRS_CHNAVB7C","IRS_CHNAVB7D","IRS_CHNAVB8","IRS_CHNAVB9",
    "IRS_CHNAVB10","IRS_CHNAVB10A","IRS_CHNAVB10B","IRS_CHNAVB10B2",
    "IRS_CHNAVB12A","IRS_CHNAVB12B","IRS_CHNAVB12C","IRS_FAPVB13",
    "IRS_FAPVB13A","IRS_FAPVB13AFC","IRS_FAPVB13ADC","IRS_FAPVB13B",
    "IRS_FAPVB13C","IRS_FAPVB13D","IRS_FAPVB13E","IRS_FAPVB13F",
    "IRS_FAPVB13G","IRS_FAPVB13H","IRS_FAPVB14","IRS_FAPVB15","IRS_FAPVB15A",
    "IRS_FAPVB15B","IRS_FAPVB15C","IRS_FAPVB15D","IRS_FAPVB15E","IRS_FAPVB16",
    "IRS_FAPVB16A","IRS_FAPVB16AURL","IRS_FAPVB16B","IRS_FAPVB16BURL",
    "IRS_FAPVB16C","IRS_FAPVB16CURL","IRS_FAPVB16D","IRS_FAPVB16E",
    "IRS_FAPVB16F","IRS_FAPVB16G","IRS_FAPVB16H","IRS_FAPVB16I","IRS_FAPVB16J",
    "IRS_BACVB17","IRS_BACVB18A","IRS_BACVB18B","IRS_BACVB18C","IRS_BACVB18D",
    "IRS_BACVB18E","IRS_BACVB18F","IRS_BACVB19","IRS_BACVB19A","IRS_BACVB19B",
    "IRS_BACVB19C","IRS_BACVB19D","IRS_BACVB19E","IRS_BACVB20A","IRS_BACVB20B",
    "IRS_BACVB20C","IRS_BACVB20D","IRS_BACVB20E","IRS_BACVB20F","IRS_EMCVB21",
    "IRS_EMCVB21A","IRS_EMCVB21B","IRS_EMCVB21C","IRS_EMCVB21D","IRS_EMCVB22A",
    "IRS_EMCVB22B","IRS_EMCVB22C","IRS_EMCVB22D","IRS_EMCVB23","IRS_EMCVB24",
    "IRS_TOTCNTOHF","IRS_OHFBUSNAME","IRS_OHFADDRESS","IRS_OHFCITYNAME",
    "IRS_OHFSTATEABB","IRS_OHFZIPCODE"
]
    df = df[desired_order]

    df.to_csv(output_csv, index=False)
    print(f"\nExtraction complete! {len(df)} records saved to: {output_csv}")
else:
    print("\nNo valid data found to save.")