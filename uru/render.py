import json
import os.path
import re

def convert_emoji(text: str) -> str:
    return re.sub(
        r"\$EM=([\w-]+)",
        r'<img class="emoji" src="/uru/emoji/\1.png" />',
        text)

INDENT = "                    "
LIVE = "https://slyllama.net"
URL = LIVE + "/uru/"

# File and folder paths
INDEX_FILE_PATH = "index.json"
SOURCE_PATH = "source/"
TEMPLATE_FILE_PATH = "_template.html"

# Get indexing data
index_file = open(INDEX_FILE_PATH, "r")
index_json = json.load(index_file)
index_file.close()

# Load template
template_file = open(TEMPLATE_FILE_PATH, "r")
template = template_file.read()
template_file.close()

for entry in index_json:
    file_name = entry + ".html"
    source_file_path = SOURCE_PATH + file_name
    if os.path.isfile(source_file_path) != True:
        continue

    # Data and URL links
    data = index_json[entry]
    url = URL + file_name

    # Read source file
    print(" * " + source_file_path)
    source_file = open(source_file_path, "r")
    source = source_file.read()
    source = source.rstrip("\n")
    source_file.close()

    # Indent source file
    source_indented = ""
    c = 0
    for line in source.split("\n"):
        if c > 0: source_indented += INDENT
        source_indented += line + "\n"
        c += 1
    source_indented = source_indented.rstrip("\n")
    source_indented = convert_emoji(source_indented)

    # Compose the output file
    output = template
    output = output.replace("$TITLE", data["title"])
    output = output.replace("$DESC", data["desc"])
    output = output.replace("$DATE", data["date"])
    output = output.replace("$URL", url)
    output = output.replace("$LIVE", LIVE)
    output = output.replace("$CONTENT", source_indented)

    # Write the output file
    output_file = open(file_name, "w")
    output_file.write(output)
    output_file.close()
