# makesly.py
# Generates journals and pages for Slyllama

JPATH = "journal/" # journal path
#LOCAL_ROOT = "file://C:/Users/alaing/Desktop/web" # debug
LOCAL_ROOT = "https://slyllama.net/test"
TITLE = "$ &ndash; Slyllama"
DESC = "Illustrative graphics for a modern age."
INDENT = "    "

import json
import os
import shutil
from pathlib import Path

def ind(c): # generate indent of size `c`
    indent = ""
    for _ in range(c):
        indent += INDENT
    return(indent)

print("This is Slyllama CMS.")

# Generate scripts with proper paths
print(" * Generating pathed scripts...")
with open("scripts-source.js") as file:
    scripts = file.read()
scripts = scripts.replace("$ROOT", LOCAL_ROOT)
with open("scripts.js", "w") as file:
    file.write(scripts)

with open("template.html") as file: # get template
    template = file.read()

with open("journal.json") as file: # get list of journal entries
    journal_list = json.load(file)

for entry in journal_list:
    name = entry["name"]
    entry_path = Path(JPATH + name + "/source.html")
    page_root = LOCAL_ROOT + "/" + JPATH + name
    
    if entry_path.exists():
        print(" * Creating entry for '" + name + "'...")
        output_path = JPATH + name
        e = template

        # Format content header
        content = ""
        content += "<a href=\"" + page_root + "\">\n"
        content += ind(1) + "<p class=\"date\">" + entry["date"] + "</p>\n"
        content += "</a>"
        content += "<h2>"+ entry["title"] + "</h2>\n"

        with open(output_path + "/source.html") as file:
            content += file.read()

        indent = ""
        for line in e.split("\n"):
            if "$CONTENT" in line:
                indent = line.strip("$CONTENT")
        
        # Add indentation to match template file
        indented_content = ""
        i = 0
        for line in content.split("\n"):
            if i > 0: indented_content += indent + line
            else: indented_content += line
            indented_content += "\n"
            i += 1
        indented_content = indented_content.rstrip("\n")

        # Content substitutions
        e = e.replace("$CONTENT", indented_content)
        e = e.replace("$ROOT", LOCAL_ROOT)
        e = e.replace("$PAGEROOT", page_root)
        e = e.replace("$TITLE", TITLE.replace("$", entry["title"]))
        if "desc" in entry:
            e = e.replace("$DESC", entry["desc"])
        else:
            e = e.replace("$DESC", DESC)

        with open(output_path + "/index.html", "w") as file:
            file.write(e)
    else:
        print(" ! No source file for '" + name + "'!")

print("Finished.")
