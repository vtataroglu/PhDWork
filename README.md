[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![Bitcoin](https://img.shields.io/badge/Bitcoin-000?style=for-the-badge&logo=bitcoin&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) ![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)


This document outlines the data collection, preparation, and construction processes of the datasets used in my PhD research. The goal is to create stable, reusable, and easily testable datasets for use in our thesis and scholarly articles. The process is divided into eleven detailed steps, each contributing to the final dataset. These steps guide you through the sources of the data, how to access it either by downloading directly or using the pre-prepared zipped files in the downloaded data folder. Each step is described in the accompanying readme file, ensuring clarity and ease of use.

## Table of Contents
- [Step 1: Download Bitcoin Block Data from Website via Python](#step-1-download-block-data-from-website-via-python)
- [Step 2: Extract All Bitcoin Block Data](#step-2-extract-all-bitcoin-block-data)
- [Step 3: Testing Block Data Output](#step-3-testing-block-data-output)
- [Step 4: Importing tsv files to SQLite](#step-4-importing-tsv-files-to-sqlite)
- [Step 5: Creating API to query on Bitcoin Block in SQLite](#step-5-creating-api-to-query-on-bitcoin-block-in-sqlite)
- [Step 6: Importing 1-Minute Historical Bitcoin Price Data to SQLite](#step-6-importing-1-minute-historical-bitcoin-price-data-to-sqlite)
- [Step 7: Testing Bitcoin Price Data Output](#step-7-testing-bitcoin-price-data-output)
- [Step 8: Creating API to query on Historical Bitcoin Price in SQLite](#step-8-creating-api-to-query-on-historical-bitcoin-price-in-sqlite)
- [Step 9: Aggregate Bitcoin price data from 1-minute into 10-minute intervals](#step-9-aggregate-bitcoin-price-data-from-1-minute-into-10-minute-intervals)
- [Step 10: Creating new API Bitcoin price from 10-minute intervals data](#step-10-creating-new-api-bitcoin-price-from-10-minute-intervals-data)
- [Step 11: Summary of the Previous 10 Steps](#step-11-summary-of-the-previous-10-steps)

## Step 1: Download Block Data from Website via Python
**Code Link**: [Download All Block Data Script](https://github.com/vtataroglu/PhDWork/blob/main/download-all-block.py)

## Importing Libraries
The script uses the following Python libraries:
- `requests`: To send HTTP requests to a web server.
- `BeautifulSoup` from `bs4`: To parse HTML documents and extract data.
- `os`: To interact with the operating system, particularly to check file existence.
- `ThreadPoolExecutor` and `as_completed` from `concurrent.futures`: For handling multi-threaded downloads.

## Function Definitions

### fetch_and_parse_url
- **Purpose**: Makes an HTTP GET request to the provided URL.
- **Success**: If the response status is 200, the HTML content is parsed with BeautifulSoup and returned.
- **Failure**: Prints a failure message and returns None.

### extract_links
- **Purpose**: Processes a BeautifulSoup object (soup) that represents a parsed HTML document.
- **Function**: Extracts all `<a>` elements (hyperlinks) and filters them to include only those with a href that contains the substring "blockchair_bitcoin_blocks".
- **Returns**: A list of tuples where each tuple contains the link text and the href attribute.

### download_file
- **Purpose**: Attempts to download a file from a constructed URL using the href attribute.
- **Success**: Saves the file to the local file system with a name derived from the href.
- **Failure**: Tracks and prints an error message if the download fails.

### main
- **Setup**: Sets the target URL to parse.
- **Operations**:
  - Calls `fetch_and_parse_url` to get the parsed HTML content.
  - Calls `extract_links` to get a filtered list of download links.
  - Filters out links for files that already exist locally, preventing re-download.
  - Uses a `ThreadPoolExecutor` to download each file concurrently, with a specified maximum number of worker threads (10).
- **Tracking**: Prints the total number of files to download and the outcome of each download attempt.

## Execution
This script is intended to be run as a standalone Python program. When executed, it performs all the above operations in sequence.

## Usage Notes
This script is particularly useful for automating the download of a large number of files from a web page where the files are linked. It efficiently handles multiple downloads by using threading, which can significantly speed up the process compared to downloading files one at a time.

## Final Notes
Ensure you have permission to scrape and download data from the website you are targeting to avoid any legal issues. Websites might have terms of service that prohibit scraping, and ignoring these can result in IP bans or other penalties.

## Step 2: Extract All Bitcoin Block Data

To extract all .tsv.gz files from one directory to another in a bash script using a single line, you can use the following command:

```bash
for file in *.tsv.gz; do gzip -dc "$file" > /path/to/destination/"${file%.gz}"; done
```
> [!WARNING]  
If you cannot run the above Bash script on the Windows operating system, you can utilize this [Python code](https://github.com/vtataroglu/PhDWork/blob/main/extract-all-gz-files.py) instead. It will assist you with the extraction process.


## Step 3: Testing Block Data Output
**Code Link**: [Test Code](https://github.com/vtataroglu/PhDWork/blob/main/testing-data-output.py)

This Python script identifies the latest .tsv file in a specified directory, prints its name, and then displays the first three lines of its content in a Markdown code block. It starts by gathering all .tsv files from the specified directory, sorting them by filename in reverse alphabetical order, and selecting the top file from this sorted list as the latest. If such a file is found, the script prints its name and the first three lines. If no .tsv files are found, it outputs a message stating that no files were found in the directory. This script could be particularly useful for testing whether the data you are working with is the same as the data downloaded by others. The name of the most recent file is shared with you in the output below.


### Latest .tsv file: `/root/test/extracted/blockchair_bitcoin_blocks_20240414.tsv`
```
id      hash    time    median_time     size    stripped_size   weight  version version_hex     version_bits    merkle_root     nonce   bits    difficulty      chainwork     coinbase_data_hex       transaction_count       witness_count   input_count     output_count    input_total     input_total_usd output_total    output_total_usd      fee_total       fee_total_usd   fee_per_kb      fee_per_kb_usd  fee_per_kwu     fee_per_kwu_usd cdd_total       generation      generation_usd  reward  reward_usd    guessed_miner
839103  00000000000000000003275752e41b5f4d9505e27e342ae36544f26edf308162        2024-04-14 00:17:33     2024-04-13 23:10:09     1690307 767539  3992924 543162368    20600000 100000011000000000000000000000  59050f064d858ee17a6db4f72cb41429ce7579c4bcecb995a547107b034ead02        67787296        386089497       86388558925171  000000000000000000000000000000000000000074288c61e1fb266b96019ce0      03bfcd0c049d201b662f466f756e6472792055534120506f6f6c202364726f70676f6c642f3b0d29f5c109010000000000   2599     2491    6349    11550   2573863044631   1645213312      2574488044631   1645612800      97634918        62408.2383      57773.27        36.9285 24459.654    15.6348  50303.977867306 625000000       399500  722634918       461908.25       Foundry USA Pool
839104  00000000000000000002cbaa113f28a70279538880c452c826d424cc30e77977        2024-04-14 00:44:00     2024-04-13 23:11:23     1680667 770907  3993388 852934656    32d6c000 110010110101101100000000000000  dd4cdb76aae37fd8b945729ea93482a449014417b4a3dc4edb753081ff046e7a        3240672804      386089497       86388558925171  00000000000000000000000000000000000000007428daf417eb69cedc647dab      03c0cd0c194d696e656420627920416e74506f6f6c202f00e8032e1952ecfabe6d6d7b7df4f93c94ff83e795dfb522964582494a5dc4146105215b8ec93adfec1df71000000000000000000021749403000000000000  4080    3980    6161    11869   1633014203508   1043822656      1633639203508   1044222208   87996616 56247.4375      52372.953       33.4768 22045.47        14.0912 48353.186941121 625000000       399500  712996616       455747.4375     AntPool
839105  00000000000000000002ed4c0befeeba01b956780e4df16ba1f77857f48a2751        2024-04-14 01:09:25     2024-04-13 23:21:07     1694430 766244  3993162 872415232    34000000 110100000000000000000000000000  9ffb66a5f4452ada293bf704feba52a475ba5ca3d92e424d6ba292430fe7ed3f        28215261        386089497       86388558925171  0000000000000000000000000000000000000000742929864ddbad3222c75e76      03c1cd0c04c52c1b662f466f756e6472792055534120506f6f6c202364726f70676f6c642f3d5c91c12a14610000000000   3775     3710    5381    12040   436642073096    279101600       437267073096    279501120       119392380       76315.6094      70475.82        45.0483 29908.586    19.1178  36684.853408397 625000000       399500  744392380       475815.5938     Foundry USA Pool
839106  0000000000000000000182164f6c34b8f3fc8d80f72cace81ce69590da6b44a7        2024-04-14 01:27:56     2024-04-13 23:38:44     1693588 768145  3998023 838860800    32000000 110010000000000000000000000000  20506ffd75a378614ca4a65d1f4dfbd4b94dba37cd9157708b64ae525def1c87        704194401       386089497       86388558925171  00000000000000000000000000000000000000007429781883cbf095692a3f41      03c2cd0c2cfabe6d6dd838a18a2eeb9cc894b80213494730fff093c6e1c0af386bd96177796d140ae310000000f09f909f092f4632506f6f6c2f6400000000000000000000000000000000000000000000000000000000000000000000000500015cc4b3      4097    4025    5893    11490   428636197905    273984256    429261197905     274383744       110656311       70731.5156      65359.266       41.7775 27691.998       17.7007 55286.966325091 625000000       399500  735656311    470231.5 F2Pool
839107  000000000000000000022cbc49c886b11f71cf28a60880aaed453a299bc315d5        2024-04-14 01:42:53     2024-04-13 23:46:55     1697468 765366  3993566 568516608    21e2e000 100001111000101110000000000000  2a26c203d77c7bfcdc115f7fd54b70d139b1660731ba26c7e19b85f3ec7a366d        3750247439      386089497       86388558925171  00000000000000000000000000000000000000007429c6aab9bc33f8af8d200c      03c3cd0c1d506f7765726564206279204c75786f722054656368e6002e0443294d35fabe6d6d207d03c739571b29c0a679c526cc3c20fc527da64932efe5d0280b124b122c86100000000000000000004dd06012010000000000  3732    3600    6443    11169   330365553030    211169664       330990553030    211569168     99087071        63336.457       58389.93        37.3229 24822.916       15.8669 31329.498589994 625000000       399500  724087071       462836.4688     Unknown
839108  00000000000000000001a2aa8be2e20e257ce1bc4a62a4f205b29902b0ba3a6a        2024-04-14 01:49:23     2024-04-14 00:17:33     1701904 763750  3993154 611123200    246d0000 100100011011010000000000000000  94203f1aed923e98ff26a7ab798c2461e8998a97216383fe9c9cdaf28ef2f0fd        375728991       386089497       86388558925171  0000000000000000000000000000000000000000742a153cefac775bf5f000d7      03c4cd0c0f2f736c7573682f2f002602457bd4aefabe6d6d61107f9df2836ddf38b423dce8cf42a80bcbd7d913cad7cc095ccd2f2d59e601100000000000000000001e996900f48400000000      3433    3325    6786    11182   237264055182    151659184       237889055182    152058688       77227221     49363.6406       45387.008       29.0114 19346.688       12.3666 57780.207937012 625000000       399500  702227221       448863.625      SlushPool
839109  000000000000000000015541a3291d7bc3943af403495f945dd678b4d0cabdbb        2024-04-14 01:50:19     2024-04-14 00:44:00     1752799 746972  3993715 662896640    27830000 100111100000110000000000000000  63850271f757564abc6ea17f6512e598bb28e579998df3b14c1d7402adfdaa4a        3940681891      386089497       86388558925171  0000000000000000000000000000000000000000742a63cf259cbabf3c52e1a2      03c5cd0c194d696e656420627920416e74506f6f6c208d00510345d132acfabe6d6d156f0efe94ec201df4a4853ae9ea670747a910168573b39530dda6f2b32bb7b510000000000000007552000070710b0000000000  3744    3619    6516    10146   92161540767     58909656        92786540767     59309156     56693621 36238.5625      32353.389       20.68   14202.083       9.0779  18563.45125422  625000000       399500  681693621       435738.5625     AntPool
839110  000000000000000000010ee343c504d9e536149f0d802c56563e69907c13395e        2024-04-14 01:52:26     2024-04-14 01:09:25     1566183 808973  3993102 700923904    29c74000 101001110001110100000000000000  d681f3604ae90056fe11d50887762a010d6c5114da28c993199405814b531b3f        1076868883      386089497       86388558925171  0000000000000000000000000000000000000000742ab2615b8cfe2282b5c26d      03c6cd0c04db361b662f4d41524120506f6f6c202876303331393234292f9ca21f12346d70c79652ad3916bb8fd413110e71b7006b000000ffffffff      3391    3247    6585    9244    235271917721    150385808       235896917721    150785312       51218036        32738.5684      32708.955    20.9076  12830.278       8.2009  32854.335711957 625000000       399500  676218036       432238.5625     MaraPool
839111  0000000000000000000149c0e19518eacc6eac6be49d2b7b344ee29e7d90501d        2024-04-14 02:07:45     2024-04-14 01:27:56     1693815 766388  3992979 765984768    2da80000 101101101010000000000000000000  dd7adcc7be2e2112f3ac0a5d3d903597ee7bde08df86ce15d76cf42c4e8457af        1873126986      386089497       86388558925171  0000000000000000000000000000000000000000742b00f3917d4185c918a338      03c7cd0c04733a1b662f466f756e6472792055534120506f6f6c202364726f70676f6c642f2cfcb20e7547010000000000   3189     3078    6957    10451   356938731684    228155232       357563731684    228554736       65357596        41776.5742      38593.777       24.6693 16373.263    10.4656  20694.940350883 625000000       399500  690357596       441276.5625     Foundry USA Pool
```

## Step 4: Importing tsv files to SQLite
**Code Link**: [Importing Code](https://github.com/vtataroglu/PhDWork/blob/main/import-data-to-sqlite.py)

The script begins by importing necessary libraries: `sqlite3` for database interactions, `csv` for reading tab-separated values files, and `os` for operating system interactions like file management.

1. **Database Connection**:
   - A connection to an SQLite database named `bitcoin_blocks.db` is established.
   - A cursor, which is used to execute SQL commands, is created from this connection.

2. **Table Creation**:
   - An SQL command is issued to create a table named `blocks` if it does not exist. The structure includes various fields that store data for each block in the Bitcoin blockchain.

3. **Reading .tsv Files**:
   - The script lists all files with a `.tsv` extension located in a specified directory.
   - Each file is opened, read as a dictionary where each row represents a block's data, and inserted into the `blocks` table.

4. **Data Insertion**:
   - For each file, the data is processed and inserted into the database, and a message is printed after each file is successfully processed.

5. **Final Output**:
   - The script prints the total number of successfully imported files and closes the database connection.

### Columns in the `blocks` Table

Each column in the table corresponds to a specific piece of data about a Bitcoin block:

- `id`: The block's unique identifier.
- `hash`: The block's hash value, a unique identifier generated from the block's data.
- `time`: Timestamp for when the block was mined.
- `median_time`: The median timestamp of the last 11 blocks.
- `size`: Size of the block in bytes.
- `stripped_size`: Size of the block in bytes, excluding any SegWit data.
- `weight`: A measurement that considers non-witness and witness data to determine block fullness in relation to the maximum block size.
- `version`: Version of the block format.
- `version_hex`: Hexadecimal representation of the block version.
- `version_bits`: Bitwise version based on the blocks mined previously.
- `merkle_root`: A hash of all the transactions in the block.
- `nonce`: A counter used for Bitcoin mining.
- `bits`: Compact form of the hash target.
- `difficulty`: Current difficulty target as a double precision number.
- `chainwork`: Total number of hashes expected to produce the chain up to the block.
- `coinbase_data_hex`: Data from the coinbase transaction, which is the first transaction in a block.
- `transaction_count`: Number of transactions in the block.
- `witness_count`: Number of witness transactions.
- `input_count`: Total number of inputs in all transactions in the block.
- `output_count`: Total number of outputs in all transactions in the block.
- `input_total`: Sum of all input values.
- `input_total_usd`: Sum of all input values in USD.
- `output_total`: Sum of all output values.
- `output_total_usd`: Sum of all output values in USD.
- `fee_total`: Total fees included in the block.
- `fee_total_usd`: Total fees in USD.
- `fee_per_kb`: Fees per kilobyte of block data.
- `fee_per_kb_usd`: Fees per kilobyte in USD.
- `fee_per_kwu`: Fees per kiloweight unit.
- `fee_per_kwu_usd`: Fees per kiloweight unit in USD.
- `cdd_total`: Coin Days Destroyed total, indicating economic activity.
- `generation`: Number of bitcoins generated in the block.
- `generation_usd`: Value of generated bitcoins in USD.
- `reward`: Total mining reward including transaction fees and block reward.
- `reward_usd`: Total mining reward in USD.
- `guessed_miner`: The miner guessed to have solved the block.

This detailed breakdown should help you understand how each component of the script works and what each column in the database represents with respect to Bitcoin block data.

## Step 5: Creating API to query on Bitcoin Block in SQLite
**Code Link**: [Creating API - Service Code](https://github.com/vtataroglu/PhDWork/blob/main/web-service-api-call.py)

First, ensure that Flask is installed using `pip install flask`, which provides the necessary framework to create and manage web services in Python. After installation, this script initializes a Flask web application to serve as an API endpoint `/api/get_data_by_interval_time`. It handles GET requests where users must provide `start_datetime` and `end_datetime` parameters. The API queries an SQLite database for records in the 'blocks' table that fall within the specified date range, converts these records into JSON format, and then compresses the response using gzip. This approach reduces data size for transmission, optimizing performance especially for large datasets and ensuring efficient data delivery over the network.

Test Url: 
```URI 
http://127.0.0.1:5000/api/get_data_by_interval_time?start_datetime=2024-04-01%2000:00:00&end_datetime=2024-04-01%2000:10:00
```

Example Response:
```JSON 
[
  {
    "id": 837165,
    "hash": "000000000000000000001356c25fd01601bad27e6240af53e050880b37772f47",
    "time": "2024-04-01 00:03:10",
    "median_time": "2024-03-31 22:56:23",
    "size": 2438208,
    "stripped_size": 518509,
    "weight": 3993735,
    "version": 536895488,
    "version_hex": "20006000",
    "version_bits": "100000000000000110000000000000",
    "merkle_root": "25cd6ab3729d9cec318b9040af103aee6e9d2b1f54a190bab2c4c556c202dc2c",
    "nonce": 2343124603,
    "bits": "386097875",
    "difficulty": 83126997340025,
    "chainwork": "000000000000000000000000000000000000000071e7017c206c4f9bbfe35960",
    "coinbase_data_hex": "032dc60c1b4d696e656420627920416e74506f6f6c38333035010002f8b3bc3efabe6d6d22803bf9ff9f49e0a58d6dd944639f552aabfe1839456fc3977578bd818faddb100000000000000000006c940434010000000000",
    "transaction_count": 2311,
    "witness_count": 2171,
    "input_count": 4975,
    "output_count": 7137,
    "input_total": 208676873880,
    "input_total_usd": 148792864,
    "output_total": 209301873880,
    "output_total_usd": 149238512,
    "fee_total": 22697185,
    "fee_total_usd": 16183.7734,
    "fee_per_kb": 9310.783,
    "fee_per_kb_usd": 6.639,
    "fee_per_kwu": 5685.7603,
    "fee_per_kwu_usd": 4.0543,
    "cdd_total": 32731.546009426,
    "generation": 625000000,
    "generation_usd": 445643.75,
    "reward": 647697185,
    "reward_usd": 461827.5312,
    "guessed_miner": "AntPool"
  }
]
```

## Step 6: Importing 1-Minute Historical Bitcoin Price Data to SQLite

This guide will walk you through the process of downloading and importing historical Bitcoin price data into a SQLite database.

> Download the Data
Download the dataset from Kaggle at [this link](https://www.kaggle.com/datasets/prasoonkottarathil/btcinusd).

> Extract the ZIP File
After downloading, extract the ZIP file. You should find multiple CSV files representing different years:
- `BTC-2017min.csv`
- `BTC-2018min.csv`
- `BTC-2019min.csv`
- `BTC-2020min.csv`
- `BTC-2021min.csv`

> Import Data Using Python

Change the `csv_file_path` in the Python script below to match the CSV file you want to import. You can repeat the import steps for each year by changing the CSV file path accordingly.

**Code Link**: [The Python script](https://github.com/vtataroglu/PhDWork/blob/main/import-btc-price-data.py) primarily focuses on importing and organizing 1-minute interval historical Bitcoin price data into a SQLite database. It begins by setting up a connection to a SQLite database named bitcoin_price.db. If this database does not exist, it will be automatically created. The script then executes a SQL command to create a table called bitcoin_prices, ensuring it only creates the table if it doesn't already exist, to avoid overwriting any existing data. This table is structured with specific columns like unix, date, symbol, open, high, low, close, volume_btc, and volume_usd to store various trading metrics. The data is loaded from a CSV file, which is specified by the user, into a pandas DataFrame. This DataFrame undergoes column name standardization by replacing spaces with underscores and converting them to lowercase, ensuring the column names are compatible with SQL conventions. Additionally, the date column is explicitly converted to a string format to match the SQLite TEXT data type requirements. After formatting, the data is imported into the SQLite database using pandas' to_sql function, which appends the data to the existing table without replacing any previous entries. Finally, the script commits these changes to the database and closes the connection, securing all the imported data within the database, and confirms the successful data importation with a print statement. This approach facilitates efficient data handling and storage, making it accessible for further analysis or reporting.

## Step 7: Testing Bitcoin Price Data Output

**Code Link**: [This Python Script](https://github.com/vtataroglu/PhDWork/blob/main/test-bitcoin-price-data.py)  is designed to query Open, High, Low, and Close (OHLC) data of Bitcoin prices from a SQLite database and return it in JSON format. The main functionality is encapsulated within a function named `query_ohlc_data`, which takes two parameters: `start_date` and `end_date`. 

These parameters define the time range for which the OHLC data is requested.

- **SQL Query Execution**: A SQL query is constructed and executed to select the columns `date`, `open`, `high`, `low`, and `close` from the `bitcoin_prices` table where the `date` falls between the `start_date` and `end_date`. The results are ordered by `date` in ascending order to maintain chronological order.

- **Data Fetching and Formatting**: After executing the query, all the resulting rows are fetched and each row is converted into a dictionary. This conversion facilitates the next step and makes the data structure more intuitive and easy to handle.

- **JSON Conversion**: Before concluding the function, the list of dictionaries (each representing a row of data) is converted into a JSON string. This conversion uses the `json.dumps` method, with the `default=str` argument to ensure proper handling of any `datetime` objects, which may not be serializable by default.


### Example Usage:

The function is demonstrated with an example, querying data from the last minute of 2019 to the first five minutes of 2020. The output is printed as a JSON string, which can be easily integrated with web applications or used for further data analysis.

start_date = '2019-12-31 23:55:00'
end_date = '2020-01-01 00:05:00'

### Example Output 
```JSON
[
  {
    "date": "2019-12-31 23:55:00",
    "open": 7175.69,
    "high": 7176.68,
    "low": 7175.69,
    "close": 7176.68
  },
  {
    "date": "2019-12-31 23:56:00",
    "open": 7182.49,
    "high": 7182.49,
    "low": 7170.2,
    "close": 7170.2
  },
  {
    "date": "2019-12-31 23:57:00",
    "open": 7164.22,
    "high": 7170.8,
    "low": 7161.65,
    "close": 7166.89
  },
  {
    "date": "2019-12-31 23:58:00",
    "open": 7166.89,
    "high": 7167.3,
    "low": 7161.99,
    "close": 7167.3
  },
  {
    "date": "2019-12-31 23:59:00",
    "open": 7167.3,
    "high": 7171.22,
    "low": 7167.3,
    "close": 7168.36
  },
  {
    "date": "2020-01-01 00:01:00",
    "open": 7161.51,
    "high": 7161.51,
    "low": 7155.09,
    "close": 7161.2
  },
  {
    "date": "2020-01-01 00:02:00",
    "open": 7158.82,
    "high": 7158.82,
    "low": 7158.82,
    "close": 7158.82
  },
  {
    "date": "2020-01-01 00:03:00",
    "open": 7158.82,
    "high": 7158.82,
    "low": 7156.9,
    "close": 7156.9
  },
  {
    "date": "2020-01-01 00:04:00",
    "open": 7158.5,
    "high": 7158.5,
    "low": 7154.97,
    "close": 7157.2
  },
  {
    "date": "2020-01-01 00:05:00",
    "open": 7156.52,
    "high": 7159.51,
    "low": 7150.1,
    "close": 7158.5
  }
]

```

<p align="center">
  <img src="https://i.giphy.com/Anyd8oskpTJuq9OVMP.webp" /> 
</p>


> 
> [!CAUTION]
> IMPORTANT
> This dataset may have missing 1-minute bars of datetime data. If you are conducting anomaly detection or any other form of time series analysis, it is crucial to be aware of this potential issue. To verify the extent of missing datetime data, you can utilize the following Python script. This script, available at **Code Link**: [BitcoinPriceDataIntegrityCheck](https://github.com/vtataroglu/PhDWork/blob/main/BitcoinPriceDataIntegrityCheck.py), identifies and quantifies missing minutes in the Bitcoin price data. It does this by comparing a DataFrame, which lists every minute within the observed date range from the database, against the actual data retrieved. It then calculates and displays the total count of these missing minutes and records these discrepancies in a text file named "missing_dates.txt", providing a comprehensive log of all timestamps for which price data is missing.



> [!TIP]
> If you need to complete missing data points, you can utilize Binance's public price data. I have developed a straightforward script that addresses this need. The script is accessible via **Code Link**: [The Python Code](https://github.com/vtataroglu/PhDWork/blob/main/retrieve-price-data-from-binance.py) retrieves minute-level cryptocurrency price data from the Binance API, targeting specific missing timestamps indicated in a file named `missing_dates.txt` (if you use BitcoinPriceDataIntegrityCheck.py then you got this file). The script reads these timestamps, organizes them by date, and for each date, it determines the time range of missing data. The script then queries the Binance API to fill these gaps, processes the responses into a structured format, and stores the results in a JSON file. This method ensures that the dataset is complete and accurate, which is crucial for analyses such as high-frequency trading strategies where minute-level precision is essential.


## Step 8: Creating API to query on Historical Bitcoin Price in SQLite

**Code Link**: [This Python Script](https://github.com/vtataroglu/PhDWork/blob/main/web-service-bitcoin-price-api-call.py)  uses Flask to create a REST API that serves historical Bitcoin price data. The data is stored in a SQLite database and can be accessed via a specific endpoint. Below is a detailed explanation of the script's components and functionalities.

- `query_ohlc_data(start_date, end_date)`: This function takes two parameters, `start_date` and `end_date`, both expected to be strings in the format 'YYYY-MM-DD HH:MM:SS'. It queries the SQLite database for OHLC data between these two dates.
  
- `@app.route('/api/get-price-data', methods=['GET'])`: Defines a route `/api/get-price-data` that handles GET requests. This route allows users to request OHLC data by providing `start` and `end` parameters in the URL query string.

- **Parameter Handling**: The function `get_ohlc_data()` retrieves the `start` and `end` parameters from the request. If either parameter is missing, it returns an error message and a 400 status code indicating a bad request.

- **Data Retrieval and Response**: If the parameters are valid, `query_ohlc_data` is called, and its results are handled. If there's an error in the date format, an appropriate error message is returned. Otherwise, the JSON data is sent back to the client in a response object with the `application/json` MIME type.


- To use the API, a user would send a GET request to `http://localhost:5000/api/get-price-data?start=YYYY-MM-DD HH:MM:SS&end=YYYY-MM-DD HH:MM:SS`. The response would be the requested Bitcoin OHLC data in JSON format or an error message if the input parameters are incorrect.

>> Example Url: http://127.0.0.1:5000/api/get-price-data?start=2020-04-01%2000:00:00&end=2020-04-01%2000:20:00

This example demonstrates how to use the Flask API to fetch Open-High-Low-Close (OHLC) data for Bitcoin from a SQLite database over a specified time period.

In this URL:
- The `start` parameter is set to `2020-04-01 00:00:00`.
- The `end` parameter is set to `2020-04-01 00:20:00`.
- These parameters define the time range for which you want to retrieve the Bitcoin price data.

### Response Data

Upon successful retrieval of the data, the API returns JSON formatted data representing the OHLC values for each minute within the specified time range. Here is an example of the JSON response data:

```json
[
  {"date":"2020-04-01 00:00:00","open":6428.74,"high":6440.25,"low":6427.83,"close":6427.83},
  {"date":"2020-04-01 00:01:00","open":6427.56,"high":6430.81,"low":6427.56,"close":6430.81},
  {"date":"2020-04-01 00:02:00","open":6429.39,"high":6429.39,"low":6429.39,"close":6429.39},
  {"date":"2020-04-01 00:03:00","open":6429.23,"high":6429.23,"low":6429.23,"close":6429.23},
  {"date":"2020-04-01 00:04:00","open":6430.1,"high":6433.42,"low":6430.1,"close":6430.86},
  ...
  {"date":"2020-04-01 00:20:00","open":6310.71,"high":6326.85,"low":6292.6,"close":6326.85}
]
```

## Step 9: Aggregate Bitcoin price data from 1-minute into 10-minute intervals

**Code Link**: [This Python Script](https://github.com/vtataroglu/PhDWork/blob/main/aggregation-from-1-to-10-min.py)   that aggregates all data in the bitcoin_prices table into 10-minute intervals, ordered from the oldest to the most recent entries, without requiring specific start and end dates. 


Step-by-step SQL Query Adjustment
1) Change your query to group the data into 10-minute intervals. You'll need to use SQLite's datetime functions to round the times to 10-minute blocks.
2) Aggregate the prices within these intervals by taking the opening price at the start of the interval, the highest price, the lowest price, and the closing price at the end of the interval.


```sql
SELECT 
    datetime((strftime('%s', date) / 600) * 600, 'unixepoch') AS time_interval,
    MIN(date) AS open_time,
    FIRST_VALUE(open) OVER (PARTITION BY datetime((strftime('%s', date) / 600) * 600, 'unixepoch') ORDER BY date ASC) AS open,
    MAX(high) AS high,
    MIN(low) AS low,
    LAST_VALUE(close) OVER (PARTITION BY datetime((strftime('%s', date) / 600) * 600, 'unixepoch') ORDER BY date DESC) AS close
FROM bitcoin_prices
WHERE date BETWEEN ? AND ?
GROUP BY time_interval
ORDER BY time_interval ASC;
```

**Open Time**: `MIN(date)` finds the earliest timestamp within each 10-minute interval, representing the time when the interval starts.

**Open Price**: `FIRST_VALUE(open)` selects the first 'open' price in each interval. It uses a window function to look at all entries in the partition of the specified 10-minute interval, ordering by date in ascending order to get the first value.

**High Price**: `MAX(high)` computes the maximum 'high' price within the interval, representing the highest price that was reached during the interval.

**Low Price**: `MIN(low)` computes the minimum 'low' price within the interval, representing the lowest price that was reached during the interval.

**Close Price**: `LAST_VALUE(close)` selects the last 'close' price in each interval, using a window function to look at all entries in the partition, ordering by date in descending order to fetch the last value before the end of the interval.


and test code for interval 10 minute

```python
import sqlite3

def fetch_first_50_entries(database_path):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        query = """
        SELECT time_interval, open_time, open, high, low, close
        FROM min10price
        ORDER BY time_interval ASC
        LIMIT 50;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        # Display the data
        for row in rows:
            print(f"Time Interval: {row[0]}, Open Time: {row[1]}, Open: {row[2]}, High: {row[3]}, Low: {row[4]}, Close: {row[5]}")

# Example usage of the function
database_path = 'bitcoin_price.db'
fetch_first_50_entries(database_path)
```

## Example Response 
```text
Time Interval: 2017-01-01 00:00:00, Open Time: 2017-01-01 00:01:00, Open: 966.16, High: 966.58, Low: 966.16, Close: 966.37
Time Interval: 2017-01-01 00:10:00, Open Time: 2017-01-01 00:10:00, Open: 966.08, High: 966.57, Low: 964.6, Close: 965.58
Time Interval: 2017-01-01 00:20:00, Open Time: 2017-01-01 00:20:00, Open: 964.87, High: 966.54, Low: 964.87, Close: 964.87
Time Interval: 2017-01-01 00:30:00, Open Time: 2017-01-01 00:30:00, Open: 965.24, High: 966.4, Low: 965.24, Close: 965.24
Time Interval: 2017-01-01 00:40:00, Open Time: 2017-01-01 00:40:00, Open: 966.38, High: 966.98, Low: 965.94, Close: 965.94
Time Interval: 2017-01-01 00:50:00, Open Time: 2017-01-01 00:50:00, Open: 966.97, High: 966.99, Low: 966.59, Close: 966.99
Time Interval: 2017-01-01 01:00:00, Open Time: 2017-01-01 01:00:00, Open: 966.59, High: 966.6, Low: 965.08, Close: 965.08
...
Time Interval: 2017-01-01 08:00:00, Open Time: 2017-01-01 08:00:00, Open: 964.96, High: 964.96, Low: 964.96, Close: 964.96
Time Interval: 2017-01-01 08:10:00, Open Time: 2017-01-01 08:10:00, Open: 964.96, High: 964.98, Low: 964.96, Close: 964.96
```

## Step 10: Creating new API Bitcoin price from 10-minute intervals data

Adding new API Endpoing to this you can check **Code Link**: [This Python Script](https://github.com/vtataroglu/PhDWork/blob/main/web-service-api-call.py) 

### API Endpoint: `/get_price_ten-interval`
This endpoint provides access to the Bitcoin price data at 10-minute intervals:

- **Route Definition**: The route listens at `/get_price_ten-interval` and only responds to GET requests.
- **Parameter Retrieval**:
  - Retrieves `start` and `end` parameters from the query string of the request. These should represent the start and end times for the query.
- **Date Validation**:
  - Validates that `start` and `end` are in the correct datetime format (`YYYY-MM-DD HH:MM:SS`). If not, it returns a JSON error message.
- **Data Fetching**:
  - Calls the `fetch_entries` function with the database path and the validated times.
- **Response**:
  - Returns the fetched data as JSON. If the date format is incorrect, it sends a 400 status code with an error message.

Test this new API endpoint to retrieve Bitcoin prices recorded at 10-minute intervals:

> Test Url : http://127.0.0.1:5000/get_price_ten-interval?start=2020-04-01%2000:00:00&end=2020-04-01%2000:20:00

You can request this URL to view newly aggregated data for each 10-minute interval. If everything appears correct, you are ready to proceed to the next step.

## Example Response 
```text
[
  {
    "close": 6423.07,
    "high": 6440.25,
    "low": 6422.88,
    "open": 6422.88,
    "open_time": "2020-04-01 00:00:00",
    "time_interval": "2020-04-01 00:00:00"
  },
  {
    "close": 6308.73,
    "high": 6428.42,
    "low": 6272.17,
    "open": 6340.05,
    "open_time": "2020-04-01 00:10:00",
    "time_interval": "2020-04-01 00:10:00"
  },
  {
    "close": 6269.01,
    "high": 6327.43,
    "low": 6262,
    "open": 6284.87,
    "open_time": "2020-04-01 00:20:00",
    "time_interval": "2020-04-01 00:20:00"
  }
]
```
## Step 11: Summary of the Previous 10 Steps

> We will explore data spanning from January 1, 2017, at 00:00:00 to March 1, 2022, at 03:50:00.

| Title                               | Value        |
|-------------------------------------|--------------|
| Count of Blocks                     | 279,340      |
| Count of Transactions               | 530,367,603  |
| Count of Price Bars (1 Minute)      | 2,716,184    |
| Count of Price Bars (10 Minutes)    | 271,455      |

> [!TIP]
> I have completed missing price data where it could be found. Please refer to the TIP information in Step 7.
