# Bitquery getTransactions
Written in python, fetches transaction data from [bitquery.io api](https://graphql.bitquery.io) with user-defined target
address and network selection (ETH or Layer 2).


The returned JSON is written out to a csv file.

## Executable script
We may use [PyInstaller](https://pyinstaller.org/en/stable/) to create an executable file which runs this script.
This nifty package will create the appropriate executable for the host os (windows/mac/linux).

## Instructions - Executable
Follow these steps to create an executable with packaged dependencies.
1. Clone repository
2. Edit config_dummy.json to add API credentials, predefined address and filter currencies
3. Rename config_dummy.json >> config.json
4. pip install pyinstaller
5. pyinstaller --onefile getTransactions.py
6. run getTransactions.exe
7. Select or input ETH address
8. Select or input ETH/Tokens
9. CSV file will be output to the script directory with the last four characters of the target address, and the script
execution time.

## Instructions - Python script
Follow these steps to run the python script natively.
1. Clone repository
2. Edit config_dummy.json to add API credentials, predefined address and filter currencies
3. Rename config_dummy.json >> config.json
4. run getTransactions.py
5. Select or input ETH address
6. Select or input ETH/Tokens
7. CSV file will be output to the script directory with the last four characters of the target address, and the script
execution time.