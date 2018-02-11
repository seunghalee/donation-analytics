# Table of Contents
1. [Challenge Prompt](README.md#challenge-prompt)
2. [Input Data Source](README.md#input-data-source)
3. [Solution Requirements](README.md#solution-requirements)
4. [Approach](README.md#approach)
5. [Repo directory structure](README.md#repo-directory-structure)

# Challenge Prompt
For each recipient, zip code, and calendar year, calculate the following three values for contributions coming from repeat donors:
* total dollars received
* total number of contributions received
* donation amount given in percentile

Given two input files:
1. `percentile.txt`, holds a single value -- the percentile value (1-100) that your program will be asked to calculate.
2. `itcont.txt`, has a line for each campaign contribution that was made on a particular date from a donor to a political campaign, committee or other similar entity. 

# Input Data Source 
The Federal Election Commission provides data files stretching back years and is [regularly updated](http://classic.fec.gov/finance/disclosure/ftpdet.shtml). Data files conform to the data dictionary [as described by the FEC](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

Fields of Interest:
* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `NAME`: name of the donor
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

# Solution Requriments
Solution was written in Python 3.6.3 and requires datetime, os, sys, and math modules.

# Approach
The solution was written under the assumption that the data is streaming in. As each line of `itcont.txt` is read, the pipe-delimited fields are checked to make sure we want to use that particular record -- records with empty or malformed fields with respect to `CMTE_ID`, `NAME`, `ZIP_CODE`, `TRANSACTION_DT`, `TRANSACTION_AMT`, `OTHER_ID` are completely ignored. If the record is one that we are interested in, the program formats fields of interest appropriately (if necessary). For example, the transaction date, which is in a string format in the input file, is formatted so it is a datetime.datetime object, and any zip codes that are longer than 5-digits are truncated. Each record is assigned a unique donor ID consisting of the donor's name and 5-digit zip code (per challenge instructions, donation records with idential names and zip codes are considered to be from the same donor). A set is created consisting of all previous donor IDs to check if a particular donor is a repeat donor. A dictionary is also created to keep track of calendar years associated with each donor ID. If a donor is a repeat donor, and the particular donation was made later than existing donation records (need to check this because the data be streamed in out of order), the program computes the following fields:

* recipient of the contribution (or `CMTE_ID` from the input file)
* 5-digit zip code of the contributor (or the first five characters of the `ZIP_CODE` field from the input file)
* 4-digit year of the contribution
* running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year. Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar). For the percentile computation the **nearest-rank method** [as described by Wikipedia](https://en.wikipedia.org/wiki/Percentile) was used.
* total amount of contributions received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
* total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors

The above six fields are then written out onto a pipe-delimited line and then saved to an output file called `repeat_donors.txt`


# Repo Directory Structure

The directory structure for this repo looks like this:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── donation-analytics.py
    ├── input
    │   └── percentile.txt
    │   └── itcont.txt
    ├── output
    |   └── repeat_donors.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── percentile.txt
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── repeat_donors.txt
            ├── test_2
                ├── input
                │   └── percentile.txt
                |   └── your-own-input-for-itcont.txt
                |   
                |── output
                    └── repeat_donors.txt




