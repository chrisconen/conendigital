import os

workspace_dir = r"g:\CONEN DIGITAL"
for root, dirs, files in os.walk(workspace_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if "600k" in content:
                    print(f"Found '600k' in {os.path.relpath(path, workspace_dir)}")
            except Exception as e:
                print(f"Error {file}: {e}")
