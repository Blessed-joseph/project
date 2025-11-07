BOOK_NAMES = [
    # french names (exemples, ajoute les variantes/abréviations que tu veux)
    "Genèse", "Exode", "Lévitique", "Nombres", "Deutéronome", "Josué", "Juges", "Ruth",
    "1 Samuel", "2 Samuel", "1 Rois", "2 Rois", "1 Chroniques", "2 Chroniques",
    "Esdras", "Néhémie", "Esther", "Job", "Psaumes", "Proverbes", "Ecclésiaste",
    "Cantique des Cantiques", "Isaïe", "Jérémie", "Lamentations", "Ézéchiel", "Daniel",
    "Osée", "Joël", "Amos", "Abdias", "Jonas", "Michée", "Nahum", "Habacuc", "Sophonie",
    "Aggée", "Zacharie", "Malachie",
    # nouveaux testaments (fr)
    "Matthieu", "Marc", "Luc", "Jean", "Actes", "Romains", "1 Corinthiens", "2 Corinthiens",
    "Galates", "Éphésiens", "Philippiens", "Colossiens", "1 Thessaloniciens", "2 Thessaloniciens",
    "1 Timothée", "2 Timothée", "Tite", "Philémon", "Hébreux", "Jacques", "1 Pierre", "2 Pierre",
    "1 Jean", "2 Jean", "3 Jean", "Jude", "Apocalypse",
    # ajoute variantes anglaises si besoin
    "Psalm", "Psalms", "Isaiah", "Jeremiah", "Revelation", "1 Samuel", "2 Samuel",
]

import re
# créer motif sûr : échapper noms, trier par longueur décroissante pour préférer matches longs
book_pattern = "|".join(sorted((re.escape(b) for b in BOOK_NAMES), key=len, reverse=True))

# motif pour chapitres et versets (exemple simple : "Book 77:11-14" ou "Psalms 77:11")
BIBLE_REF_RE = re.compile(
    rf"\b(?:{book_pattern})\s*\.?\s*(\d+)(?:[:.,]\s*(\d+(?:[-–—]\d+)?))?\b",
    flags=re.IGNORECASE,
)

# Exemples d'utilisation
texts = [
    "TEXT: PSALMS 77:11-14",
    "Key verse — Psalm 77:11",
    "Psaumes 23",
    "1 Samuel 3:1",
]

for t in texts:
    m = BIBLE_REF_RE.search(t)
    if m:
        print("Matched:", m.group(0), "chapter:", m.group(1), "verse part:", m.group(2))
    else:
        print("No match in:", t)






import re
from datetime import date

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
MONTHS_MAP = {m.lower(): i + 1 for i, m in enumerate(MONTHS)}
month_pattern = "|".join(sorted((re.escape(m) for m in MONTHS), key=len, reverse=True))

DATE_RE = re.compile(
    rf"\b(?:(?P<weekday>[A-Za-z]+)\s*[\r\n]+\s*)?(?P<month>{month_pattern})[ ,\n\r\t]+(?P<day>\d{{1,2}})(?:[ ,\n\r\t]+(?P<year>\d{{4}}))?",
    flags=re.IGNORECASE,
)


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
            results.append({"match": m.group(0).strip(), "iso": d.isoformat(), "weekday": m.group("weekday")})
        except Exception:
            continue
    return results


# examples / quick manual test
SAMPLES = [
    "THURSDAY\nJANUARY 1",
    "THURSDAY\r\nJANUARY 1, 2025",
    "FRIDAY\nFEBRUARY 12",
    "JANUARY 31",
    "This is not a date",
    "WEDNESDAY\nMARCH 3 2024",
]

if __name__ == "__main__":
    for s in SAMPLES:
        print("INPUT:", repr(s))
        print("FOUND:", find_dates_english(s))
        print("-" * 40)


# pytest tests (optional)
def test_find_dates_basic():
    assert find_dates_english("THURSDAY\nJANUARY 1")[0]["iso"].endswith("-01-01")
    assert find_dates_english("JANUARY 1, 2025")[0]["iso"] == "2025-01-01"
    assert find_dates_english("FRIDAY\nFEBRUARY 12")[0]["iso"].endswith("-02-12")
    assert find_dates_english("This is not a date") == []