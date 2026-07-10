#!/usr/bin/env python3
"""Fix H2 class inconsistency in student story articles."""

import glob
import re

PATTERN = r'<h2 class="text-xl font-bold text-gray-900 mt-6 mb-3">'
REPLACEMENT = '<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">'

files = glob.glob("articles/student-story-*.html")
count = 0

for filepath in sorted(files):
    with open(filepath, "r") as f:
        content = f.read()

    new_content = content.replace(PATTERN, REPLACEMENT)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        count += 1
        print(f"Fixed: {filepath}")

print(f"\nTotal files updated: {count}")