import csv
import json
import sys
import os
import xml.etree.ElementTree as ET


#read file using utf-8 if doesn't work use latin-1 -> convert rows in lists
def read_tab_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as f:
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
    return rows[0], rows[1:]


#csv file conversion -> writes headers and data to a CSV file using utf-8 encoding
def write_csv(headers, data, output_filename):
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"CSV file saved as {output_filename}")


#json file conversion -> converts data to JSON format by mapping headers to each row's values
def write_json(headers, data, output_filename):
    json_data = []
    for row in data:
        row_dict = {}
        for i in range(len(headers)):
            row_dict[headers[i]] = row[i]
        json_data.append(row_dict)
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)
    print(f"JSON file saved as {output_filename}")


#xml file conversion -> converts data to XML format by creating XML elements for each row
def write_xml(headers, data, output_filename):
    root = ET.Element('Data')
    for row in data:
        item = ET.SubElement(root, 'Row')
        for i in range(len(headers)):
            field = ET.SubElement(item, headers[i].replace(' ', '_'))
            field.text = row[i]
    tree = ET.ElementTree(root)
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)
    print(f"XML file saved as {output_filename}")


#check if user input filename and flag for each option
def main():
    if len(sys.argv) != 3:
        print("Usage: python tab_converter.py <filename> <-c|-j|-x>")
        sys.exit(1)

    filename = sys.argv[1]
    format_flag = sys.argv[2]

    if not os.path.isfile(filename):
        print(f"File '{filename}' not found.")
        sys.exit(1)

    headers, data = read_tab_file(filename)
    base_name = os.path.splitext(os.path.basename(filename))[0]

    if format_flag == '-c':
        write_csv(headers, data, f"{base_name}.csv")
    elif format_flag == '-j':
        write_json(headers, data, f"{base_name}.json")
    elif format_flag == '-x':
        write_xml(headers, data, f"{base_name}.xml")
    else:
        print("Invalid format. Use -c for CSV, -j for JSON, -x for XML.")
        sys.exit(1)


if __name__ == "__main__":
    main()
