from ..schemas import CauseListResponse, CauseItem
from ..errors.http_errors import http_400, http_500, http_429
from ..scraper.session_manager import NCLTSession
from ..scraper.court_scraper import parse_court_options
from ..scraper.fetch_results import fetch_initial_page, extract_captcha, fetch_results
from ..scraper.captcha_solver import solve_math
from ..scraper.parse_results import parse_results
from ..utils.cache import set_cache, get_cache
from ..utils.rate_limiter import limiter
from ..utils.retry_utils import retry_async

async def fetch_cause_list(params):
    # Rate limiting
    if not limiter.allow():
        return http_429("Please wait before sending more requests.")

    cache_key = f"{params.from_date}:{params.to_date}:{params.court or 'ALL'}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    async with NCLTSession() as session:
        # retry wrapper for network fragility
        html = await retry_async(lambda: fetch_initial_page(session))

        court_map = parse_court_options(html)

        # Court validation
        if params.court:
            if params.court not in court_map:
                return http_400(f"Invalid court: {params.court}")
            court_id = court_map[params.court]
        else:
            court_id = "All"

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        cid, token, expr = extract_captcha(soup)
        answer = solve_math(expr)

        result_html = await retry_async(
            lambda: fetch_results(
                session=session,
                court_id=court_id,
                from_date=params.from_date,
                to_date=params.to_date,
                captcha_sid=cid,
                captcha_token=token,
                captcha_answer=answer
            )
        )

        items = parse_results(result_html)

        resp = CauseListResponse(
            success=True,
            data=[CauseItem(**item) for item in items],
            total_records=len(items),
            message="Data fetched successfully"
        )

        set_cache(cache_key, resp, ttl=60)
        return resp
