import sqlite3
import json
import re

def clean_hazards(hazards):
    """
    Cleans the hazards string by removing digits enclosed in square brackets.

    Args:
        hazards (str): The hazards string to clean.

    Returns:
        str: The cleaned hazards string.
    """
    return re.sub(r"\[[0-9]+\]", "", hazards)

def process_database(db_file, json_file):
    """
    Processes an SQLite database containing plant information and appends 
    entries to a JSON file with medicinal use disambiguation instructions.
    Handles comma-separated common names and spaces in names.

    Args:
        db_file (str): Path to the SQLite database file.
        json_file (str): Path to the JSON file to write to.
    """

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Create a cursor to iterate through plant entries
        cursor.execute("SELECT latin_name, common_name, known_hazards FROM plants")

        # Open the JSON file in write mode to overwrite existing content
        with open(json_file, "w") as f:
            for latin_name, common_name, known_hazards in cursor:
                if common_name and known_hazards:
                    for name in common_name.split(','):
                        name = name.strip()  # Remove leading/trailing spaces
                        instruction = f"What are the hazards of {name}?"
                        clean_hazards_str = clean_hazards(known_hazards)
                        output = f"The hazard data for {name}, {latin_name} are: {clean_hazards_str}"

                        # Append to the JSON file
                        f.write(json.dumps({"instruction": instruction, "output": output}) + "\n")

if __name__ == "__main__":
    db_file = "data.sqlite"  # Updated database file path
    json_file = "hazards.json"  # Updated JSON file path

    process_database(db_file, json_file)
