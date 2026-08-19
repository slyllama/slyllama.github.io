# make.py
# Much simpler version of makesly.py, probably for asuran stuff

import json
import os
import shutil

INDENT = "        "
PAGES_FILE = "rats/pages.json"
OUTPUT_ROOT_PATH = "rats/page/"
SOURCE_PATH = "rats/source/"
TEMPLATE = ""
TEMPLATE_FILE = "rats/template.html"

# Check if pages file exists
if os.path.isfile(PAGES_FILE) == False:
    print("Missing '" + PAGES_FILE + "'.")
    quit()

# Populate template
with open(TEMPLATE_FILE) as template_file:
    TEMPLATE = template_file.read()

with open(PAGES_FILE) as pages_file:
    pages_data = json.load(pages_file)
    for entry in pages_data:
        source_path = SOURCE_PATH + entry + ".html"
        output_folder = OUTPUT_ROOT_PATH + entry
        if os.path.isfile(source_path) == False:
            print("Missing '" + source_path + "'.")
            continue

        if os.path.isdir(output_folder): shutil.rmtree(output_folder)
        if entry != "index": os.makedirs(output_folder)

        source_str = ""
        with open(source_path) as source_file:
            source_str_array = source_file.read().split("\n")
        c = 0
        for line in source_str_array:
            # Add indents on all lines except first
            if c == 0: source_str += line + "\n"
            else: source_str += INDENT + line + "\n"
            c += 1

        # Output
        source_str = source_str.rstrip("\n")
        output = TEMPLATE.replace("$CONTENT", source_str)
        output = output.replace("$TITLE", pages_data[entry]["title"])

        # Exception for the index file
        if entry == "index": output_path = "rats/index.html"
        else: output_path = output_folder + "/index.html"
        with open(output_path, "w") as output_file:
            output_file.write(output)
