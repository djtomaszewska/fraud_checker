import sys
import csv
from pathlib import Path

def get_resource_path(relative_path: str) -> Path:
    """
    Get the absolute path to a resource, works for development and for PyInstaller
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(relative_path)

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