import pandas as pd
import csv
from itertools import combinations
import re

#Input Parser:
# Read the csv file and functional dependencies file
file = pd.read_csv('exampleInputTable.csv')

with open('functional_dependencies.txt', 'r') as f:
    lines = [line.strip() for line in f]

dependencies = {}
for line in lines:
    determinent, dependent = line.split(" -> ")
    # Seperating the determ by comma inorder to make a list
    determinent = determinent.split(", ")
    dependencies[tuple(determinent)] = dependent.split(", ")


# Taking input from user
max_normal_form = input("Choice of the highest normal form to reach (1: 1NF, 2: 2NF, 3: 3NF, B: BCNF, 4: 4NF, 5: 5NF): ")
if max_normal_form in ["1", "2", "3", "4", "5"]:
    max_normal_form = int(max_normal_form)

# To determine the highest normal form of the relation
find_highest_normalform = int(
    input('Find the highest normal form of the input table? (1: Yes, 2: No): '))
high_normalform = 'not normalized'


# Enter Key
primary_key = input(
    "Enter the primary key values seperated with commas: ").split(', ')
print('\n')

keys = ()
for key in primary_key:
    keys = keys + (key,)

primary_key = keys


def contains_comma(series):
    return series.str.contains(',').any()


def parser(file):
    file = file.astype(str)
    columns_with_commas = [
        col for col in file.columns if contains_comma(file[col])]

    for col in columns_with_commas:
        file[col] = file[col].str.split(
            ',').apply(lambda x: [item.strip() for item in x])

    return file
file = parser(file)

multivalue = {}
if not max_normal_form == 'B' and max_normal_form >= 4:
    with open('multivalued_dependencies.txt', 'r') as fil:
        mvd_lines = [line.strip() for line in fil]

    print(mvd_lines)

    for mvd in mvd_lines:
        determinent, dependent = mvd.split(" ->> ")
        determinent = determinent.split(
            ", ") if ", " in determinent else [determinent]
        determinent_str = str(determinent)
        if determinent_str in multivalue:
            multivalue[determinent_str].append(dependent)
        else:
            multivalue[determinent_str] = [dependent]


def is_list_or_set(item):
    return isinstance(item, (list, set))

def is_superkey(rel, determinent):
    grouped = rel.groupby(
        list(determinent)).size().reset_index(name='count')
    return not any(grouped['count'] > 1)

def closure(attributes, fds):
    closure_set = set(attributes)
    while True:
        closure_before = closure_set.copy()
        for determinent, dependents in fds.items():
            if set(determinent).issubset(closure_set):
                closure_set.update(dependents)
        if closure_before == closure_set:
            break
    return closure_set

def powerset(s):
    x = len(s)
    for i in range(1 << x):
        yield [s[j] for j in range(x) if (i & (1 << j)) > 0]


def bcnf_decomp(rel, dependencies):
    decomposed_t = []

    for determinent, dependent in dependencies.items():
        closure_set = closure(set(determinent), dependencies)
        if not closure_set.issuperset(rel.columns):
            cols = list(determinent) + dependent
            if set(cols).issubset(rel.columns) and not set(cols) == set(rel.columns):
                new_t = rel[list(determinent) + dependent].drop_duplicates()
                decomposed_t.append(new_t)
                rel = rel.drop(columns=dependent)

    if not decomposed_t:
        return [rel]
    else:
        return [rel] + decomposed_t


#Normal Form Finder:
def in_1nf(rel):
    if rel.empty:
        return False

    for column in rel.columns:
        unique_types = rel[column].apply(type).nunique()
        if unique_types > 1:
            return False
        if rel[column].apply(lambda x: isinstance(x, (list, dict, set))).any():
            return False

    return True


def in_2nf(primary_key, dependencies, rel):
 
    non_prime_attributes = [
        col for col in rel.columns if col not in primary_key]

    for determinent, dependents in dependencies.items():
        if set(determinent).issubset(primary_key) and set(determinent) != set(primary_key):
            if any(attr in non_prime_attributes for attr in dependents):
               return False
    return True

def in_3nf(rels, dependencies):
    primary_keys = [key for key in dependencies]
    non_key_attributes = [item for sublist in dependencies.values()
                          for item in sublist]
    for rel_name, rel in rels.items():
        for determinent, dependents in dependencies.items():
            if set(determinent).issubset(set(rel.columns)) and not set(determinent).issubset(primary_keys) and set(dependents).issubset(non_key_attributes):
                return False
    return True


def in_bcnf(rels, primary_key, dependencies):
    for rel_name, rel in rels.items():
        all_attri = set(rel.columns)
        for determinent, dependents in dependencies.items():
            for dependent in dependents:
                if dependent not in determinent:
                    if all_attri - closure(determinent, dependencies):
                        return False
    return True


def in_4nf(rels, multivalue):
    for rel_name, rel in rels.items():
        for determinent, dependents in multivalue.items():
            for dependent in dependents:
                if isinstance(determinent, tuple):
                    determinent_cols = list(determinent)
                else:
                    determinent_cols = [determinent]

                if all(col in rel.columns for col in determinent_cols + [dependent]):
                    grouped = rel.groupby(determinent_cols)[
                        dependent].apply(set).reset_index()
                    if len(grouped) < len(rel):
                        print(
                            f"violation of multi-valued dependencies: {determinent} ->> {dependent}")
                        return False

    return True


def in_5nf(rels):
    candidate_keys_dict = {}
    for rel_name, rel in rels.items():
        print(rel)
        user_input = input("Enter the candidate keys ")
        print('\n')
        tuples = re.findall(r'\((.*?)\)', user_input)
        candidate_keys = [tuple(map(str.strip, t.split(','))) for t in tuples]
        candidate_keys_dict[rel_name] = candidate_keys

    print(f'the Candidate Keys for given relation:')
    print(candidate_keys_dict)
    print('\n')

    for rel_name, rel in rels.items():
        candidate_keys = candidate_keys_dict[rel_name]

        data_tuples = [tuple(row) for row in rel.to_numpy()]

        
        def project(data, attributes):
            return {tuple(row[attr] for attr in attributes) for row in data}

        # to check if the given attributes are a super key
        def is_superkey(attributes):
            for key in candidate_keys:
                if set(key).issubset(attributes):
                    return True
            return False, candidate_keys_dict

        for i in range(1, len(rel.columns)):
            for attrs in combinations(rel.columns, i):
                
                if is_superkey(attrs):
                    continue

                # Project the data onto the attributes and their complement
                projected_data = project(data_tuples, attrs)
                complement_attrs = set(rel.columns) - set(attrs)
                complement_data = project(data_tuples, complement_attrs)
                # combine the projected data and check whether it is equals to the original data

                
                joined_data = {(row1 + row2)
                               for row1 in projected_data for row2 in complement_data}
                if set(data_tuples) != joined_data:
                    print("Not satisfy 5NF then check attribures:", attrs)
                    return False, candidate_keys_dict

    return True, candidate_keys_dict

#Normalizer:
def first_normal_form(rel, primary_key):
    rels = {}
    one_flag = in_1nf(rel)

    if one_flag:
        rels[primary_key] = rel
        return rels, one_flag
    else:
        for col in rel.columns:
            if rel[col].apply(is_list_or_set).any():
                rel = rel.explode(col)
        rels[primary_key] = rel
        return rels, one_flag

def second_normal_form(rel, primary_key, dependentencies):
    rel = rel[primary_key]
    rels = {}
    rm_cols = []
    two_flag = in_2nf(primary_key, dependentencies, rel)

    if two_flag:
        rels[primary_key] = rel
        return rels, two_flag
    else:
        non_prime_attributes = [
            col for col in rel.columns if col not in primary_key]
        for determinent, dependents in dependencies.items():
            if set(determinent).issubset(primary_key) and set(determinent) != set(primary_key):
                if any(attr in dependents for attr in non_prime_attributes):
                    new_rel = rel[list(determinent) + dependents].drop_duplicates()
                    rels[tuple(determinent)] = new_rel
                    for attr in dependents:
                        if attr not in determinent and attr not in rm_cols:
                            rm_cols.append(attr)

        rel.drop(columns=rm_cols, inplace=True)
        rels[primary_key] = rel
        return rels, two_flag


def third_normal_form(rels, primary_key, dependencies):
    three_rels = {}
    original_rel = rels
    three_flag = in_3nf(rels, dependencies)

    if three_flag:
        return rels, three_flag
    else:
        for rel_name, rel in rels.items():
            for determinent, dependents in dependencies.items():
                if set(determinent).issubset(set(rel.columns)) and not set(dependents).issubset(determinent):
                    new_cols = list(set(determinent).union(dependents))

                    if set(new_cols).issubset(set(rel.columns)) and not set(new_cols) == set(rel.columns):
                        table1_cols = list(determinent) + dependents
                        table2_cols = list(set(rel.columns) - set(dependents))

                        new_table1 = rel[table1_cols].drop_duplicates(
                        ).reset_index(drop=True)
                        new_table2 = rel[table2_cols].drop_duplicates(
                        ).reset_index(drop=True)
                        three_rels[tuple(determinent)] = new_table1
                        three_rels[rel_name] = new_table2
                        break
            else:
                three_rels[rel_name] = rel

        return three_rels, three_flag


def bc_normal_form(rels, primary_key, dependencies):
    bcnf_rels = {}
    bcnf_final = {}
    bcnf_flag = in_bcnf(rels, primary_key, dependencies)

    if bcnf_flag:
        return rels, bcnf_flag
    else:
        for rel_name, rel in rels.items():

            for determinent, dependents in dependencies.items():
                closure_set = closure(set(determinent), dependencies)
                if not closure_set.issuperset(rel.columns):
                    cols = list(determinent) + dependents
                    if set(cols).issubset(rel.columns) and not set(cols) == set(rel.columns):
                        new_table = rel[list(determinent) + dependents].drop_duplicates()
                        bcnf_rels[tuple(determinent)] = new_table
                        rel = rel.drop(columns=dependents)

            bcnf_rels[rel_name] = rel

    return bcnf_rels, bcnf_flag


def fourth_normal_form(rels, multivalue):
    four_rels = {}
    four_flag = in_4nf(rels, multivalue)

    if four_flag:
        return rels, four_flag
    else:
        for rel_name, rel in rels.items():
            for determinent, dependents in multivalue.items():
                for dependent in dependents:
                    if isinstance(determinent, tuple):
                        determinent_cols = list(determinent)
                    else:
                        determinent_cols = [determinent]

                    if all(col in rel.columns for col in determinent_cols + [dependent]):
                        grouped = rel.groupby(determinent_cols)[
                            dependent].apply(set).reset_index()
                        if len(grouped) < len(rel):
                            # Decomposition
                            table_1 = rel[determinent_cols +
                                               [dependent]].drop_duplicates()
                            four_rels[tuple(determinent_cols)] = table_1
                            table_2 = rel[determinent_cols + [col for col in rel.columns if col not in [
                                dependent] + determinent_cols]].drop_duplicates()
                        
                            four_rels[rel_name] = table_2

                            break
                else:
                    continue
                break
            else:
                four_rels[rel_name] = rel

    if len(four_rels) == len(rels):
        return four_rels 
    else:
        return fourth_normal_form(four_rels, multivalue)


def decomposing_to_5nf(rel_name, dataframe, candidate_keys):
    
    def project(df, attributes):
        return df[list(attributes)].drop_duplicates().reset_index(drop=True)

    # find whether the decomposition is loseless
    def is_lossless(df, df1, df2):
        common_columns = set(df1.columns) & set(df2.columns)
        if not common_columns:
            return False
        joined_df = pd.merge(df1, df2, how='inner', on=list(common_columns))
        return df.equals(joined_df)

    decomposed_tables = [dataframe]

    # check for each candidate key and thn decompose the table
    for key in candidate_keys:
        new_tables = []
        for table in decomposed_tables:
            if set(key).issubset(set(table.columns)):
                table1 = project(table, key)
                remaining_columns = set(table.columns) - set(key)
                table2 = project(table, remaining_columns | set(key))

                # Check if the decomposition is lossless
                if is_lossless(table, table1, table2):
                    new_tables.extend([table1, table2])
                else:
                    new_tables.append(table)
            else:
                new_tables.append(table)
        decomposed_tables = new_tables

    return decomposed_tables


def fifth_normal_form(rels, primary_key, dependencies):
    five_rels = {}
    five_flag, candidate_keys_dict = in_5nf(rels)

    if five_flag:
        return rels, five_flag
    else:
        for rel_name, rel in rels:
            candidate_keys = candidate_keys_dict[rel_name]
            decomposed_rels = decomposing_to_5nf(
                rel_name, rel, candidate_keys)
            five_rels.append(decomposed_rels)

    return five_rels, five_flag

# Used to generate output as per the requirement
def output_type(dtype):
    """change pandas dtype to SQL data type."""
    if "int" in str(dtype):
        return "INT"
    elif "float" in str(dtype):
        return "FLOAT"
    elif "object" in str(dtype):
        return "VARCHAR(255)"
    elif "datetime" in str(dtype):
        return "DATETIME"
    else:
        return "TEXT"

#SQL Query Generator: 
def sql_query_1NF(primary_keys, df):
    primary_key = list(df.keys())[0]
    t_name = "_".join(primary_key) + "_table"
    df = df[primary_key]
    t_name = "_".join(primary_keys) + "_table"

    # Create SQL Query
    query = f"CREATE TABLE {t_name} (\n"

    # Iterate through columns to create query
    for col, dtype in zip(df.columns, df.dtypes):
        if col in primary_keys:
            query += f"  {col} {output_type(dtype)} PRIMARY KEY,\n"
        else:
            query += f"  {col} {output_type(dtype)},\n"

    
    query = query.rstrip(',\n') + "\n);"

    with open('output.txt', 'w') as file: 
        file.write(query)
    print(query)



def sql_query(rels):
    sql_queries = []
    for rel_name, rel in rels.items():
        primary_keys = rel_name
        primary_keys = (primary_keys,) if isinstance(
            primary_keys, str) else primary_keys
        t_name = "_".join(primary_keys) + '_table'
        if t_name.count('_') >= 2:
            query = f"CREATE TABLE {t_name} (\n"

            for col, dtype in zip(rel.columns, rel.dtypes):
                if col in primary_keys:
                    query += f" FOREIGN KEY ({col}) REFERENCES {col.replace('_fk','')}_table({col.replace('_fk','')}),\n"
                else:
                    query += f"  {col} {output_type(dtype)},\n"

            query = query.rstrip(',\n') + "\n);"
        else:
            query = f"CREATE TABLE {t_name} (\n"

            for col, dtype in zip(rel.columns, rel.dtypes):
                if col in primary_keys:
                    query += f"  {col} {output_type(dtype)} PRIMARY KEY,\n"
                else:
                    query += f"  {col} {output_type(dtype)},\n"

            query = query.rstrip(',\n') + "\n);"

        sql_queries.append(query)

    print(sql_queries)
    with open('output.txt', 'w') as file:
        for query in sql_queries:
            file.write(query)
            file.write('\n')


if max_normal_form == 'B' or max_normal_form >= 1:
    onenf_table, one_flag = first_normal_form(
        file, primary_key)
    if one_flag:
        high_normalform = 'Highest normal form of the input table: 1NF'
        
    if max_normal_form == 1:
        if one_flag:
            print('The table is already in 1NF')
            print('\n')

        sql_query_1NF(primary_key, onenf_table)

if max_normal_form == 'B' or max_normal_form >= 2:
    twonf_tables, two_flag = second_normal_form(
        onenf_table, primary_key, dependencies)
    if one_flag and two_flag:
        high_normalform = 'Highest normal form of the input table: 2NF'

    if max_normal_form == 2:
        if two_flag and one_flag:
            print('The table is already in 2NF')
            print('\n')

        sql_query(twonf_tables)

if max_normal_form == 'B' or max_normal_form >= 3:
    threenf_tables, three_flag = third_normal_form(
        twonf_tables, primary_key, dependencies)
    
    if one_flag and two_flag and three_flag:
        high_normalform = 'Highest normal form of the input table: 3NF'
        
    if max_normal_form == 3:
        if three_flag and two_flag and one_flag:
            print('The table is already in 3NF')
            print('\n')

        sql_query(threenf_tables)

if max_normal_form == 'B' or max_normal_form >= 4:
    bcnf_tables, bcnf_flag = bc_normal_form(
        threenf_tables, primary_key, dependencies)
    
    if one_flag and two_flag and three_flag and bcnf_flag:
        high_normalform = 'Highest normal form of the input table: BCNF'
        
    if max_normal_form == 'B':
        if bcnf_flag and three_flag and two_flag and one_flag:
            print('The table is already in BCNF')
            print('\n')

        sql_query(bcnf_tables)

if not max_normal_form == 'B' and max_normal_form >= 4:
    fournf_tables, four_flag = fourth_normal_form(
        bcnf_tables, multivalue)
    
    if one_flag and two_flag and three_flag and bcnf_flag and four_flag:
        high_normalform = 'Highest normal form of the input table: 4NF'
        
    if max_normal_form == 4:
        if four_flag and bcnf_flag and three_flag and two_flag and one_flag:
            print('The table is already in 4NF')
            print('\n')

        sql_query(fournf_tables)

if not max_normal_form == 'B' and max_normal_form >= 5:
    fivenf_tables, five_flag = fifth_normal_form(
        fournf_tables, primary_key, dependencies)
    
    if one_flag and two_flag and three_flag and bcnf_flag and four_flag and five_flag:
        high_normalform = 'Highest normal form of the input table: 5NF'
        
    if max_normal_form == 5:
        if five_flag and four_flag and bcnf_flag and three_flag and two_flag and one_flag:
            print('The table is already in 5NF')
            print('\n')

        sql_query(fivenf_tables)
        

if find_highest_normalform == 1 :
    print('\n')
    print(high_normalform)

    file_path = 'output.txt'
    with open(file_path, 'r') as file:
        existing_content = file.read()

    # Add new lines to the existing content
    updated_content = existing_content + high_normalform

    # Write the updated content back to the file
    with open(file_path, 'w') as updated_path:
        updated_path.write(updated_content)
    print('\n')