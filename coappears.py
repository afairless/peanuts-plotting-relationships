#! /usr/bin/env python3


def get_sibling_directory_path(sibling_directory_name):
    '''
    returns path for a specified folder that is in the same parent directory as
        the current working directory
    '''

    import os

    current_path = os.getcwd()
    last_separator_position = current_path.rfind(os.sep)
    parent_directory_path = current_path[0:last_separator_position]
    sibling_directory_path = os.path.join(parent_directory_path,
                                          sibling_directory_name)

    return(sibling_directory_path)


def count_coappearances(table, col_name1, col_name2):
    '''
    Calculates each character's number of appearances, their number of
        co-appearances, and their number of co-appearances as a proportion of
        how many times either appeared

    'table' - Boolean table/dataframe (i.e., all cells are zeroes or ones);
        each column represents a character; each row represents a potential
        appearance; ones represent appearances
    'col_name1', 'col_name2' - each is a name of a column in 'table'
    '''

    n_appears_1 = table[col_name1].sum()
    n_appears_2 = table[col_name2].sum()
    n_coappears = (table[col_name1] & table[col_name2]).sum()
    n_either_appears = (table[col_name1] | table[col_name2]).sum()

    if n_either_appears > 0:
        prop_coappears = n_coappears / n_either_appears
    else:
        prop_coappears = None

    return(n_appears_1,n_appears_2, n_coappears, prop_coappears)


def create_coappears_dataframe(table, pairs):
    '''
    Creates table with each character's number of appearances, each character
        pair's number of co-appearances, and each character pair's
        number of co-appearances as a proportion of the number of times either
        character appeared

    'table' - Boolean table/dataframe (i.e., all cells are zeroes or ones);
        each column represents a character; each row represents a potential
        appearance; ones represent appearances
    'pairs' - list of pairs of characters
    '''

    import pandas as pd

    col_names = ['source',          # name required for D3 force network graph
                 'target',          # name required for D3 force network graph
                 'number_appearances_char1',
                 'number_appearances_char2',
                 'number_coappearances',
                 'proportion_coappearances']

    coappears_list = []

    for e in pairs:
        n_appears1, n_appears2, n_coappears, prop_coappears = (
            count_coappearances(table, e[0], e[1]))
        coappears_list.append([e[0], e[1], n_appears1, n_appears2,
                               n_coappears, prop_coappears])

    coappears = pd.DataFrame.from_records(coappears_list, columns=col_names)

    return(coappears)


def prettify_character_names(table):
    '''
    Replaces 'snoopy and personas' with 'snoopy' and capitalizes names in first
        two columns of table
    '''

    original = 'snoopy and personas'
    replacement = 'snoopy'

    table.iloc[:, 0] = table.iloc[:, 0].str.replace(original, replacement)
    table.iloc[:, 1] = table.iloc[:, 1].str.replace(original, replacement)

    table.iloc[:, 0] = table.iloc[:, 0].str.title()
    table.iloc[:, 1] = table.iloc[:, 1].str.title()

    return(table)


def list_to_prettified_df(a_list, counts_df):
    '''
    Converts list of Peanuts character names to table/dataframe with rows
        representing every unique pair of characters
    Character names are capitalized and 'snoopy and personas' is replaced with
        'snoopy'
    '''

    from itertools import combinations

    pairs = list(combinations(a_list, 2))
    coappears = create_coappears_dataframe(counts_df, pairs)
    coappears = prettify_character_names(coappears)

    return(coappears)


def read_text_file(text_filename, as_string=False):
    '''
    reads each line in a text file as a list item and returns list by default
    if 'as_string' is 'True', reads entire text file as a single string
    '''

    text_list = []

    try:
        with open(text_filename) as text:
            if as_string:
                # reads text file as single string
                text_list = text.read().replace('\n', '')
            else:
                # reads each line of text file as item in a list
                for line in text:
                    text_list.append(line.rstrip('\n'))
            text.close()
        return(text_list)

    except:
        return('There was an error while trying to read the file')


def write_list_to_text_file(a_list, text_file_name, overwrite_or_append='a'):
    '''
    writes a list of strings to a text file
    appends by default; change to overwriting by setting to 'w' instead of 'a'
    '''

    try:
        textfile = open(text_file_name, overwrite_or_append, encoding='utf-8')
        for element in a_list:
            textfile.write(element)
            textfile.write('\n')

    finally:
        textfile.close()


def append_commas_to_list_elements_except_last(a_list):
    '''
    Appends a comma to each element of a list except for the last element
    '''

    a_list = [e + ',' for e in a_list]
    a_list[-1] = a_list[-1][:-1]

    return(a_list)


def assemble_json(nodes_json_file, links_json_file, assembled_file):
    '''
    Reads JSON files for information on nodes and links of network and assembles
        it into a single JSON file that designates the nodes and links
    '''

    nodes = read_text_file(nodes_json_file)
    links = read_text_file(links_json_file)

    nodes_start = ['{', '"nodes": [']
    nodes_end = ['],']
    links_start = ['"links": [']
    links_end = [']', '}']

    nodes = append_commas_to_list_elements_except_last(nodes)
    links = append_commas_to_list_elements_except_last(links)

    write_list_to_text_file(nodes_start, assembled_file, 'w')
    write_list_to_text_file(nodes, assembled_file)
    write_list_to_text_file(nodes_end, assembled_file)
    write_list_to_text_file(links_start, assembled_file)
    write_list_to_text_file(links, assembled_file)
    write_list_to_text_file(links_end, assembled_file)


def convert_to_color_strings(table):
    '''
    Converts table of red-green-blue color specifications into strings
    'table' - dataframe of 4 columns with each row representing a color; the
        2nd, 3rd, and 4th columns represent red, green, and blue, respectively,
        with values ranging from 0 to 255
    '''

    rgb_strings = []

    for i in range(len(table)):
        r = table.iloc[i, 1]
        g = table.iloc[i, 2]
        b = table.iloc[i, 3]
        rgb_string = 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        rgb_strings.append(rgb_string)

    return(rgb_strings)


def main():
    '''
    Calculates the strength of Peanuts' characters relationships in terms of
        raw numbers (i.e., number of comics in which they appear together, or
        co-appearances) and as a proportion of the number of comics
        in which either character appeared
    Calculates relationship strengths for 3 sets of characters:  all characters,
        the 17 characters with the most appearances, and all characters who are
        distinctly named and appear in the strip (as opposed to merely
        being mentioned)
    JSON output is in format suitable for display as a D3 network force graph
    '''

    import os
    import pandas as pd
    from itertools import combinations

    data_source_folder = '30_character_appear'
    data_source_path = get_sibling_directory_path(data_source_folder)
    data_source_file = 'counts_by_comic_1_overall.csv'
    data_source_filepath = os.path.join(data_source_path, data_source_file)
    counts = pd.read_csv(data_source_filepath)

    # all characters
    character_pairs = list(combinations(counts.columns[1:], 2))
    coappears = create_coappears_dataframe(counts, character_pairs)
    coappears.to_csv('coappearances_all.csv', index=False)
    #coappears.to_json('coappearances_all.json', orient='records', lines=True)

    # top 17 characters
    top17_list = ['charlie brown', 'snoopy and personas', 'lucy', 'linus',
                  'peppermint patty', 'sally', 'marcie', 'woodstock',
                  'schroeder', 'patty', 'violet', 'rerun', 'spike', 'shermy',
                  'pig-pen', 'frieda', 'franklin']

    top17_coappears = list_to_prettified_df(top17_list, counts)
    top17_coappears.to_csv('coappearances_top17.csv', index=False)
    links_json_file = 'top17_coappearances.json'
    top17_coappears.to_json(links_json_file, orient='records', lines=True)

    top17_colors = pd.read_csv('character_colors.csv')
    top17_rgb_strings = convert_to_color_strings(top17_colors)
    top17_pretty = [e.title() for e in top17_list]
    top17_pretty[1] = 'Snoopy'
    group_placeholder = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 1, 2, 3, 4, 5, 1, 2]
    top17_appears = counts.ix[:, top17_list].sum().tolist()
    top17_nodes = [('id', top17_pretty),
                   ('group', group_placeholder),
                   ('n_appears', top17_appears),
                   ('colors', top17_rgb_strings)]
    top17_nodes = pd.DataFrame.from_items(top17_nodes)
    nodes_json_file = 'top17_nodes.json'
    top17_nodes.to_json(nodes_json_file, orient='records', lines=True)

    assembled_file = 'top17_network.json'
    assemble_json(nodes_json_file, links_json_file, assembled_file)

    # all distinct, named characters that appear (as opposed to only mentioned)
    adn_list = ['charlie brown', 'snoopy and personas', 'lucy', 'linus',
                'peppermint patty', 'sally', 'marcie', 'woodstock', 'schroeder',
                'patty', 'violet', 'rerun', 'spike', 'shermy', 'pig-pen',
                'frieda', 'franklin', 'peggy jean', 'molly volley',
                'charlotte braun', 'crybaby boobie', 'tapioca pudding',
                'pigtailed girl', 'kite-eating tree', 'andy', 'olaf', 'eudora',
                'truffles', 'roy', 'cormac', 'thibault', 'sophie', 'poochie',
                'joe richkid', 'joe agate', 'naomi', 'maynard', 'lydia', 'lila',
                'larry', 'royanne', 'harold', 'benny', 'clara', 'emily',
                'ethan', 'floyd', 'shirley', 'belle', 'faron', 'harriet',
                'bill', 'conrad', 'olivier', 'raymond', 'fred', 'wilson']

    adn_coappears = list_to_prettified_df(adn_list, counts)
    adn_coappears.to_csv('coappearances_adn.csv', index=False)
    links_json_file = 'adn_coappearances.json'
    adn_coappears.to_json(links_json_file, orient='records', lines=True)

    gray_rgb_strings = ['rgb(169, 169, 169)'] * (len(adn_list) - len(top17_list))
    adn_rgb_strings = top17_rgb_strings
    adn_rgb_strings.extend(gray_rgb_strings)
    adn_pretty = [e.title() for e in adn_list]
    adn_pretty[1] = 'Snoopy'
    group_placeholder = [1] * len(adn_list)
    adn_appears = counts.ix[:, adn_list].sum().tolist()
    adn_nodes = [('id', adn_pretty),
                 ('group', group_placeholder),
                 ('n_appears', adn_appears),
                 ('colors', adn_rgb_strings)]
    adn_nodes = pd.DataFrame.from_items(adn_nodes)
    nodes_json_file = 'adn_nodes.json'
    adn_nodes.to_json(nodes_json_file, orient='records', lines=True)

    assembled_file = 'adn_network.json'
    assemble_json(nodes_json_file, links_json_file, assembled_file)


if __name__ == '__main__':
    main()
