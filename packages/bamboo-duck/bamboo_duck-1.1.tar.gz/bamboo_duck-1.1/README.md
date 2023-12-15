## Overview

DESDR - Process is a Python tool created to replace DBT in the DESDR workflow. With DESDR, we can build and maintain the SQL models that power the data visualization dashboard more effectively

DESDR Features:
- VARS, FUNCTION, and MACROS: replace DBT in the original DESDR workflow and allow users to break down complex SQL models into more maintainable chunks.
- DESDR Execute: allows users to run in-line SQL commands and receive results. Good for testing the accuracy of SQL command/ model 
- DESDR Process: process all SQL files in /models folders and output SQL commands that power the dashboard to models_out.json

## Getting Started:
1) Install Python (if you haven't already). Please follow the guide here: https://realpython.com/installing-python/
2) Clone the GitHub repo:
   
   ```sh
   git clone https://github.com/Columbia-DESDR/bamboo-duck.git
   ```
   
## Understanding DESDR Functionality 

The repo contains some samples of SQL code to demonstrate how DESDR - Process works. Follow the steps below to explore each function of DESDR:

1) VAR:

We can define some global variables for the SQL file/ models. These values are defined in a .yml file. To update the values of these variables, please update the .yml file.

For the sample SQL code, the variables are defined in dbt_project.yml

2) REFS:

We want the ability to refer to a different SQL model inside our current model. For example, suppose we want to execute this SQL statement:

      WITH foo AS (
        WITH bar AS ( SELECT * from baaz )
        SELECT * FROM bar
      )
      SELECT * FROM foo

Instead of having to write all the WITH AS statements (regular SQL standard), you can simply write:
   
   ```sh
   SELECT * from ref("foo")
   ```

and define foo.sql in a separate file as:

   ```sh
   SELECT * FROM bar
   ```

and defined bar.sql in a separate file as:

   ```sh
   SELECT * from baaz
   ```
3) MACROS:

 We want to perform some calculations on different SQL models as well. 

 For example: 

 We defined the macro join_example as: 
```sh
{% macro join_example(w1,w2) %}
  WITH output as (SELECT a.gid, b.gid from {{w1}} a JOIN {{w2}} b ON a.gid=b.gid)
{% endmacro %}
   ```
and we have chirps and evi as separate sql models, defined in chrips.sql and evi.sql (see /models for full content of chirps.sql and evi.sql), then we can write:

```sh
{{join_example(ref("chirps"),ref("evi"))}}
 ```
instead of the full sql statements:

 ```sh
   "with chirps as ( with unpivot_result as ( select * from chirps_raw ), gid_map as ( select a.gid, a.year, a.value, a.dekad, b.village from unpivot_result a left join admin_raw b on a.gid = b.gid ), filter_year_admin as ( select * from gid_map where gid = 'var(region)' and YEAR >= var(year_start) and YEAR <= var(year_end) ), cap as ( select *, case when value > var(dekcap) then var(dekcap) else value end as value_cap from filter_year_admin a ), output as ( select * from cap ) select * from output ), evi as ( with unpivot_result as ( select * from evi_raw ), gid_map as ( select a.gid, a.year, a.value, a.dekad, b.village from unpivot_result a left join admin_raw b on a.gid = b.gid ), filter_year_admin as ( select * from gid_map where gid = 'var(region)' and YEAR >= var(year_start) and YEAR <= var(year_end) ), cap as ( select *, case when value > var(dekcap) then var(dekcap) else value end as value_cap from filter_year_admin a ), output as ( select * from cap ) select * from output ), src as (SELECT * from chirps a JOIN evi b ON a.year=b.year)"
   ```
## How to use DESDR - Process

DESDR - Process is a command line application. To understand how DESDR - Process works, open your terminal, navigate to the bamboo-duck folder, and run the following command:

```sh
python3 main.py 
 ```
or 

```sh
python3 main.py -h
 ```
This command will return the instructions on how to use DeSDr - Process

```sh
Displaying Usage: This program is created to execute DuckDB Query (-e or -Execute flag) or process data (Process Flag)
To execute a sql file, executing this command: python3 main.py -e [sql file] [yml file]
To execute an SQL inline command, execute this command: python3 main.py -e ["sql query"] [yml file]
To create models_out.json, develop SQL models and put them in /models folder, executing this command: python3 main.py -p
```

To understand how DESDR - Process users the VARS and REFS, navigate to /test folder and inspect test.sql, test1.sql, test2.sql and test3.sql. Notice how test has ref to test1, test1 has ref to test2 and, test2 has ref to test3. Run the following command:

```sh
python3 main.py -e test.sql dbt_project.yml
```
and see the result of the SQL command:

```sh
The result of SQL query is: 
(1128, 'Genete', 'LEGAMIBO', 18, 21, 25, 27, 'Nov', 'Previous R4 Village (Not Updated)')
```
We can also write an in-line SQL query and execute it:

```sh
python3 main.py -e "SELECT * FROM ref('test1') WHERE gid = var('region')" dbt_project.yml
```
It should also return the same result.

Now, navigate to the /models folder. Inside this folder, you will find some sample SQL modes. These models were used to deploy the Ethiopia instance of DESDR and you can refer to these models to develop SQL models for new instances of DESDR. Run the command below: 

```sh
python3 main.py -p 
```

to obtain a models_out.json file to power the data visualization of the dashboard. 

## Questions/ Contacts:

Any questions/ comments on this guide, please contact nn2571@columbia.edu


   










































