import sqlite3
import json

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
        cursor.execute("SELECT latin_name, common_name, medicinal_uses FROM plants")

        # Open the JSON file in write mode to overwrite existing content
        with open(json_file, "w") as f:
            for latin_name, common_name, medicinal_uses in cursor:
                if common_name and medicinal_uses:
                    for name in common_name.split(','):
                        name = name.strip()  # Remove leading/trailing spaces
                        instruction = f"What are the medicinal uses of {name}?"
                        output = f"The medicinal uses of {name}, {latin_name}, are: {medicinal_uses}"

                        # Append to the JSON file
                        f.write(json.dumps({"instruction": instruction, "output": output}) + "\n")

if __name__ == "__main__":
    db_file = "data.sqlite"  # Updated database file path
    json_file = "medici.json"  # Updated JSON file path

    process_database(db_file, json_file)
