import json
import sys
from pathlib import Path
from src.validator import TariffValidator


def main():
    blacklist_path = Path("data/pesel_blacklist.csv")
    validator = TariffValidator(blacklist_path)
   
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    else:
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
    print(f"Request:  {result['requestId']}")

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)  # Creates 'output' directory if it doesn't exist

    output_file = output_dir / f"result_{json_path.stem}.json" # Creates output file path with the pattern: result_<original_filename>.json

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"💾 Zapisano wynik do pliku: {output_file}\n")


if __name__ == "__main__":
    main()