import os

ADLISTS = ["ads_malware", "fakenews", "gambling", "porn", "social"]
OUTPUT_DIR = "out"
OUTPUT_FILE = f"{OUTPUT_DIR}/hosts.txt"
PREFIX_TO_CHECK = "0.0.0.0"


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def check_line_starts_with(line, prefix):
    return line.startswith(prefix)

def integrity_message(fname):
    if os.path.exists(fname):
        print(f"Hosts file compiled sucessfully and available in {fname}")
    else:
        print(f"Hosts file couldn't be compiled: {fname}")


def selected_lists(input):
    lists = [item for item in input if item in ADLISTS]
    if not lists:
        lists = ADLISTS
    return lists

def filter_condition(line):
    return check_line_starts_with(line, PREFIX_TO_CHECK)

def main():
    input_lists = os.getenv("LISTS", ADLISTS).split(",")
    lists = selected_lists(input_lists)
    lists = list("lists/" + list + ".txt" for list in lists)

    for fname in lists:
        # Open the input file in read mode
        with open(fname, 'r') as file:
            lines = [line for line in file.readlines() if filter_condition(line)]

        # Use a set to keep track of unique lines
        unique_lines = set(lines)
        unique_lines = sorted(unique_lines)

        delete_file(fname)

        # Open the output file in write mode
        with open(fname, 'w') as file:
            # Write the unique lines back to the file
            file.writelines(unique_lines)

        integrity_message(fname)


if __name__ == "__main__":
    main()
