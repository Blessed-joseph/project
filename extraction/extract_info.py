import fitz  # PyMuPDF
from pathlib import Path
import re



# je cree une liste des livres de la bible en  anglais
BOOKS_OF_BIBLE = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]

# je crée un pattern regex pour détecter les références bibliques
book_pattern = "|".join(
    sorted((re.escape(b) for b in BOOKS_OF_BIBLE), key=len, reverse=True)
)

# j'implemente le fomalise ppour les references bibliques
BIBLE_REF_RE = re.compile(
    rf"\b(?:{book_pattern})\s*\.?\s*(\d+)(?:[:.,]\s*(\d+(?:[-–—]\d+)?))?\b",
    flags=re.IGNORECASE,
)


# je construis la fonction qui fait l'extraction des informations


# def extraire_infos(pdf_path: Path) -> dict:
#     """
#     Cette fonction extrait le texte et les images d'un fichier PDF.
#     Args:
#         pdf_path (str): Le chemin vers le fichier PDF.
#     Returns:
#         dict: Un dictionnaire contenant le texte et les images extraits.
#     """
#     # j'ouvre le document PDF
#     doc = fitz.open(pdf_path)
#     # je recupère la première page du document
#     page = doc.load_page(0)
#     # je récupère le texte de la page
#     texte_complet = page.get_text()

#     # je parcours page par page


#     return {
#         "texte": texte_complet,
#     }

#  j'appele la fonction poour la date


# def extraire_infos(pdf_path: Path) -> dict:
#     """
#     Extrait texte d'un PDF non scanné et identifie :
#       - title : heuristique (plus grande taille en haut de page)
#       - dates : via find_dates_english
#       - key_verse : bloc autour de la mention "Key verse"
#       - bible_refs : toutes les références bibliques détectées
#       - texte : texte complet
#     """
#     doc = fitz.open(pdf_path)
#     spans = []
#     texte_complet = ""

#     # parcourir chaque page et collecter spans (texte + taille + bbox)
#     # juste pour la première page, on pourrait étendre à tout le doc si besoin
#     page_num = 0
#     page = doc.load_page(page_num)
#     page_dict = page.get_text("dict")
#     for block in page_dict.get("blocks", []):
#         if block.get("type") != 0:
#             continue
#         block_bbox = block.get("bbox", [0, 0, 0, 0])
#         for line in block.get("lines", []):
#             for span in line.get("spans", []):
#                 txt = span.get("text", "").strip()
#                 if not txt:
#                     continue
#                 span_bbox = span.get("bbox", block_bbox)
#                 spans.append(
#                     {
#                         "text": txt,
#                         "size": span.get("size", 0),
#                         "font": span.get("font", ""),
#                         "bbox": span_bbox,
#                         "page": page_num + 1,
#                         "block_top": block_bbox[1],
#                     }
#                 )
#                 texte_complet += txt + "\n"

#     doc.close()

#     # -------------------
#     # titre : heuristique -> plus grande taille proche du haut (première page prioritaire)
#     title = ""
#     if spans:
#         # considérer d'abord spans de la première page si présents
#         spans_page1 = [s for s in spans if s["page"] == 1] or spans
#         candidate = sorted(spans_page1, key=lambda s: (-s["size"], s["block_top"]))[0]
#         top_y = candidate["block_top"]
#         size_threshold = max(1.0, candidate["size"] * 0.7)
#         title_spans = [
#             s
#             for s in spans_page1
#             if abs(s["block_top"] - top_y) < 20 and s["size"] >= size_threshold
#         ]
#         title_spans = sorted(title_spans, key=lambda s: s["bbox"][0])
#         title = " ".join(s["text"] for s in title_spans).strip() or candidate["text"]

#     # -------------------
#     # dates (anglais) : utiliser la fonction importée find_dates_english
#     dates = []
#     try:
#         from extraction.ident_date import find_dates_english
#     except ImportError:
#         dates = []
#     else:
#         dates = find_dates_english(texte_complet)

#     # -------------------
#     # key verse : chercher "Key verse" et capturer le texte adjacent
#     key_verse = ""
#     m = re.search(
#         r"(Key verse[:\u2014\-–—]?\s*)(.+?)(?:\n{2,}|\n[A-Z]{2,}|\Z)",
#         texte_complet,
#         flags=re.I | re.S,
#     )
#     if m:
#         key_verse = m.group(2).strip()
#     else:
#         # fallback : prendre la ligne(s) suivant une occurrence de "Key" ou "Key verse"
#         m2 = re.search(
#             r"(^.*Key\s*verse.*$[\s\S]{0,250})", texte_complet, flags=re.I | re.M
#         )
#         if m2:
#             key_verse = m2.group(1).strip()

#     # -------------------
#     # références bibliques : toutes les occurrences via BIBLE_REF_RE
#     bible_refs = [bm.group(0).strip() for bm in BIBLE_REF_RE.finditer(texte_complet)]

#     result = {
#         "title": title,
#         "dates": dates,  # liste de dicts {match, iso, weekday}
#         "key_verse": key_verse,
#         "texte": texte_complet,
#         "bible_refs": bible_refs,
#     }

#     return result


# ...existing code...
def extraire_infos(pdf_path: Path) -> dict:

    doc = fitz.open(pdf_path)  # ouvre le document PDF donné par pdf_path
    blocks = []  # liste qui contiendra les blocs textuels et images extraits

    # parcourir toutes les pages du document
    for pindex in range(doc.page_count):
        print(pindex)
        page = doc.load_page(pindex)  # charge la page pindex
        pd = page.get_text("dict")  # récupère la structure texte de la page sous forme de dict
        # itérer sur chaque bloc renvoyé par PyMuPDF (texte, images, ...)
        for block in pd.get("blocks", []):
            btype = block.get("type", 0)  # type du bloc (0 = texte, autre = image/forme)
            bbox = block.get("bbox", [0, 0, 0, 0])  # bbox du bloc [x0, y0, x1, y1]
            if btype == 0:  # si c'est un bloc texte
                line_items = []  # on va reconstituer les lignes du bloc
                # parcourir les lignes du bloc
                for line in block.get("lines", []):
                    line_text_parts = []  # fragments de texte (spans) pour cette ligne
                    # parcourir les spans (texte avec même font/size)
                    for span in line.get("spans", []):
                        txt = span.get("text", "")  # obtenir le texte du span
                        if txt is None:
                            continue  # ignorer spans sans texte
                        line_text_parts.append(txt.strip())  # ajouter le texte nettoyé
                    if line_text_parts:
                        # joindre les spans de la ligne par un espace
                        line_items.append(" ".join(line_text_parts).strip())
                # joindre les lignes du bloc par des sauts de ligne pour préserver la mise en forme
                block_text = "\n".join([li for li in line_items if li])
                # ajouter le bloc texte à la liste avec métadonnées de position
                blocks.append(
                    {
                        "type": "text",
                        "page": pindex + 1,
                        "top": bbox[1],
                        "left": bbox[0],
                        "text": block_text.strip(),
                        "bbox": bbox,
                    }
                )
            else:
                # si ce n'est pas du texte, considérer comme image/objet et stocker minimalement
                blocks.append(
                    {
                        "type": "image",
                        "page": pindex + 1,
                        "top": bbox[1],
                        "left": bbox[0],
                        "text": "",
                        "bbox": bbox,
                    }
                )

    doc.close()  # fermer le document après extraction

    # trier les blocs dans l'ordre de lecture : page, top (y), left (x)
    blocks_sorted = sorted(blocks, key=lambda b: (b["page"], b["top"], b["left"]))

    # helper : détecte si un bloc texte est probablement un numéro de page isolé
    def is_page_number(t: str) -> bool:
        return bool(re.fullmatch(r"\s*\d{1,3}\s*", t))

    # filtrer les blocs pour enlever les numéros de page seuls
    blocks_filtered = [b for b in blocks_sorted if not (b["type"] == "text" and is_page_number(b["text"]))]

    # helpers pour détecter en-têtes et labels spécifiques
    MONTHS_RE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b", re.I)
    WEEKDAY_RE = re.compile(r"\b(?:MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)\b", re.I)

    # retourne True si le texte contient un mois ET un jour (ex: JANUARY 1)
    def contains_month_and_day(t: str) -> bool:
        return bool(MONTHS_RE.search(t)) and bool(re.search(r"\b\d{1,2}\b", t))

    # retourne True si le texte contient la balise TEXT: ou TEXT -
    def is_text_label(t: str) -> bool:
        return bool(re.search(r"\bTEXT\s*[:\-]\s*", t, re.I))

    # retourne True si le texte mentionne "Key verse"
    def is_key_verse_heading(t: str) -> bool:
        return bool(re.search(r"\bkey\s*verse\b", t, re.I))

    # retourne True si le texte est le heading "THOUGHT FOR THE DAY"
    def is_thought_heading(t: str) -> bool:
        return bool(re.search(r"\bthought\s*for\b.*\bday\b", t, re.I))

    # retourne True si le texte mentionne "Bible in One Year" ou "ONE YEAR"
    def is_bible_one_year_heading(t: str) -> bool:
        return bool(re.search(r"\b(bible\s+in\b.*one\s+year|ONE\s+YEAR)\b", t, re.I))

    # heuristique : repérer l'indice du début de l'article principal (paragraphe long commençant par une majuscule)
    ARTICLE_MIN_LEN = 80  # longueur minimale pour considérer un bloc comme début d'article
    article_idx = None  # index du bloc de début d'article trouvé
    for i, b in enumerate(blocks_filtered):
        t = b["text"].strip() if b["type"] == "text" else ""  # texte nettoyé du bloc
        t_norm = re.sub(r"^\s+", "", t)  # normaliser début de texte
        # si bloc suffisamment long et commence par Majuscule+minuscule, considérer comme article
        if t_norm and len(t_norm) >= ARTICLE_MIN_LEN and re.match(r"[A-Z][a-z]", t_norm.replace("\n", " ")):
            article_idx = i  # mémoriser l'index de début d'article
            break

    # headers : blocs avant l'article (ou quelques premiers blocs si article non trouvé)
    headers = blocks_filtered[:article_idx] if article_idx is not None else blocks_filtered[:6]

    # initialiser valeurs à extraire
    date_header = ""  # en-tête date (ex: THURSDAY / JANUARY 1)
    title = ""  # titre principal
    text_ref = ""  # label TEXT: PSALMS ...

    # extraire date_header : premier header contenant jour/mois ou jour semaine
    for h in headers:
        if h["type"] == "text" and (contains_month_and_day(h["text"]) or WEEKDAY_RE.search(h["text"])):
            date_header = h["text"].strip()
            break

    # extraire text_ref (ligne commençant par TEXT: ou TEXT -)
    for h in headers:
        if h["type"] == "text" and is_text_label(h["text"]):
            text_ref = h["text"].strip()
            break

    # extraire title : premier header texte qui n'est pas date ni TEXT et qui contient des minuscules (casse mixte -> titre)
    for h in headers:
        t = h["text"].strip()
        if not t:
            continue
        if t == date_header or t == text_ref:
            continue
        if re.search(r"[a-zà-ÿ]", t):  # présence de minuscules -> probable titre en casse normale
            title = t
            break
    # fallback : si aucun titre trouvé, prendre le premier header text non vide
    if not title and headers:
        for h in headers:
            if h["type"] == "text" and h["text"].strip():
                title = h["text"].strip()
                break

    # 2) Key verse : trouver le bloc "Key verse" puis associer tout son contenu jusqu'au point final '.' rencontré
    key_verse = ""  # contiendra la phrase/verset complet associé au heading Key verse
    key_idx = None
    for i, b in enumerate(blocks_filtered):
        if b["type"] == "text" and is_key_verse_heading(b["text"]):
            key_idx = i  # index où apparaît "Key verse"
            break
    if key_idx is not None:
        parts = []  # fragments de texte à assembler pour former le key verse
        # si une image est immédiatement avant le heading, la noter (pas utilisée ici mais respectée)
        assoc_image = None
        if key_idx - 1 >= 0 and blocks_filtered[key_idx - 1]["type"] == "image":
            assoc_image = blocks_filtered[key_idx - 1]
        # parcourir les blocs à partir du heading jusqu'à une condition d'arrêt
        for j in range(key_idx, len(blocks_filtered)):
            b = blocks_filtered[j]
            if b["type"] == "text":
                parts.append(b["text"].strip())  # ajouter le texte du bloc
                # condition d'arrêt : le bloc se termine par un point '.' OU contient une référence biblique fermée (ex: (Psalm 77:11))
                if re.search(r"\.\s*$", b["text"]) or re.search(r"\([^)]+Psalm[^\)]*\)\.?$", b["text"], re.I):
                    break  # fin du key verse atteint
            else:
                # si on rencontre une image, on la mémorise mais on ne stoppe pas nécessairement
                if assoc_image is None:
                    assoc_image = b
        key_verse = "\n".join(p for p in parts if p)  # assembler les parties trouvées

    # 3) Article principal : extraire à partir de article_idx jusqu'à la prochaine section majeure (Thought/Bible/key)
    article = ""
    if article_idx is not None:
        parts = []
        for b in blocks_filtered[article_idx:]:
            t = b["text"].strip() if b["type"] == "text" else ""
            # si on rencontre un heading majeur, on arrête l'article
            if is_thought_heading(t) or is_bible_one_year_heading(t) or is_key_verse_heading(t):
                break
            parts.append(t)  # ajouter le bloc texte à l'article
        article = "\n\n".join(p for p in parts if p)  # assembler en paragraphes

    # 4) Bible in one year : détecter et rassembler son contenu
    bible_in_one_year = ""
    for i, b in enumerate(blocks_filtered):
        if b["type"] == "text" and is_bible_one_year_heading(b["text"]):
            t = b["text"]
            m = re.search(r":\s*(.+)$", t)  # si contenu après ':' dans le même bloc
            if m:
                bible_in_one_year = m.group(1).strip()
            else:
                # sinon récupérer les petits blocs suivants jusqu'à un autre heading majeur
                parts = []
                for nxt in blocks_filtered[i + 1 :]:
                    nt = nxt["text"].strip() if nxt["type"] == "text" else ""
                    if is_thought_heading(nt) or is_key_verse_heading(nt):
                        break
                    parts.append(nt)
                bible_in_one_year = " ".join(p for p in parts if p)
            break

    # 5) Thought for the day : détecter et rassembler son contenu séparément
    thought_for_the_day = ""
    for i, b in enumerate(blocks_filtered):
        if b["type"] == "text" and is_thought_heading(b["text"]):
            t = b["text"]
            m = re.search(r":\s*(.+)$", t)  # contenu sur la même ligne après ':'
            if m:
                thought_for_the_day = m.group(1).strip()
            else:
                # sinon rassembler les blocs suivants jusqu'à la prochaine section majeure
                parts = []
                for nxt in blocks_filtered[i + 1 :]:
                    nt = nxt["text"].strip() if nxt["type"] == "text" else ""
                    if is_bible_one_year_heading(nt) or is_key_verse_heading(nt):
                        break
                    parts.append(nt)
                thought_for_the_day = "\n".join(p for p in parts if p)
            break

    # reconstruire le texte complet brut dans l'ordre de lecture (séparateur double ligne pour blocs)
    texte = "\n\n".join(b["text"] for b in blocks_filtered if b["type"] == "text" and b["text"].strip())

    # construire le dictionnaire résultat avec toutes les parties extraites
    result = {
        "date_header": date_header,
        "title": title,
        "text_ref": text_ref,
        "key_verse": key_verse,
        "article": article,
        "bible_in_one_year": bible_in_one_year,
        "thought_for_the_day": thought_for_the_day,
        "texte": texte,
        "ordered_blocks": [b for b in blocks_filtered],
    }

    return result 