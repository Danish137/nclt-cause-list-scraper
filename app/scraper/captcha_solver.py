import re
import operator
from ..errors.scraper_errors import CaptchaError

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}

def solve_math(expr: str) -> int:
    """
    Extracts and solves math captcha like: '1 + 7 ='
    """
    match = re.search(r"(\d+)\s*([+\-*/])\s*(\d+)", expr)
    if not match:
        raise CaptchaError(f"Could not parse captcha expression: {expr}")
    a, op, b = match.groups()
    return OPS[op](int(a), int(b))
