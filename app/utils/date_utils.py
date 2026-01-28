from datetime import datetime

def convert_to_nclt_format(date_str: str) -> str:
    """
    Converts YYYY-MM-DD → MM/DD/YYYY for NCLT format.
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%m/%d/%Y")
