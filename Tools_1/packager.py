import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(BASE_DIR, 'logic.py')
DEST_DIR = os.path.join(BASE_DIR, 'Quantix')
DEST_FILE = os.path.join(DEST_DIR, 'logic.py')
KEY = 42

# Ensure the destination folder exists
os.makedirs(DEST_DIR, exist_ok=True)

# Read the file
with open(SOURCE_FILE, 'r') as f:
    real_code = f.read()

# Scramble
scrambled = "".join([chr(ord(c) ^ KEY) for c in real_code])

# Write to the destination
with open(DEST_FILE, 'w') as f:
    f.write('# GitHub-Ready Logic\n')
    f.write(f'key = {KEY}\n')
    f.write(f'code = {repr(scrambled)}\n')
    f.write('exec("".join([chr(ord(c) ^ key) for c in code]), globals())\n')

print(f"Success: logic.py deployed to {DEST_FILE}")