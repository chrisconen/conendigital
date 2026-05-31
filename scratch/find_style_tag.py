import re
import os

workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

style_starts = []
style_ends = []

for i, line in enumerate(lines, 1):
    if "<style>" in line:
        style_starts.append(i)
    if "</style>" in line:
        style_ends.append(i)

print("Style starts at lines:", style_starts)
print("Style ends at lines:", style_ends)
