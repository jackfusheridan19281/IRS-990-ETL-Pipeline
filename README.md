# IRS Form 990 Schedule H ETL Pipeline

A Python ETL pipeline for extracting structured financial, community benefit, and hospital policy data from IRS Form 990 Schedule H XML filings and consolidating the results into CSV files for downstream analysis.

The pipeline processes batches of locally downloaded IRS XML filings, extracts Schedule H fields along with selected core Form 990 financial and filer information, attaches metadata for each IRS data release, standardizes the output schema, and combines the results into a single structured dataset.

IRS Form 990 XML releases can be downloaded from the [IRS Form 990 Series Downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads).

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The project uses:

- pandas
- beautifulsoup4
- tqdm

## Usage

### 1. Download and Extract IRS XML Releases

Download the desired Form 990 XML ZIP files from the IRS website and extract each release into its own subfolder.

The structure should look similar to:

```text
EIN zip files 2025/
├── 2025_TEOS_XML_01A/
├── 2025_TEOS_XML_02A/
├── 2025_TEOS_XML_03A/
└── ...
```

Each release folder should contain the corresponding `.xml` filings.

### 2. Configure the File Paths

Near the top of the script, update:

```python
parent_folder = r"C:\IRS990H_Parser\EIN zip files 2025"
output_csv = r"C:\IRS990H_Parser\csv output\IRS 990H 2025.csv"
```

`parent_folder` should point to the folder containing the extracted IRS release folders.

`output_csv` should specify the location and filename of the final CSV.

On Windows, you can use **Copy as path** in File Explorer and paste the path into the script. Keep the `r` before the path so Python treats it as a raw string.

### 3. Run the Script

Run the Python script after configuring the paths.

The pipeline will:

1. Identify each IRS release subfolder.
2. Match the folder to its release metadata.
3. Process each XML filing in the folder.
4. Parse eligible Form 990 Schedule H filings.
5. Extract and standardize the selected fields.
6. Combine all records into a pandas DataFrame.
7. Export the completed dataset to CSV.

## Data Extracted

The pipeline extracts structured fields covering areas including:

- IRS release and filing metadata
- Filer information
- Core Form 990 financial data
- Financial assistance policies
- Community benefit expenditures
- Community building activities
- Bad debt and Medicare information
- Management companies and joint ventures
- Hospital facility information
- Community Health Needs Assessments
- Billing and collection policies
- Non-hospital healthcare facilities

Output variables are standardized into abbreviated `IRS_` column names before export.

## Adding a New IRS Release

The script uses the `release_info_for_subfolder` dictionary to associate each local release folder with information about the original IRS ZIP file.

For a new release, add an entry following the existing structure:

```python
"2026_TEOS_XML_01A": {
    "ReleaseYear": "2026",
    "ReleaseSource": "https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_01A.zip",
    "ReleaseDownload": "2026-01-01",
    "ReleaseFileName": "2026_TEOS_XML_01A.zip"
},
```

Replace `ReleaseDownload` with the actual date the ZIP file was downloaded.

Each entry corresponds to one IRS ZIP release. If multiple releases are published during the year, add a separate entry for each release and extract each ZIP into its corresponding subfolder.

## Notes

IRS Form 990 XML releases are published throughout the year, so additional release folders and metadata entries may need to be added over time.

For better performance when processing large numbers of XML files, local storage is recommended over cloud-synced directories such as OneDrive.

The pipeline depends on the structure of IRS Form 990 XML filings. Changes to IRS XML schemas or release formats may require updates to the parsing logic.


If you have any questions, please reach out to my personal email. Good luck!

Jack Sheridan sheridanjack38@gmail.com
