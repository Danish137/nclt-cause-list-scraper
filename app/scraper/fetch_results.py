from bs4 import BeautifulSoup
from ..utils.date_utils import convert_to_nclt_format
from ..errors.scraper_errors import CaptchaError, ScrapeError
from ..utils.config import BASE_URL
from .captcha_solver import solve_math

async def fetch_initial_page(session):
    """
    Fetch initial page to extract:
    - court dropdown
    - captcha tokens
    - math expression
    """
    resp = await session.get(BASE_URL)
    if resp.status_code != 200:
        raise ScrapeError("Failed to fetch NCLT page")
    return resp.text


def extract_captcha(soup):
    """
    Extract captcha_sid, captcha_token, math_expr
    """
    sid = soup.select_one('input[name="captcha_sid"]')
    token = soup.select_one('input[name="captcha_token"]')
    expr = soup.select_one('.field-prefix')

    if not (sid and token and expr):
        raise CaptchaError("Failed to extract CAPTCHA components")

    return sid['value'], token['value'], expr.text.strip()


async def fetch_results(session, court_id, from_date, to_date, captcha_sid, captcha_token, captcha_answer):
    """
    Executes the GET search request
    """
    params = {
        "field_nclt_benches_list_target_id": court_id,
        "field_cause_date_value": convert_to_nclt_format(from_date),
        "field_cause_date_value_1": convert_to_nclt_format(to_date),
        "captcha_sid": captcha_sid,
        "captcha_token": captcha_token,
        "captcha_response": captcha_answer,
    }

    resp = await session.get(BASE_URL, params=params)
    if resp.status_code != 200:
        raise ScrapeError("Failed to fetch results")

    return resp.text
