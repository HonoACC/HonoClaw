#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) < 2:
    print('Usage: normalize-latest-mac-yml.py <path>')
    sys.exit(1)

file = Path(sys.argv[1])
if not file.exists():
    print(f'No latest-mac.yml found at {file}, skipping normalization')
    sys.exit(0)

lines = file.read_text().splitlines()
start = next((i for i, line in enumerate(lines) if line.strip() == 'files:'), None)
if start is None:
    print('latest-mac.yml has no files section, skipping normalization')
    sys.exit(0)

end = len(lines)
for i in range(start + 1, len(lines)):
    if lines[i] and not lines[i].startswith(' '):
        end = i
        break

blocks = []
i = start + 1
while i < end:
    line = lines[i]
    if line.startswith('  - url: '):
        block = [line]
        i += 1
        while i < end and (lines[i].startswith('    ') or lines[i].strip() == ''):
            block.append(lines[i])
            i += 1
        blocks.append(block)
    else:
        i += 1

seen = set()
deduped = []
removed = []
for block in blocks:
    url = block[0].split(': ', 1)[1].strip()
    if url in seen:
        removed.append(url)
        continue
    seen.add(url)
    deduped.append(block)

new_lines = lines[: start + 1]
for block in deduped:
    new_lines.extend(block)
new_lines.extend(lines[end:])
file.write_text('\n'.join(new_lines) + '\n')
print(f'Normalized {file}: kept {len(deduped)} file entries, removed {len(removed)} duplicates')
if removed:
    print('Removed duplicates: ' + ', '.join(removed))
