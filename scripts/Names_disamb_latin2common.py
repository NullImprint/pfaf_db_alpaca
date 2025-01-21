import sqlite3
import json

def process_database(db_file, json_file):
    """
    Processes an SQLite database containing plant information and appends 
    entries to a JSON file with common name disambiguation instructions.
    Checks that the common_name field is not empty before generating JSON.

    Args:
        db_file (str): Path to the SQLite database file.
        json_file (str): Path to the JSON file to write to.
    """

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Create a cursor to iterate through plant entries
        cursor.execute("SELECT latin_name, common_name FROM plants")

        # Open the JSON file in append mode
        with open(json_file, "a") as f:
            for latin_name, common_name in cursor:
                if common_name:  # Check if common_name is not empty
                    instruction = f"What are the common names of {latin_name}?"
                    output = f"The common names of {latin_name} are: {common_name}."

                    # Append to the JSON file
                    f.write(json.dumps({"instruction": instruction, "output": output}) + "\n")

if __name__ == "__main__":
    db_file = "data.sqlite"  # Replace with the actual database file path
    json_file = "name_disamb.json"

    process_database(db_file, json_file)
