import sqlite3
import json
import os

def process_database(db_file, json_file):
    """
    Processes an SQLite database containing plant information and appends 
    entries to a JSON file with common name disambiguation instructions.
    Checks that the common_name and hardiness fields are not empty before 
    generating JSON. Handles comma-separated common names. Excludes entries 
    with hardiness "0-0".

    Args:
        db_file (str): Path to the SQLite database file.
        json_file (str): Path to the JSON file to write to.
    """

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Create a cursor to iterate through plant entries
        cursor.execute("SELECT latin_name, common_name, hardiness FROM plants")

        # Open the JSON file in append mode
        with open(json_file, "w") as f:  # Open in write mode to overwrite existing content
            for latin_name, common_name, hardiness in cursor:
                if common_name and hardiness and hardiness != "0-0":
                    for name in common_name.split(','):
                        name = name.strip()  # Remove leading/trailing spaces
                        instruction = f"What is the hardiness of {name}?"
                        if hardiness == "0-0":
                            output = f"I'm not certain of the USDA hardiness range of {name}"
                        else:
                            output = f"The USDA hardiness range of {name} is: {hardiness}"

                        # Append to the JSON file
                        f.write(json.dumps({"instruction": instruction, "output": output}) + "\n")

    # Open the JSON file in read mode
    with open(json_file, "r") as f:
        lines = f.readlines()

    # Remove lines containing ": -"
    filtered_lines = [line for line in lines if ": -" not in line]

    # Overwrite the JSON file with filtered lines
    with open(json_file, "w") as f:
        f.writelines(filtered_lines)

if __name__ == "__main__":
    db_file = "data.sqlite"  # Replace with the actual database file path
    json_file = "name_disamb.json"

    process_database(db_file, json_file)
