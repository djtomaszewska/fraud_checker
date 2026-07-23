import json
import sys
from pathlib import Path
from src.validator import TariffValidator
from src.data_loader import get_resource_path


def main():
    blacklist_path = get_resource_path("data/pesel_blacklist.csv")
    validator = TariffValidator(blacklist_path)
    
    if not blacklist_path.exists():
        print(f"❌ Błąd krytyczny: Brak bazy danych PESEL pod adresem: '{blacklist_path}'")
        sys.exit(1)
   
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    else:
        json_path = Path("data/request_clean.json")

    if not json_path.exists():
        print(f"❌ Błąd: Plik '{json_path}' nie istnieje.")
        sys.exit(1)
    
    if json_path.is_dir():
        print(f"❌ Błąd: Podana ścieżka '{json_path}' jest katalogiem, a nie plikiem JSON!")
        sys.exit(1)
    
    if json_path.suffix.lower() != ".json":
        print(f"❌ Błąd: Plik '{json_path.name}' nie jest plikiem .json! (Wykryto rozszerzenie: '{json_path.suffix}')")
        sys.exit(1)

    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Błąd: Plik '{json_path.name}' zawiera niepoprawny format JSON (błąd składni).")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Błąd odczytu pliku '{json_path.name}': {e}")
        sys.exit(1)

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