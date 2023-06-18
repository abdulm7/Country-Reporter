# How to run:
 - pip3 install -r Requirements.txt
 - python3 db_main.py OR use modules in your own program

How my Python Modules are Structured and any Changes
 - All my python modules are in the 'db_functions.py' file
    - I have a module to read each unqiue type of file (exception capital and area)
        - since capital and area have the same file structure (ISO3, Country, Data) I used the same function twice
    - There is one module that combines all economic information based on the information returned from the modules that read the files
    - There is one module that that combines all non-economic information based on the information returned from the modules that read the files
        - both these modules are used in a module to prepare all data in the database to be pushed
        - The reason I combinine all data in memory and pushing it at once is to better organize and handle the table, also based on what was said in class, we will not run into enough data to overflow the memory
    - to use all the above modules, you just need to call the 'create_tables_dict' entering all the file names in the following order: names file, area file, capitals file, currency and population file, languages file, and gdp file.
 - Files are expected to have all there information in the correct order
    - 'names' header order:
        - ISO3, Common Name, Official Name, ISO2
    - 'area' header order:
        - ISO3, Country Name, Area
    - 'capitals' header order:
        - ISO3, Country Name, Capital
    - 'currency and population' header order:
        - Country, Currency, Population Year, Year, Year
    - 'languages' header order:
        - ISO3, Country, Languages
        - Note, languages can have multiple values that are comma seperated
    - 'gdp' file header order:
        - Country, Year
 - No changes were made to the CSV files
 - missing information from the csv is okay as long as it is in the correct order
 - The following assignment related modules are included
    - creating a table
    - delete a table
    - load bulk records
    - adding an individual record
    - delete an individual record
    - display a specified table
    - query modules that build the require reports

# How to connect to the database
 - have a AWS user named 'default' which has admin and db read and write permissions
 - have your S5-S3.conf file (left name for convience of using same file as A1)
    - S5-S3.conf file should contain your 'default' user's access and secret keys
 - ensure config file is in the same directory as db_main.py

# How to use modules:
 - All modules can be used through the main program, 'db_main.py'
 - An interactive CLI that is simple and easy to use

# How to generate both types of reports:
 - To generate each report simply run the 'db_main.py' file
 - ensure the data has been loaded into the databases
    - if not you can load in db_main if csv files are in the same directory
 - select option '7' for country level
    - enter country name (NOTE: THIS IS CASE SENSITIVE e.g. wrong: canada, correct: Canada)
    - enter the file you would like to store the report in (NOTE: DO NOT INCLUDE EXTENSION e.g. wrong: report_a.txt, correct: report_a)
    - if the file exists you will have the option to overwrite or not
 - select option '8' for global level
    - enter year you desire to see (NOTE: YEAR MUST BE NUMERIC)
    - enter the file you would like to store the report in (NOTE: DO NOT INCLUDE EXTENSION e.g. wrong: report_b.txt, correct: report_b)

# Main Program:
 - the 'db_main.py' file is the program that can excute all of the modules
 - a simple CLI that allows the user to:
    - create the 'non-econ' (Non-economic) and 'econ' (Economic) tables in the database with a single command
    - delete both tables from the databases with a single command
    - Load all the records from CSV with a single command
    - Add individual record (Without any of the attributes)
    - Delete an individual record
    - Display the Economic or Non-Economic table directly from the database
    - Create "Report A" (country level report) and store it in a 'txt' file
    - Create "Report B" (Global level report) and store it in a 'txt' file
    - Adding missing information to a record in the database
    - Exit the program
 - All menu options can be selected with their associate numeric value to reduce the complications of string commands. 'quit' and 'exit' can be used to end the program as well.
 - When writing the report to a file, if the txt file already exists, the user will be prompted whether they would like to overwrite or not, in this scenario they can used the associated numeric values or enter 'y' for yes or 'n' for no

# How to make edits
 - Edits can easily be made through option '9' in the menu where you can add/update information in an existing record
 - if the record doesn't exist, you can add it by using option '4'
 - These menu options are very interative and will inform the user of the correct input required with useful error messages assuming they incorrectly inputted something

# Limitations:
 - Country input is case sensitive so user must match case of the country as well as the spelling of the common name to correctly retrieve the information
    - e.g. user enters 'Central african republic', this would result in 'country not found' error
           to fix this, user must enter 'Central African Republic' 
    - assuming user adds a record, whatever the spelling and case of that record, it would be required they match it to retrieve the information
        - e.g. user creates record 'united Kingdom'
                to add to this record, country input must also be 'united Kingdom'
 - The 2 table names are set to 'non-econ' and 'econ', they are global variables, you can change the name of these variables, but it must be done in both the modules and main program python files
 - Country level report requires the country requested to be in both tables
