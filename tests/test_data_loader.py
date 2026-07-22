import pytest
from src.data_loader import load_csv_file


def test_load_csv_file_returns_empty_dict_on_missing_file(tmp_path):
    """
    Should handle missing file gracefully and return an empty dictionary (or raise FileNotFoundError).
    """
    non_existent_file = tmp_path / "ghost_file.csv"

    with pytest.raises(FileNotFoundError):
        load_csv_file(non_existent_file)


def test_load_csv_file_reads_valid_data(tmp_path):
    """
    Should correctly parse a valid CSV file into a dictionary.
    """

    csv_file = tmp_path / "test_blacklist.csv"
    csv_file.write_text(
        "pesel,reason\n90110544556,Fraud\n", encoding="utf-8"
    )

    result = load_csv_file(csv_file)
    assert result == {"90110544556": "Fraud"}