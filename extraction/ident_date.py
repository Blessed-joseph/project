from datetime import date
import re

#######Pour les dates ##########

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
MONTHS_MAP = {m.lower(): i + 1 for i, m in enumerate(MONTHS)}
month_pattern = "|".join(sorted((re.escape(m) for m in MONTHS), key=len, reverse=True))

DATE_RE = re.compile(
    rf"\b(?:(?P<weekday>[A-Za-z]+)\s*[\r\n]+\s*)?(?P<month>{month_pattern})[ ,\n\r\t]+(?P<day>\d{{1,2}})(?:[ ,\n\r\t]+(?P<year>\d{{4}}))?",
    flags=re.IGNORECASE,
)
####### Fin des dates ##########


def find_dates_english(text: str):
    results = []
    for m in DATE_RE.finditer(text):
        month_s = m.group("month").lower()
        day_s = m.group("day")
        year_s = m.group("year")
        try:
            month_n = MONTHS_MAP.get(month_s)
            if not month_n:
                continue
            day_n = int(day_s)
            year_n = int(year_s) if year_s else date.today().year
            d = date(year_n, month_n, day_n)
            results.append(
                {
                    "match": m.group(0).strip(),
                    "iso": d.isoformat(),
                    "weekday": m.group("weekday"),
                }
            )
        except (ValueError, TypeError):
            continue
    return results
