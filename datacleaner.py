#!/usr/bin/env python3
import argparse
import csv
import json
import sys
import os
VERSION = "1.0.0"

def clean_csv(input_file, output_file=None, remove_empty=True, trim_whitespace=True):
    cleaned_rows = []
    with open(input_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if remove_empty and not any(row.values()):
                continue
            if trim_whitespace:
                row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            cleaned_rows.append(row)
    if output_file:
        ext = os.path.splitext(output_file)[1]
        if ext == '.json':
            with open(output_file, 'w') as f:
                json.dump(cleaned_rows, f, indent=2)
        else:
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cleaned_rows)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    return len(cleaned_rows)

def main():
    try:
    parser = argparse.ArgumentParser(description='Data Cleaner')
    parser.add_argument('input')
    parser.add_argument('-o', '--output')
    parser.add_argument('--keep-empty', action='store_true')
    args = parser.parse_args()
    count = clean_csv(args.input, args.output, remove_empty=not args.keep_empty)
    print(f"Cleaned {count} rows", file=sys.stderr)
if __name__ == '__main__':
    main()
