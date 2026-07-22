import json
from pathlib import Path
import pytest

from src.validator import TariffValidator


DATA_DIR = Path(__file__).parent.parent / "data"


@pytest.fixture
def validator():
    """Fixture initializing TariffValidator with test CSV data."""
    csv_path = DATA_DIR / "pesel_blacklist.csv"
    return TariffValidator(csv_path)


def load_json_fixture(filename: str) -> dict:
    """Helper function to load a JSON file from test data directory."""
    file_path = DATA_DIR / filename
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

def test_validation_accepts_clean_request(validator):
    """Clean request with valid non-blacklisted PESEL should return ACCEPT."""
    data = load_json_fixture("request_clean.json")
    result = validator.validate(data)

    assert result["decision"] == "ACCEPT"
    assert "Weryfikacja pozytywna" in result["reason"]
    assert result["requestId"] == "req-clean-0001"


def test_validation_rejects_blacklisted_pesel(validator):
    """Blacklisted PESEL should return REJECT with specific reason from CSV."""
    data = load_json_fixture("request_blacklisted.json")
    result = validator.validate(data)

    assert result["decision"] == "REJECT"
    assert "czarnej liście" in result["reason"]
    assert "Podejrzenie współudziału w oszustwie" in result["reason"]


def test_validation_rejects_invalid_pesel_checksum(validator):
    """PESEL with invalid checksum digit should return REJECT."""
    data = load_json_fixture("request_invalid_pesel.json")
    result = validator.validate(data)

    assert result["decision"] == "REJECT"
    assert "Nieprawidłowy numer PESEL" in result["reason"]


def test_validation_rejects_missing_pesel(validator):
    """Request with null PESEL should return REJECT."""
    data = load_json_fixture("request_missing_pesel.json")
    result = validator.validate(data)

    assert result["decision"] == "REJECT"
    assert "Brak numeru PESEL" in result["reason"]


def test_validation_rejects_invalid_json_structure(validator):
    """Request missing applications array should safely return REJECT without throwing exception."""
    data = load_json_fixture("request_invalid_structure.json")
    result = validator.validate(data)

    assert result["decision"] == "REJECT"
    assert result["requestId"] == "req-invalid-0004"