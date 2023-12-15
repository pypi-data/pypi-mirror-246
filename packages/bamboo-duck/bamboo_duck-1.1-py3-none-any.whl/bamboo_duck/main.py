import getopt
import sys
import duckdb
import os
import yaml
import string
import re
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from .my_function import *
from .parsewith import *
import json

def cli():
    
    options = "he:p"

    long_options = ["Help", "Execute", "Process"]

    e_flag = False
    p_flag = False

    # Get args from users
    argumentList = sys.argv[1:]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        if len(argumentList) == 0:
            print("Displaying Usage: This program is created to execute DuckDB Query (-e or -Execute flag) or process data (-p or -Process Flag)")
            print(
                "To execute a sql file, executing this command: python3 main.py -e [sql file name] [yml file name]")
            print(
                "To execute an SQL inline command, execute this command: python3 main.py -e [\"sql query\"] [yml file name]")
            print("To create models_out.json, develop SQL models and put them in /models folder, executing this command: python3 main.py -p ")

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print("Displaying Usage: This program is created to execute DuckDB Query (-e or -Execute flag) or process data (Process Flag)")
                print(
                    "To execute a sql file, executing this command: python3 main.py -e [sql file] [yml file]")
                print(
                    "To execute an SQL inline command, execute this command: python3 main.py -e [\"sql query\"] [yml file]")
                print("To create models_out.json, develop SQL models and put them in /models folder, executing this command: python3 main.py -p ")

            elif currentArgument in ("-e", "--Execute"):
                print("Executing the SQL query in the specified path or inline: " +
                    sys.argv[2] + " using the yml file: " + sys.argv[3])

                yaml_file_name = sys.argv[3]
                with open(yaml_file_name, 'r') as yaml_file:
                    variables = yaml.safe_load(yaml_file)
                # If input is SQL file
                if is_sql_file(sys.argv[2]):
                    sql_file_name = sys.argv[2]
                    directory_to_search = os.getcwd()
                    sql_file_path = find_file_in_directory(
                        sql_file_name, directory_to_search)
                    with open(sql_file_path, 'r') as sql_file:
                        sql_script = sql_file.read()

                # If input is
                else:
                    sql_script = sys.argv[2]
                    temp_sql_file = create_temp_sql_file('CTE.sql', sql_script)
                    sql_file_name = temp_sql_file
                    # print("what is SQL file name")
                    # print(sql_file_name)
                # Set e_flag - True:
                e_flag = True

            elif currentArgument in ("-p", "--Process"):
                yaml_file_name = sys.argv[2]
                print("Process the data")
                p_flag = True

    except getopt.error as err:
        print(str(err))

    # Run execute option
    if e_flag == True:
        con = duckdb.connect(database=':memory:')
        create_tables_from_csv(con)
        cursor = con.cursor()
        macro_dict = create_macro_dictionary_from_macro_models()
        # print("inside main")
        # print(sql_file_name)
        query = process_sql_content(
            sql_file_name, sql_script, macro_dict, variables)

        # print(query)
        query = variable_replacement(variables, query)
        cursor.execute(query)

        # Fetch all rows from the result
        result = cursor.fetchall()

        # Print the result
        print("The result of SQL query is: ")
        for row in result:
            print(row)


    if p_flag == True:

        sql_model_dict = {}
        output_file_path = "models_out.json"
        macro_dict = create_macro_dictionary_from_macro_models()

        with open(yaml_file_name, 'r') as yaml_file:
            variables = yaml.safe_load(yaml_file)

        con = duckdb.connect(database=':memory:')
        create_tables_from_csv(con)
        cursor = con.cursor()

        current_directory = os.getcwd()
        models_directory = os.path.join(current_directory, 'models')

        for root, _, files in os.walk(models_directory):
            for file in fnmatch.filter(files, '*.sql'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as sql_file:
                    query = sql_file.read()
                query = process_sql_content(file, query, macro_dict, variables)
                # print(query)
                query = query.replace('\n', ' ')
                query = re.sub(r'\s+', ' ', query)
                sql_model_dict[file] = query
                # Write the dictionary to the JSON file

        write_pretty_json(sql_model_dict, output_file_path)
        print("Finish SQL files processing. See models_out.json for output")

if __name__ == "__main__":
    cli()

