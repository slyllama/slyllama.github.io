import os

# Load the relevant files
struct_raw = open("struct.txt", "r")
frame_raw = open("frame.html", "r")
struct = []
frame = ""

# Put the frame into memory
for line in frame_raw:
	frame += line.rstrip("\n")

for line in struct_raw:
	source = ""

	# Put the structure array into memory
	struct = line.split(",")
	# If we can't find the file
	if os.path.isfile(struct[0]) == False:
		print("Couldn't open '" + struct[0] + "'!")
		struct_raw.close()
		quit()
	# Open the file if we can find it
	source_raw = open(struct[0], "r")
	for line in source_raw:
		source += line
	# Write the final string
	out_prep = frame.replace("$C", "\n" + source).replace("$T", struct[1])

	# Create an "out" file and write to it
	out = open(struct[0].split(".")[0] + ".html", "w")
	out.write(out_prep)

	# Close open files
	source_raw.close()
	out.close()
struct_raw.close()
