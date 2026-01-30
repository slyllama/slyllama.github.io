import json
import os

mf_file = open("manifest.json", "r")
mf = json.loads(mf_file.read())
mf_file.close()

tmp_file = open("template.html", "r")
tmp = tmp_file.read()
tmp_file.close()

for page in mf:
    fmt = tmp
    src_path = "src/" + page["name"] + ".html"
    if os.path.isfile(src_path):
        src_file = open(src_path, "r")
        src = src_file.read()
        src_file.close()
        src = "\t\t\t" + src.replace("\n", "\n\t\t\t").rstrip("\n\t\t\t")

        # Substitutions
        fmt = fmt.replace("$C", src)
        fmt = fmt.replace("$T", page["title"])

        out_file = open(page["name"] + ".html", "w")
        out_file.write(fmt)
        out_file.close()
