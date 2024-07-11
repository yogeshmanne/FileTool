import pandas as pd
import os
from lxml import etree

def process_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    elif file_extension == '.json':
        df = pd.read_json(file_path)
    elif file_extension == '.txt':  # Add support for text files (.txt)
        # Assuming text file is tab-separated, adjust delimiter as needed
        df = pd.read_csv(file_path, delimiter='\t')
    else:
        raise ValueError("Unsupported file format: Only CSV, Excel, JSON, and TXT files are supported.")
    
    return df

def sanitize_column_name(name):
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Remove any invalid characters and ensure it starts with a letter or underscore
    valid_name = ''.join(char if char.isalnum() or char == '_' else '' for char in name)
    if not valid_name[0].isalpha() and valid_name[0] != '_':
        valid_name = '_' + valid_name
    return valid_name

def convert_to_xml(df, output_file):
    root = etree.Element('root')
    sanitized_columns = {col: sanitize_column_name(col) for col in df.columns}
    for i, row in df.iterrows():
        row_element = etree.SubElement(root, 'row')
        for field, value in row.items():
            field_element = etree.SubElement(row_element, sanitized_columns[field])
            field_element.text = str(value)
    tree = etree.ElementTree(root)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding='utf-8')