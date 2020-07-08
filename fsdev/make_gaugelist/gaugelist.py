src = open("import.txt", "r")
src_read = src.readlines()
for line in src_read:
	ls = line.strip("\n").split(",")
	# [0]: file name
	# [1]: gauge type
	# [2]: X-dimension
	# [3]: Y-dimension
	# [4]: gauge component
	print("<li><code>"+ ls[0]+"</code> &ndash; "+ls[1]+" ("+ls[2]+" &times; "+ls[3]+"): "+ls[4]+".</li>")

src.close()
