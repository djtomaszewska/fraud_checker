from pathlib import Path
from src.data_loader import load_csv_file
from src.utils import extract_pesel, is_valid_pesel

class TariffValidator:
    def __init__(self, pesel_blacklist_path: str | Path):
        """
        Initialize the validator with a blacklist of invalid PESEL numbers.
        """
        self.pesel_blacklist = load_csv_file(pesel_blacklist_path)
    
    def validate(self, request_data: dict) -> dict:
        """ 
        Validates the request.
        Returns a dictionary with the decision (ACCEPT or REJECT) and reason for the decision.
        """
        request_id = (
            request_data.get("envelope", {})
            .get("meta", {})
            .get("requestId", "UNKNOWN")
        )
        
        pesel = extract_pesel(request_data)
        if not pesel:
            return {
                "requestId": request_id,
                "decision": "REJECT",
                "reason": "Brak numeru PESEL w zapytaniu lub niepoprawna struktura JSON",
            }
        if not is_valid_pesel(pesel):
            return {
                "requestId": request_id,
                "decision": "REJECT",
                "reason": f"Nieprawidłowy numer PESEL: {pesel} (błąd cyfry kontrolnej lub formatu)",
            }
        if pesel in self.pesel_blacklist:
            reason = self.pesel_blacklist[pesel]
            return {
                "requestId": request_id,
                "decision": "REJECT",
                "reason": f"PESEL znajduje się na czarnej liście. Powód: {reason}",
            }
        return {
            "requestId": request_id,
            "decision": "ACCEPT",
            "reason": "Weryfikacja pozytywna - brak przeciwwskazań",
        }