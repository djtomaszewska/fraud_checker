import json
import sys
from pathlib import Path
from src.validator import TariffValidator


def main():
    # Domyślna ścieżka do bazy
    blacklist_path = Path("data/pesel_blacklist.csv")
    validator = TariffValidator(blacklist_path)

    # Jeśli użytkownik podał plik jako argument w terminalu
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    else:
        # Fallback na domyślny plik demonstracyjny
        json_path = Path("data/request_clean.json")

    if not json_path.exists():
        print(f"❌ Błąd: Plik '{json_path}' nie istnieje.")
        sys.exit(1)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    result = validator.validate(data)

    print(f"\n--- Wynik walidacji dla: {json_path.name} ---")
    print(f"Status:   {result['decision']}")
    print(f"Powód:    {result['reason']}")
    print(f"Request:  {result['requestId']}\n")


if __name__ == "__main__":
    main()