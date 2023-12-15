import sys
import duckdb
import os
import yaml
import string
import re
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import tempfile
from .parsewith import *
import fnmatch
import json


def write_pretty_json(data, output_file):
    with open(output_file, "w") as output:
        json.dump(data, output, indent=4, separators=((','), ': '))


def create_tables_from_csv(connection):
    # seeds_dir = os.path.join(os.path.dirname(__file__), "seeds")
    seeds_dir = os.path.join(os.getcwd(), "seeds")


    csv_files = [f for f in os.listdir(seeds_dir) if f.endswith(".csv")]

    for csv_file in csv_files:
        table_name = os.path.splitext(csv_file)[0]  # Remove ".csv" extension
        csv_path = os.path.join(seeds_dir, csv_file)
        query = f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}')"
        connection.execute(query)


def process_sql_content(file, query, macro_dict, variables):
    query = search_and_process_macros(query, macro_dict)
    query = reference_replacement(file, query, macro_dict, variables)

    query_query = parse_with_query(query.query)

    for name, definition in query_query.defs:
        query.add(name, definition)

    query = build_query(query_query.query, query.defs)

    return query


def run_query_and_print_result(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)

        columns = cursor.description
        column_names = [column[0] for column in columns]
        print("\t".join(column_names))

        for row in cursor.fetchall():
            print("\t".join(str(value) for value in row))


def find_file_in_directory(file_name, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == file_name:
                # print("here")
                # print(file_name)
                # print(os.path.join(root, file_name))
                return os.path.join(root, file_name)
            # else:
            #     return file_name


def find_sql_files(directory):
    sql_files = []

    for root, _, files in os.walk(directory):
        for file in fnmatch.filter(files, '*.sql'):
            sql_files.append(os.path.join(root, file))

    return sql_files


def create_temp_sql_file(filename, content):
    temp_file = tempfile.NamedTemporaryFile(
        suffix=".sql", delete=False, prefix=filename)
    temp_filename = temp_file.name

    temp_file.write(content.encode())
    temp_file.close()

    return temp_filename


def is_sql_file(filename):
    if filename.lower().endswith('.sql'):
        return True
    else:
        return False


def build_query(final_query, final_with_clause):
    query = ''

    if len(final_with_clause) > 0:
        query += 'WITH '
        for index, (name, definition) in enumerate(final_with_clause):
            query += name + " AS " + "( " + definition + " )"
            if index != len(final_with_clause) - 1:
                query += ', '

    query += " " + final_query[0]

    return query


def create_macro_dictionary(file_path):
    macro_dictionary = {}

    with open(file_path, 'r') as file:
        file_content = file.read()

        # Use regular expressions to find macro blocks
        macro_blocks = re.findall(
            r"{% macro\s+(\w+)\s*\((.*?)\) %}(.*?){% endmacro %}", file_content, re.DOTALL | re.MULTILINE)
        macro_blocks = re.findall(
            r"{% macro\s+(\w+)\s*\((.*?)\) %}(.*?){% endmacro %}", file_content, re.DOTALL)

        # Process each macro block
        for macro_match in macro_blocks:
            macro_name = macro_match[0]
            macro_parameters_string = macro_match[1].split(',')
            macro_parameters = []
            for paramter in macro_parameters_string:
                paramter = paramter.strip()
                macro_parameters.append(paramter)
            # print(macro_parameters)
            macro_args_count = len(macro_parameters)
            # print(macro_args_count)
            macro_content = macro_match[2].strip()

            macro_dictionary[macro_name] = {
                'parameters': macro_parameters,
                'parameters_count': macro_args_count,
                'content': macro_content
            }
    return macro_dictionary


def create_macro_dictionary_from_macro_models():
    macros_dictionary = {}
    # Get the current directory
    current_directory = os.getcwd()

    # Check if the 'modelout' folder exists within the current directory
    models_directory = os.path.join(current_directory, 'macros')
    if not os.path.exists(models_directory) or not os.path.isdir(models_directory):
        print("The 'macros' folder does not exist within the current directory.")
        return
    else:
        for root, _, files in os.walk(models_directory):
            for file in files:
                file_path = os.path.join(root, file)
                cur_dict = create_macro_dictionary(file_path)
                macros_dictionary.update(cur_dict)

    return macros_dictionary


def search_and_process_macros(string, macros_dict):

    macro_pattern = r"\{\{\ ([^{}]*?)\(([^{}]*?)\)\ }}"
    macro_matches = re.findall(macro_pattern, string)

    if len(macro_matches) == 0:
        return string

    for macro_match in macro_matches:
        macro_name = macro_match[0]
        macro_parameters = macro_match[1].split(',')

        if macro_name in macros_dict:
            macro_info = macros_dict[macro_name]
            macro_info_content = macro_info['content']
            macro_info_parameters = macro_info['parameters']
            macro_args_count = macro_info['parameters_count']

            if len(macro_parameters) == macro_args_count:
                # Process the macro content with the parameters
                processed_macro = macro_info_content
                for i in range(0, macro_args_count):
                    if isinstance(macro_parameters[i], str) and len(macro_parameters[i]) >= 2 and macro_parameters[i][0] == "'" and macro_parameters[i][-1] == "'":
                        macro_parameters[i] = macro_parameters[i][1:-1]
                    processed_macro = processed_macro.replace(
                        '{{ ' + macro_info_parameters[i] + ' }}', macro_parameters[i])
                string = string.replace(
                    '{{ '+macro_name+'('+macro_match[1]+') }}', processed_macro)
                string = search_and_process_macros(string, macros_dict)
            else:
                print(
                    f"Macro '{macro_name}' has incorrect number of arguments.")
    return string


"""
Replace the variable within a SQL script with their specified value:

Args:
    variables: A dictionary of the variable and their assigned value
    sql_script: a SQL script in string format, which contain variables that need to be replaced with value
    
Return:
    A new SQL script with the variables replaced by their assigned value
    
Example:
    variables:
        test1: 'gid'
    sql_script: SELECT var('test1') from my_table
    
    >>>> variable_replacement(variables,sql_script:)
    >>>>> SELECT 'gid' from my_table
    
"""


def variable_replacement(variables, sql_script,):
    for variable, value in variables.items():
        pattern = r'var\(\'' + variable + r'\'\)'
        if isinstance(value, str):
            replacement = "'" + value + "'"
        else:
            replacement = str(value)
        sql_script = re.sub(pattern, replacement, sql_script)

    return sql_script


"""
Inlining SQL queries reference with CTEs (WITH clause) 
Args:
    sql_file_name: Name of the sql file we want to process (ex: sample.sql)
    sql_script: Content of that SQL file (ex:
    " WITH foo AS (
    SELECT * FROM {{ref("bar")}})
    SELECT * FROM foo)"
    
Return:
    A new SQL script with CTEs (WITH clause) to reference files
    
Example:
    Using the sample Args above:
    Definition of bar (in a seperate SQL file):
      SELECT * from baaz

    >>>> reference_replacement(sample.sql,sql_script)
    >>>>> "WITH foo AS (
    WITH bar AS ( SELECT * from baaz )
    SELECT * FROM bar
  )
  SELECT * FROM foo
"
"""


def reference_replacement(sql_file_name, sql_script, macro_dict, variables):
    refPattern = r"ref\('(.+?)'\)"
    vertexList = set()
    vertexList.add(sql_file_name)
    edgesList = []
    q = deque()
    q.append(sql_file_name)

    directory_to_search = os.getcwd()

    # Using BFS to get all reference SQL files
    while len(q) != 0:
        cur = q.popleft()
        if os.path.sep in cur:
            if os.path.isfile(cur):
                file_path = cur
        else:
            file_path = find_file_in_directory(cur, directory_to_search)
        # print(cur)
        # print(file_path)
        with open(file_path, 'r') as curSqlFile:
            curSqlScript = curSqlFile.read()
        for match in re.finditer(refPattern, curSqlScript):
            fileName = match.group(1) + '.sql'
            if fileName not in vertexList:
                vertexList.add(fileName)
                # print("here")
                # print(fileName)
                q.append(fileName)
            edgesList.append((cur, fileName))

    G = nx.DiGraph()
    G.add_nodes_from(vertexList)
    G.add_edges_from(edgesList)

    # Draw the graph - For Debugging only
    # nx.draw(G, with_labels=True)

    # Display the graph - For Debugging only
    # plt.show()

    is_dag = nx.is_directed_acyclic_graph(G)
    if not is_dag:
        print("Invalid SQL statement")
        sys.exit()

    topological_order = list(nx.topological_sort(G))

    sql_content_list = []
    sql_content_list.append((sql_file_name, sql_script))

    for file_name in topological_order[1:]:
        filename = find_file_in_directory(file_name, directory_to_search)
        with open(filename, 'r') as file:
            sql_content = file.read()
            sql_content = search_and_process_macros(sql_content, macro_dict)
            sql_content_list.append((file_name, sql_content))

    defs = []
    for file_name, file_content in reversed(sql_content_list):
        vertices_with_incoming_edges = [u for u, v in G.in_edges(file_name)]
        file_without_extension = os.path.splitext(file_name)[0]
        pattern1 = r"ref\('" + file_without_extension + r"'\)"
        pattern2 = r"ref\('" + file_without_extension + r"'\)"

        for index, (file_name_inner_loop, file_content_inner_loop) in enumerate(sql_content_list):
            # If a file contain a reference to our current file name, update the content of that file with CTEs
            if file_name_inner_loop in vertices_with_incoming_edges:
                new_query = re.sub(
                    pattern1, file_without_extension, file_content_inner_loop)
                new_query = re.sub(
                    pattern2, file_without_extension, file_content_inner_loop)
                file_content_inner_loop = new_query
                sql_content_list[index] = (
                    file_name_inner_loop, file_content_inner_loop)

    # Traverse the files in reveresed topo sort order, and replace the ref with CTEs (WITH CLAUSE) recursively
    for index, (file_name, file_content) in enumerate(reversed(sql_content_list)):
        file_without_extension = os.path.splitext(file_name)[0]
        if index == len(sql_content_list)-1:
            query = file_content
        elif index == len(sql_content_list)-2:
            defs.append((file_without_extension, file_content))
        else:
            defs.append((file_without_extension, file_content))

    result = Query(defs, query)

    return result
