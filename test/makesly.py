# makesly.py
# Generates journals and pages for Slyllama

JPATH = "journal/" # journal path
TITLE = "$ &mdash; Slyllama"
PROG_TITLE = "This is Slyllama CMS"
URL = "https://slyllama.net/test"
DESC = "Illustrative graphics for a modern age."
INDENT = "    "

import json
import os
import shutil
import sys
from pathlib import Path

def print_usage_and_quit():
    print("Usage:")
    print(" -local   use local path (usually for testing).")
    print(" -live    use live URLs.")
    quit()

def ind(c): # generate indent of size `c`
    indent = ""
    for _ in range(c):
        indent += INDENT
    return(indent)

def indent_content(c):
    indented_content = ""
    i = 0
    for line in c.split("\n"):
        if i > 0: indented_content += indent + line
        else: indented_content += line
        indented_content += "\n"
        i += 1
    indented_content = indented_content.rstrip("\n")
    return(indented_content)

# Process local/live arguments and display program messages
if len(sys.argv) != 2:
    print(PROG_TITLE + ".")
    print_usage_and_quit()
if sys.argv[1] == "-local":
    print(PROG_TITLE + " (working locally).")
    root_prefix = "file:///" + os.path.abspath(".").replace("\\", "/")
elif sys.argv[1] == "-live":
    print(PROG_TITLE + " (working live).")
    root_prefix = URL
else:
    print(PROG_TITLE + ".")
    print_usage_and_quit()

# Generate scripts with proper paths
print(" * Generating pathed scripts...")
with open("source/scripts.js") as file:
    scripts = file.read()
scripts = scripts.replace("$ROOT", root_prefix)
with open("scripts.js", "w") as file:
    file.write(scripts)

with open("source/template.html") as file: # get template
    template = file.read()
indent = "" # used for pretty formatting of HTML
for line in template.split("\n"):
    if "$CONTENT" in line:
        indent = line.strip("$CONTENT")

# Format home page
print(" * Generating home page...")
home_content = ""
with open("source/home.html") as file:
    home_content = file.read()
fmt_home_content = indent_content(home_content)

hem = template
hem = hem.replace("$CONTENT", fmt_home_content)
hem = hem.replace("$ROOT", root_prefix)
hem = hem.replace("$TITLE", "Slyllama")
hem = hem.replace("$PAGEROOT", root_prefix)
hem = hem.replace("$DESC", "Illustrative graphics for a modern age.")

with open("index.html", "w") as file:
    file.write(hem)
with open("source/journal.json") as file: # get list of journal entries
    journal_list = json.load(file)

# Build master list
print(" * Building journal list...")
master_content = ""
master_content += "<h1><span>Design Journal</span></h1>"

for entry in journal_list:
    name = entry["name"]
    entry_path = Path(JPATH + name + "/source.html")
    page_root = root_prefix + "/" + JPATH + name
    if not entry_path.exists():
        continue
    
    master_content += "<a href=\"" + page_root + "\">\n"
    master_content += ind(1) + "<p class=\"date\">" + entry["date"] + "</p>\n"
    master_content += "</a>"
    master_content += "<h2 class=\"journal-list-title\">\n"
    master_content += ind(1) + "<a href=\"" + page_root + "\">" + entry["title"] + "</a>\n"
    master_content += "</h2>\n"
    master_content += "<p>" + entry["desc"] + "</p>\n"
    master_content += "<div class=\"journal-list-pad\"></div>"

fmt_master_content = indent_content(master_content)
em = template
em = em.replace("$CONTENT", fmt_master_content)
em = em.replace("$ROOT", root_prefix)
em = em.replace("$PAGEROOT", root_prefix + "/journal")
em = em.replace("$DESC", "A casual collection of writing on design and illustration!")
em = em.replace("$TITLE", TITLE.replace("$", "Design Journal"))

with open(JPATH + "index.html", "w") as file:
    file.write(em)
    pass

# Process each individual journal entry
for entry in journal_list:
    name = entry["name"]
    entry_path = Path(JPATH + name + "/source.html")
    page_root = root_prefix + "/" + JPATH + name
    
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
        
        # Add indentation to match template file
        fmt_content = indent_content(content)

        # Content substitutions
        e = e.replace("$CONTENT", fmt_content)
        e = e.replace("$ROOT", root_prefix)
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
