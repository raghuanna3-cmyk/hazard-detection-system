import os
import re
from datetime import datetime

def extract_times_from_log(file_path):
    start_time = None
    end_time = None
    time_pattern = r"\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [AP]M"

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        match = re.search(time_pattern, line)
        if match:
            timestamp = match.group()
            if not start_time:
                start_time = timestamp
            end_time = timestamp  # last matched timestamp becomes end_time

    return start_time, end_time

def process_logs(directory):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            filepath = os.path.join(directory, filename)
            start, end = extract_times_from_log(filepath)
            results.append((filename, start, end))
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract start and end times from log files.")
    parser.add_argument("log_dir", help="Directory containing log files")
    args = parser.parse_args()

    summary = process_logs(args.log_dir)
    print(f"{'Filename':<50} {'Start Time':<25} {'End Time':<25}")
    print("-" * 100)
    for filename, start, end in summary:
        print(f"{filename:<50} {start:<25} {end:<25}")

if __name__ == "__main__":
    main()