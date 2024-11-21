import os
import string

ROOT = "file:///D:/Repos/slyllama.github.io/wam/html/"
#ROOT = "https://slyllama.net/wam/html/"


def fmt_name(name):
    return(string.capwords(name.replace("-", " ")).replace("Ss", "SS"))

def get_product_data(path):
    proper_path = "src/" + path + ".txt"
    if os.path.exists(proper_path) == False:
        print("Error: no data at '" + path + "'!")
        return(-1)
    
    file = open(proper_path, "r")
    data_str = file.readlines()
    file.close()

    return(data_str)

def make_table(csv):
    table = "<table border=1>"
    linec = 0

    for l in csv.split("\n"):
        table += "<tr>"
        if linec == 0:
            for i in l.split(","):
                table += "<th>" + i + "</th>"
        else:
            for i in l.split(","):
                table += "<td>" + i + "</td>"

        linec += 1
        table += "</tr>"
    
    table += "</table>"
    return(table)

def make_html(path):
    html = ""
    data = serialise_product(path)

    if data == -1:
        return(-1)
    
    if os.path.exists("html/" + data["category"]) == False:
        os.mkdir("html/" + data["category"])
    
    # HTML additions
    html = "<!DOCTYPE html>\n<html>\n<head>"
    html += "\n<link rel='stylesheet' type='text/css' href='" + ROOT + "reset.css'/>"
    html += "\n<link rel='stylesheet' type='text/css' href='" + ROOT + "style.css'/>"
    html += "\n</head>"
    html += "\n<body id='body-iframe'>"
    html += "\n<div class='product-info-wrapper'>"
    html += "<div class='product-info'>"
    html += "\n<h1>" + data["name"] + "</h1>"
    if "description" in data:
        html += "\n" + data["description"]
    if "data" in data:
        html += "\n" + make_table(data["data"])
    
    html += "\n</div>"
    html += "\n<div class='product-image'>"
    if "custom-image-link" in data:
        html += "<img src='" + data["custom-image-link"] + "'/>"
    else:
        html += "<img src='img/" + data["id"] + ".jpg'/>"
    html += "</div>"
    html += "\n</div>"
    html += "\n<script>"
    html += "function postHeight() { parent.postMessage(document.querySelector('body').clientHeight, '*'); }"
    html += "postHeight(); addEventListener('resize', (event) => { postHeight(); });"
    html += "</script>"
    html += "\n</body>\n</html>"

    html_path = "html/" + path + ".html"
    html_file = open(html_path, "w")
    html_file.write(html)
    html_file.close()

def serialise_product(path):
    current_ident = ""
    current_value = ""
    data = {}

    data["category"] = path.split("/")[0]
    data["id"] = path.split("/")[1]
    
    # Check whether the specified product exists
    data_str = get_product_data(path)
    if data_str == -1:
        return(-1)
    
    for l in data_str:
        l_words = l.split(" ")
        if l[0] == "#":
            current_ident = l_words[0][1:].replace("\n", "")
            data[current_ident] = ""
            current_value = "" # new identifier - reset
            
            for w in range(1, len(l_words)):
                current_value += l_words[w] + " "
            current_value = current_value.rstrip(" ")
            data[current_ident] += current_value
        else: data[current_ident] += l.replace("    ", "\t")
    
    for i in data: data[i] = data[i].rstrip("\n")
    return(data)

for folder in next(os.walk("src"))[1]:
    for f in os.listdir("src/" + folder):
        fname = folder + "/" + f.replace(".txt", "")
        print("Making " + str(fname) + "...")
        make_html(fname)

def generate_page(name, products):
    html = "<!DOCTYPE html>\n<html>\n<head>"
    html += "\n<link rel='stylesheet' type='text/css' href='" + ROOT + "reset.css'/>"
    html += "\n<link rel='stylesheet' type='text/css' href='" + ROOT + "style.css'/>"
    html += "\n<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    html += "\n</head>"
    html += "\n<body id='body-iframe'>"
    html += "<h1>" + fmt_name(name) + "</h1>"
    html += "<div class='category-grid'>"
    for i in products:
        p = serialise_product(i)

        html += "\n<div id='category-grid' class='category-card'>"
        img_path = i.split("/")[0] + "/img/" + i.split("/")[1] + ".jpg"  
        url = ROOT + "product.html?" + i
        html += "<a target='_top' href='" + url + "'><img src='" + img_path + "'/></a>"
        html += "<a target='_top' href='" + url + "'><h3>" + fmt_name(i.split("/")[1]) + "</h3></a>"
        if p != -1:
            if "subtitle" in p:
                html += "<p class='subtitle'>" + p["subtitle"] + "</p>"
        else:
            html += "<p class='subtitle' style='color: red;'>No product data!</p>"
        html += "</div>"
    html += "</div>"
    html += "\n<script>"
    html += "function postHeight() { parent.postMessage(document.querySelector('body').clientHeight, '*'); }"
    html += "postHeight(); addEventListener('resize', (event) => { postHeight(); });"
    html += "</script>"
    html += "\n</body></html>"
    file = open("html/" + name + ".html", "w")
    file.write(html)
    file.close()

generate_page("tank-truck", [
    "tank-truck/safety-valve",
    "tank-truck/lever-gate-valve-with-flange",
    "tank-truck/rubber-funnel-with-locking-clamp",
    "tank-truck/rubber-joint",
    "tank-truck/safety-valve-with-hose-connector",
    "tank-truck/depression-valve",
    "tank-truck/curved-siphon-valve",
    "tank-truck/glass-level-indicator",
    "tank-truck/porthole-level-indicator",
    "tank-truck/inspection-glass-replacement",
    "tank-truck/tube-level-indicator",
    "tank-truck/lever-gate-valve",
    "tank-truck/flanged-ball-valve",
    "tank-truck/three-way-flanged-cock-valve",
    "tank-truck/flanged-cock-valve",
    "tank-truck/cast-iron-gate-valve-with-ss-knife",
    "tank-truck/ss-knife-gate-valve",
    "tank-truck/adjustable-spray-gun",
    "tank-truck/spray-gun-with-sprinkle-guard",
    "tank-truck/spray-gun-with-long-sprinkle-guard"
])
