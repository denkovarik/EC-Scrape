:: This batch file installs the dependencies for the project
ECHO OFF
:: Update PIP
call py -m pip install --upgrade pip
:: Install Pandas
call py -m pip install pandas
:: Install Biopython
call py -m pip install biopython
:: Install xlrd
call py -m pip install xlrd
:: Install openpyxl
call py -m pip install openpyxl
:: Install PySimpleGUI
call py -m pip install PySimpleGUI
:: Install Progress Bar
call py -m pip install progress progressbar2 alive-progress tqdm
:: Install PySimpleGUI
call py -m pip install pysimplegui
:: Install Requests
call py -m pip install requests