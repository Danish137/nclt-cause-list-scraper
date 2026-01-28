from bs4 import BeautifulSoup

def parse_results(html: str) -> list:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    if not table:
        return []

    rows = table.find_all("tr")[1:]   # Skip header row
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue

        title = cols[0].text.strip()
        court = cols[1].text.strip()
        entries = cols[2].text.strip()
        pdf_tag = cols[3].find("a")
        pdf = pdf_tag['href'] if pdf_tag else None
        file_size = cols[4].text.strip()
        cause_date = cols[5].text.strip()

        data.append({
            "title": title,
            "court": court,
            "no_of_entries": int(entries or 0),
            "pdf_file": pdf,
            "file_size": file_size,
            "cause_date": cause_date
        })

    return data
