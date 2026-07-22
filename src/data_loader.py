import csv
from pathlib import Path

def load_csv_file(file_path: str | Path) -> dict[str, str]:
    """
    Load a CSV file and return as a dictionary mapping PESEL to reason
    """
    
    file_path = Path(file_path)
    
    if not file_path.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku bazy PESEL: {file_path}")

    with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return {row["pesel"].strip(): row["reason"].strip() for row in reader}

#pesel_dict = load_csv_file("data/pesel_blacklist.csv")