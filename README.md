# Logs Analysis
Udacity - Full Stack - Project 3

## 1 Description

This project analyzes log information from "news" database.

## 2 Set up the database

First, download the data from here:

<a>https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip</a>

Second, decompress this `.zip` file, you'll get a file named `newsdata.sql`, move this file to your `/vagrant` directory.

Third, bring back your virtual machine and log into it:

`$ vagrant up`

`$ vagrant ssh`

Finally, `cd` to your `/vagrant` directory in virtual machine, import the data:

`$ psql -d news -f newsdata.sql`

## 2 Compile and run the project

In your virtual machine, type the following command line:

`$ python log_reporter.py`

The report will be displayed in your terminal.

You can also view this report in `expected_output.txt`. 
