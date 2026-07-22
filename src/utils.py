import re

def extract_pesel(request_data: dict) -> str | None:
    """
    Extracts the PESEL number from the request data.
    """
    try:
        pesel = request_data["envelope"]["applications"][0]["policies"][0]["personInfo"]["pesel"]

        if pesel is None:
            return None

        pesel_str = str(pesel).strip()
        return pesel_str if pesel_str else None

    except (KeyError, IndexError, TypeError, AttributeError):
        return None

def is_valid_pesel_format(pesel: str) -> bool:
    """
    Validates the format of a PESEL number.
    """
    if not isinstance(pesel, str):
        return False
    return bool(re.fullmatch(r"\d{11}", pesel))

def is_valid_pesel(pesel: str) -> bool:
    """
    Validates the length, format andchecksum of a PESEL number. 
    """
    if not is_valid_pesel_format(pesel):
        return False
    
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    digits = [int(char) for char in pesel]

    checksum = sum(w * d for w, d in zip(weights, digits[:10]))
    control_digit = (10 - (checksum % 10)) % 10

    return control_digit == digits[10]