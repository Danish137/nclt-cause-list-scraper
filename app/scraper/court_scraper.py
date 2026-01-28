from bs4 import BeautifulSoup
from ..errors.scraper_errors import CourtMappingError

def parse_court_options(html: str) -> dict:
    """
    Parses dropdown and returns {court_name: value_id}
    """
    soup = BeautifulSoup(html, "lxml")
    select = soup.select_one("select[id^=edit-field-nclt-benches-list-target-id]")
    if not select:
        raise CourtMappingError("Unable to locate court select element")

    mapping = {}
    for opt in select.find_all("option"):
        name = opt.text.strip()
        value = opt.get("value", "").strip()
        if name and value:
            mapping[name] = value
    return mapping
