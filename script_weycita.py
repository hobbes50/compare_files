# ,4646512
from collections import OrderedDict


VALUE_SEPARATOR=","

def compare_files(filename1, filename2):
    file1_table = OrderedDict() #key -> (value, line_number) table
    file2_table = {}

    file_deleted = open(filename2 + ".deleted", 'w')
    file_new = open(filename2 + ".new", 'w')
    file_modified = open(filename2 + ".modified", 'w')

    print("Reading original file " + filename1)
    line_number = 0
    with open(filename1, 'r') as file1:
        for line in file1:
            line_number += 1
            index_value_sep = line.rfind(VALUE_SEPARATOR)
            if (index_value_sep > 0):
                key = line[0:index_value_sep]
                value = line[index_value_sep + 1:-2]  #-2 to get rid of the line ending
                if (key in file1_table):
                    print("error: key '" + key + "' duplicated (lines " + str(file1_table[key][1]) + " and " + str(line_number) + ")")
                else:
                    file1_table[key] = (value, line_number)

    print("Comparing with new file " + filename2)
    line_number = 0
    with open(filename2, 'r') as file2:
        for line in file2:
            line_number += 1
            index_value_sep = line.rfind(VALUE_SEPARATOR)
            if (index_value_sep > 0):
                key = line[0:index_value_sep]
                value = line[index_value_sep + 1:-2] #-2 to get rid of the line ending
                
                #Check unicity in file2
                if (key in file2_table):
                    print("error: key '" + key + "' duplicated (lines " + str(file2_table[key][1]) + " and " + str(line_number) + ")")
                    continue
                else:
                    file2_table[key] = (value, line_number)

                #Look for key in file1
                if (key in file1_table):
                    (old_value, old_line_number) = file1_table[key]
                    if (value != old_value):
                       file_modified.write(key + " (lines " + str(old_line_number)  + " and " + str(line_number) +  "): " + old_value + "->" + value + "\n")
                    del file1_table[key]
                else:
                    file_new.write(key + " (line " + str(line_number) + "): " + value + "\n")

    print("Listing deleted keys in " + filename1)
    for key, item in file1_table.items():
        (old_value, old_line_number) = item
        file_deleted.write(key + " (line " + str(old_line_number) + "): " + old_value + "\n")

    file_deleted.close()
    file_new.close()
    file_modified.close()


import argparse
def main(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('file1', help='original file')
    parser.add_argument('file2', help='new file')

    args = parser.parse_args()    

    compare_files(args.file1, args.file2)

    return 0

if __name__ == "__main__":
    main()
