# 🚀 Strategia Wdrażania i Utrzymania (Deployment Guide)

Dokumentacja określająca zasady wydań, strategię gałęzi oraz proces wdrażania aplikacji **Fraud Checker** na środowiska testowe (**PREP / Staging**) oraz produkcyjne (**PROD**).

---

## 🌴 1. Strategia Gałęzi i Wersjonowanie (GitFlow & SemVer)

Stosujemy uproszczony model **GitFlow** powiązany ze spójnym wersjonowaniem semantycznym (**Semantic Versioning - SemVer**: `MAJOR.MINOR.PATCH`):

* **`feature/*`** – Gałęzie programistyczne. Zmiany są scalane do `develop` poprzez Pull Request (PR) po przejściu testów jednostkowych.
* **`develop`** – Główna gałąź integracyjna. Każdy commit automatycznie uruchamia wdrożenie na środowisko **PREP**.
* **`main`** – Gałąź produkcyjna. Zawiera wyłącznie stabilny, przetestowany kod. Wdrożenie na **PROD** odbywa się poprzez odcięcie taga wersji (np. `v1.0.0`).

---

## ⚙️ 2. Środowisko PREP (Staging / Testowe)

Środowisko **PREP** służy do weryfikacji integracyjnej oraz testów automatycznych E2E / regression testing.

### Proces wdrażania na PREP:
1. **Automatyczny Trigger:** Merge PR do gałęzi `develop`.
2. **Bramka Jakości (CI Pipeline):**
   * Uruchomienie statycznej analizy kodu (Linter / Flake8).
   * Wykonanie pełnej paczki testów `pytest` z wymogiem **100% Code Coverage**.
3. **Budowanie Artefaktu:**
   * Wygenerowanie nowej wersji binarki `.exe` (dla użytkowników Windows) lub zbudowanie obrazu Dockerowego (`fraud-checker:prep-latest`).
4. **Deploy:** Automatyczne nadpisanie zasobów na serwerze testowym.
5. **Post-deploy:** Wykonanie automatycznych testów akceptacyjnych na przykładowych wnioskach JSON (`sample_clean_woman.json`, `sample_blacklisted_man.json`).

---

## 🟢 3. Środowisko PROD (Produkcja)

Środowisko **PROD** wymaga pełnego bezpieczeństwa, ciągłości działania (*high availability*) oraz braku przestojów (*zero-downtime deployment*).

### Proces wdrażania na PROD:
1. **Akceptacja i Tagowanie:** 
   * Utworzenie Pull Requesta z `develop` do `main`.
   * Wymagany Code Review (przynajmniej 1 akceptacja Senior Developera / QA Leada).
   * Po scaleniu następuje nadanie taga release'u na `main` (np. `git tag v1.0.0`).
2. **Budowanie Wersji Produkcyjnej:**
   * GitHub Actions buduje oficjalne wydanie (Release).
   * Automatyczne dołączenie wygenerowanej binarki `.exe` do sekcji **Assets** w GitHub Releases.
3. **Wdrożenie Kontenerowe / Aplikacyjne:**
   * **Strategia Blue-Green Deployment:** Nowy kontener z aplikacją odpala się obok starego. Po potwierdzeniu `healthcheck` ruch jest przełączany na nową wersję.
4. **Weryfikacja produkcyjna (Smoke Tests):**
   * Wykonanie pojedynczej, bezpiecznej walidacji próbnej na produkcji celem weryfikacji dostępności bazy czarnej listy.

---

## 🔄 4. Plan Awaryjny (Rollback Strategy)

W przypadku wykrycia błędów krytycznych na środowisku produkcyjnym:

1. **Wersja Kontenerowa (Docker / Kubernetes):**
   * Natychmiastowe przywrócenie ruchu do poprzedniego taga obrazu (np. z `v1.0.1` do `v1.0.0`) za pomocą komendy `helm rollback` / podmiany taga w konfiguracji infra.
2. **Wersja Binarna CLI (.exe):**
   * Oznaczenie feralnego release'u na GitHubie jako **Pre-release / Deprecated**.
   * Wskazanie użytkownikom jako zalecanej poprzedniej stabilnej wersji z zakładki Releases.

---

## 📊 5. Monitoring i Logi

* **Audit Log:** Każde wywołanie walidacji zapisuje wynik do pliku JSON w folderze `output/` z zachowaniem Unikalnego ID Requestu (`requestId`).
* **Alertowanie:** Błędy odczytu bazy czarnej listy (`FileNotFoundError`, błędy uprawnień I/O) generują błąd krytyczny i natychmiastowe powiadomienie na kanale alertowym (np. Slack / Microsoft Teams).