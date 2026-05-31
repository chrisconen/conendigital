with open(r"g:\CONEN DIGITAL\weboldal-keszites-budapest.html", "r", encoding="utf-8") as f:
    content = f.read()

print("Length of budapest.html:", len(content))
print("Occurrences of '600k':", content.count("600k"))
print("Occurrences of '1.5M':", content.count("1.5M"))
print("Occurrences of '450k':", content.count("450k"))
print("Occurrences of '1.2M':", content.count("1.2M"))
print("Occurrences of '250k':", content.count("250k"))
print("Occurrences of 'Ft':", content.count("Ft"))
