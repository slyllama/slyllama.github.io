# makesly.py
# Generates journals and pages for Slyllama

JPATH = "journal/" # journal path
TITLE = "$ &mdash; Slyllama"
PROG_TITLE = "This is Slyllama CMS"
URL = "https://slyllama.net"
DESC = "Illustrative graphics for a modern age."
INDENT = "    "
VIEWER_PATTERN = r'src=\"[^\"]*\"'
VIEWER_ALT_PATTERN = r'alt=\"[^\"]*\"'

import json
import os
import re
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

with open("source/template.html") as file: # get template
    template = file.read()
indent = "" # used for pretty formatting of HTML
for line in template.split("\n"):
    if "$CONTENT" in line:
        indent = line.strip("$CONTENT")

# Identify clickable images using the $VIEWER identifier, extract the image source and use it to apply the function and styles
def add_viewers(data):
    t = data
    u = ""
    for line in t.split("\n"):
        if "$VIEWER" in line:
            src = re.search(VIEWER_PATTERN, line).group()
            src = src.rstrip("\"")
            src = src.replace("src=\"", "")

            alt = re.search(VIEWER_ALT_PATTERN, line).group()
            alt = alt.rstrip("\"")
            alt = alt.replace("alt=\"", "")

            new_line = line.replace("$VIEWER", "onclick=\"viewImg(\'" + src + "\', \'" + alt + "\');\" tabindex=\"-1\" style=\"cursor: zoom-in;\"")
            u += new_line
        else: u += line
        u += "\n"
    return(u)


def generate_page(name, data, custom_path = "!"):
    print(" * Generating page '" + name + "'...")
    cnt = ""
    if custom_path != "!":
        output_path = custom_path
    else:
        output_path = root_prefix + "/" + name
    with open("source/" + name + ".html") as file:
        cnt = file.read()
    fmt_cnt = indent_content(cnt)

    t = template
    t = t.replace("$CONTENT", fmt_cnt)
    t = t.replace("$ROOT", root_prefix)

    if custom_path != "!":
        t = t.replace("$PAGEROOT", root_prefix + output_path)
    else:
        t = t.replace("$PAGEROOT", output_path)

    u = add_viewers(t)
    
    for tag in data:
        u = u.replace(tag, data[tag])
    
    if custom_path != "!":
        with open(output_path + "index.html", "w") as file:
            file.write(u)
    else:
        if not Path(name).exists():
            os.makedirs(name)
        with open(name + "/index.html", "w") as file:
            file.write(u)

generate_page("home", {
    "$TITLE": "Slyllama",
    "$DESC": "Illustrative graphics for a modern age." 
}, "")

generate_page("dwelt", {
    "$TITLE": "Dwelt: Mechanical Dreams",
    "$DESC": "A dreamscape in video game form." 
}, "!")

with open("source/journal.json") as file: # get list of journal entries
    journal_list = json.load(file)

# Build master list
print(" * Building journal list...")
master_content = ""
master_content += "<h1><span>Design Journal</span></h1>"
master_content += "<div class='sep'></div>"

journal_list.reverse()

for entry in journal_list:
    if "status" in entry:
        if entry["status"] == "draft":
            continue
    
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
        if "status" in entry:
            if entry["status"] == "draft":
                content += ind(1) + "<p class=\"date draft-tag\">DRAFT</p>\n"
        else:
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
        e = add_viewers(e)

        with open(output_path + "/index.html", "w") as file:
            file.write(e)
    else:
        print(" ! No source file for '" + name + "'!")

print("Finished.")
