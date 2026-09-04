#!/usr/bin/env python3

#
# Apply clang-format to all <pre highlight="js"> blocks in index.bs
#

import os
import re
import subprocess

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../index.bs')

def clang_format(text):
    try:
        result = subprocess.run(
            ['clang-format', '--assume-filename=.js', '--style=file'],
            capture_output=True, text=True, encoding='utf-8', input=text.strip())
    except FileNotFoundError:
        raise SystemExit('clang-format not found; install it and try again.')

    # Bail out rather than silently replacing the block with empty output.
    if result.returncode != 0:
        raise SystemExit(f'clang-format failed: {result.stderr.strip()}')

    return result.stdout

def replace(content):
    # Reformat the JS content.
    replacement = clang_format(content);

    # Indent by 4 spaces.
    replacement = re.sub(r'^', '    ', replacement, flags=re.M)

    # Remove trailing whitespace.
    replacement = re.sub(r' +$', '', replacement, flags=re.M)

    # Indicate progress.
    print('.', end='', flush=True)

    return replacement + '\n'


# Slurp in the file.
f = open(filename, encoding='utf-8')
content = f.read()
f.close()

# Replace all of the JS blocks.
content = re.sub(r'(<pre highlight="js"> *\n)(.*?)( *</pre>)',
                 lambda m: m.group(1) + replace(m.group(2)) + m.group(3), content,
                 flags=re.DOTALL)

# Write the file back out.
f = open(filename, 'w', newline='\n', encoding='utf-8')
f.write(content)
f.close()


print('\n')
