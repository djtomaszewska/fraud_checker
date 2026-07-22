# 🛡️ Fraud Checker - PESEL Tariff Validator

![Tests Status](https://github.com/<TWOJ_NICK>/fraud_checker/actions/workflows/test.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

Lekki silnik walidacji wniosków taryfikacyjnych pod kątem wykrywania nadużyć (Fraud Detection). System weryfikuje poprawność danych PESEL w zagnieżdżonych strukturach JSON oraz sprawdza obecność wnioskodawców na wewnętrznych czarnych listach (CSV).

---

## 🚀 Architektura i Przepływ Walidacji

Walidator działa w oparciu o sekwencyjny potok walidacji (early return pattern):

1. **Extract PESEL (`extract_pesel`)** – Bezpieczne wyciąganie numeru PESEL z zagnieżdżonej struktury JSON (`envelope -> applications[0] -> policies[0] -> personInfo`). Odporne na brakujące klucze, puste listy czy `null`.
2. **PESEL Validation (`is_valid_pesel`)** – Weryfikacja formatu (11 cyfr) oraz matematycznej cyfry kontrolnej z wykorzystaniem algorytmu wagowego `[1, 3, 7, 9, 1, 3, 7, 9, 1, 3]`.
3. **Blacklist Check (`TariffValidator`)** – Weryfikacja obecności PESEL-u w bazie zastrzeżonych numerów (`data/pesel_blacklist.csv`) wraz z pobraniem konkretnego powodu odrzucenia.

---

## 🛠️ Wymagania i Instalacja

* Python 3.10+
* `pytest` oraz `pytest-cov` (do uruchamiania testów)

### Instalacja środowiska:


# Klonowanie repozytorium
git clone [https://github.com/](https://github.com/)djtomaszewska/fraud_checker.git
cd fraud_checker

# Tworzenie i aktywacja venv (Windows)
python -m venv .venv
.venv\Scripts\activate

# Instalacja zależności testowych
'pip install pytest pytest-cov'

### Aplikacja posiada testy jednostkowe:
# Uruchomienie testów:
'python -m pytest -v'

# Generowanie raportu pokrycia kodu (Coverage):
'python -m pytest --cov=src --cov-report=term-missing'

# Struktura projektu:

fraud_checker/
├── .github/
│   └── workflows/
│       └── test.yml         # CI/CD GitHub Actions
├── data/
│   ├── pesel_blacklist.csv  # Baza zastrzeżonych numerów PESEL
│   └── request_*.json       # Pliki ze scenariuszami testowymi
├── src/
│   ├── data_loader.py       # Wczytywanie plików CSV
│   ├── utils.py             # Wyciąganie danych i walidacja algorytmu PESEL
│   └── validator.py         # Główna klasa walidatora (TariffValidator)
├── tests/
│   ├── test_data_loader.py  # Testy jednostkowe modułu loaderów
│   ├── test_utils.py        # Testy jednostkowe walidacji PESEL (parametryzowane)
│   └── test_validator.py    # Testy integracyjne walidatora na JSON-ach
├── pyproject.toml           # Konfiguracja ścieżek dla pytest
├── main.py
├── requirements.txt
└── README.md