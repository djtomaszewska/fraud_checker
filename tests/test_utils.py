import pytest
from src.utils import extract_pesel, is_valid_pesel


@pytest.mark.parametrize(
    "pesel_input, expected_valid",
    [
        ("90110544556", True),  # Correct checksum & format
        ("95010112344", True),  # Correct checksum & format
        ("95010112349", False),  # Wrong checksum
        ("12345", False),  # Too short
        ("9011054455677", False),  # Too long
        ("9011054455a", False),  # Non-digit characters
        ("", False),  # Empty string
        (None, False),  # None value
    ],
)
def test_is_valid_pesel(pesel_input, expected_valid):
    assert is_valid_pesel(pesel_input) == expected_valid


@pytest.mark.parametrize(
    "payload, expected_pesel",
    [
        ({"envelope": {"applications": [{"policies": [{"personInfo": {"pesel": "90110544556"}}]}]}}, "90110544556"),
        ({"envelope": {"applications": [{"policies": [{"personInfo": {"pesel": "  90110544556  "}}]}]}}, "90110544556"),  # Whitespace strip
        ({"envelope": {"applications": [{"policies": [{"personInfo": {"pesel": None}}]}]}}, None),
        ({"envelope": {"applications": []}}, None),
        ({}, None),
        ("not_a_dict", None),
    ],
)
def test_extract_pesel_edge_cases(payload, expected_pesel):
    assert extract_pesel(payload) == expected_pesel