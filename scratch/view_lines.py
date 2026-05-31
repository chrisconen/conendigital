with open(r"g:\CONEN DIGITAL\weboldal-keszites-budapest.html", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i in range(1045, 1075):
    if i < len(lines):
        print(f"Line {i+1}: {repr(lines[i])}")
