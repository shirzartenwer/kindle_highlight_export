'''To import my kindle highlight to Readwise'''
import re 
import os 
from typing import Dict, List
import csv 
import pandas as pd

def get_kindle_highlights(dict_list, input_file_path, output_file_path):
    with open(input_file_path) as infile, open(output_file_path, 'w') as outfile:
        last_line_was_seperator = True
        last_line_was_blank = False
        last_line_was_info = False
        for line in infile:
            if last_line_was_seperator:
                out_put_header["Title"].append(line)
                last_line_was_seperator = False
                continue
            elif not last_line_was_blank and line.startswith("-"):
                # Location and date are not yet properly separated.
                start = "-"
                middle = "|"
                location = line[len(start):-len(middle)]
                time = line[len(middle):]
                # location = re.search('- (.*)|', line).group(1)
                # time = re.search('|(.*)', line).group(1)
                out_put_header["Location"].append(location)
                out_put_header["Date"].append(time)
                last_line_was_blank = False
                last_line_was_seperator = False
                last_line_was_info = True
                continue
            elif line.strip() =="" and last_line_was_info:
                last_line_was_blank = True
                last_line_was_seperator = False
                last_line_was_info = False
                continue
            elif last_line_was_blank:
                out_put_header["Highlight"].append(line)
                last_line_was_blank = False
                continue     
            elif line.strip() == "==========":
                last_line_was_seperator = True
                continue
    return dict_list
                
                

if __name__ == "__main__":
    out_put_header = {"Highlight": [],
                  "Title": [],
                  "Author": [],
                  "URL": [],
                  "Note": [],
                  "Location": [],
                  "Date": []}
    input_file_path = "../../MyClippings.txt"
    output_intermediate = "../../intermidiate_kindle.txt"
    result_dict_list = get_kindle_highlights(out_put_header, input_file_path, output_intermediate)
    print("Today is amazing!")
    
    df = pd.DataFrame.from_dict(result_dict_list, orient='index').transpose()
    df.to_csv("../../kindle_highlights.csv", ";", header=True, index=False)
    ### check if the output format is correct
    file = open(input_file_path, "r")
    nr_highlights = file.read().count("==========")
    
    for key, element in result_dict_list.items():
        if len(element) !=nr_highlights:
            print(f'Number of {key} collected is {len(element)}, which is not consistent with numebr of highlights')
        
    
                
                
                
                