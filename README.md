# webscraping2
# Assignment 6 - Part B: Multiprocess Web Scraping
## Introduction
This assignment involves creating a multiprocess web scraper to extract data from Wikipedia's Summer Olympics pages. By leveraging multiple processes, the goal is to enhance the speed of web scraping tasks and store the fetched data into a SQLite database efficiently.

## Environment Setup
### Dependencies
1. Requests or urllib3 for making HTTP requests.
2. json for processing JSON data.
3. Beautiful Soup 4 (bs4) for parsing HTML and XML documents.
4. sqlite3 for database operations.
5. random for random sampling.
### Install the required libraries using the following command:
pip3 install requests beautifulsoup4 sqlite3
##Database Setup
Create a SQLite database named OlympicsData.db. Within this database, create a table named SummerOlympics with columns for storing various details about the Summer Olympics from the past 50 years (1968-2020).

## Files
1. 23CS60R45_ASSGN6_3.py: Initializes the database and fetches the main Summer Olympics Wikipedia page to extract URLs for individual Olympics events.
2. scraper.py: Performs the web scraping for each Olympics URL marked as not done in the database and updates the database with the fetched information.
3. checker.py: Checks whether all rows in the database are populated and generates a report with specific queries.
4. performance_report.txt: Documents the observed speed up in scraping tasks by using multiple processes.
## How to Run
Initialize Database and Fetch URLs
Run the handler.py script to initialize the database and fetch initial data:
python3 23CS60R45_ASSGN6_3.py
## Start Scraping Process
Execute the scraper.py script in separate processes:
python3 scraper.py&
python3 scraper.py&
python3 scraper.py&

## Check Database and Generate Report
After the scraping processes complete, run checker.py to check the database's completeness and generate a report:
python3 checker.py
## Performance Analysis
Refer to the performance_report.txt for an analysis of the performance gains achieved through multiprocess scraping.
## Assignment Objective
The primary objective of this assignment is to understand the benefits and implementation challenges of using multiple processes for web scraping tasks. Students are expected to analyze the speed-up gained from parallelizing web scraping operations and document their findings.




