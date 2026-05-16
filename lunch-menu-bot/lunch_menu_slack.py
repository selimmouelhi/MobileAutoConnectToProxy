#!/usr/bin/env python3
"""
Office Guru Lunch Menu → Slack Bot
Fetches the weekly lunch menu from Office Guru and posts it to Slack.
Runs every Monday via launchd — sends 5 messages (one per day Mon–Fri).
"""

import os
import re
import sys
import tempfile
from datetime import datetime, timedelta

import httpx
import pdfplumber
from dotenv import load_dotenv

# Load .env file from same directory as this script
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# ─── Configuration ───────────────────────────────────────────────────────────
EMAIL = os.environ.get("OG_EMAIL", "selim.mouelhi@framna.com")
PASSWORD = os.environ.get("OG_PASSWORD", "")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID", "")
SEND_HOUR = 12  # Hour to deliver messages (24h format)
SEND_MINUTE = 30  # Minute to deliver messages

API_BASE = "https://api.officeguru.com/employee-app"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "OG-App-Name": "employee",
    "Origin": "https://my.officeguru.com",
    "Referer": "https://my.officeguru.com/",
}

DAY_NAMES_DA = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag"]
DAY_NAMES_EN = ["monday", "tuesday", "wednesday", "thursday", "friday"]
DA_TO_EN = dict(zip(DAY_NAMES_DA, [d.capitalize() for d in DAY_NAMES_EN]))
EN_TO_DA = {v: k.capitalize() for k, v in DA_TO_EN.items()}

DIVIDER = "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"

# Known allergen words to strip from food descriptions
ALLERGENS = [
    "Svovldioxid og sulfitter", "Glutenfri", "Laktosefri",
    "Vegetar", "Vegansk", "Gluten", "Mælk", "Æg", "Gris", "Okse",
    "Fisk", "Selleri", "Soja", "Sennep", "Nødder", "Sesam",
    "Jordnødder", "Hvidløg", "Chili", "Koriander",
]

# Emoji mapping: keywords in section name → emoji (order matters: specific before generic)
EMOJI_MAP = [
    (":seedling:", ["vegansk", "vegan"]),
    (":leafy_green:", ["vegetar", "green noon"]),
    (":cut_of_meat:", ["klassisk", "full noon", "hot dish", "varm ret"]),
    (":green_salad:", ["salat", "salad"]),
    (":plate_with_cutlery:", ["brød", "bread", "kold", "cold", "tilbehør"]),
    (":cake:", ["kage", "cake"]),
]


# ─── Office Guru API ─────────────────────────────────────────────────────────

def login(client: httpx.Client) -> str:
    """Login and return the auth token."""
    resp = client.post(
        f"{API_BASE}/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
        headers=HEADERS,
    )
    resp.raise_for_status()
    data = resp.json()

    token = data.get("token") or data.get("data", {}).get("token")
    if token:
        return token

    for cookie in client.cookies.jar:
        if "token" in cookie.name.lower():
            return cookie.value

    auth_header = resp.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]

    raise RuntimeError(
        f"Could not extract auth token. Response keys: {list(data.keys())}. "
        f"Cookies: {[c.name for c in client.cookies.jar]}"
    )


def get_lunch_modules(client: httpx.Client, token: str) -> list[dict]:
    """Fetch all lunch modules with their date ranges."""
    auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    resp = client.get(f"{API_BASE}/modules", headers=auth_headers)
    resp.raise_for_status()
    modules = resp.json()["data"]

    lunch_modules = []
    for module in modules:
        if module["type"] != "lunch":
            continue
        detail_resp = client.get(
            f"{API_BASE}/modules/{module['id']}?with_deleted=true",
            headers=auth_headers,
        )
        detail_resp.raise_for_status()
        detail = detail_resp.json()["data"]
        detail["_first_day"] = datetime.fromisoformat(
            detail["first_day"].replace("Z", "+00:00")
        ).date()
        detail["_last_day"] = datetime.fromisoformat(
            detail["last_day"].replace("Z", "+00:00")
        ).date()
        lunch_modules.append(detail)

    if not lunch_modules:
        raise RuntimeError("No lunch modules found")
    return lunch_modules


def get_module_for_date(modules: list[dict], target: "date") -> dict | None:
    """Pick the module whose date range covers the target date."""
    for m in modules:
        if m["_first_day"] <= target <= m["_last_day"]:
            return m
    # Fallback: closest module by start date
    modules_sorted = sorted(modules, key=lambda m: abs((m["_first_day"] - target).days))
    return modules_sorted[0] if modules_sorted else None


def get_menu_pdf_url(client: httpx.Client, token: str, module_id: str) -> str:
    """Fetch the weekly choices to get the menu PDF URL."""
    auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    resp = client.get(
        f"{API_BASE}/modules/{module_id}/choices",
        params={"start_date": monday.isoformat(), "end_date": sunday.isoformat()},
        headers=auth_headers,
    )
    resp.raise_for_status()
    data = resp.json()
    pdf_url = data.get("meta", {}).get("menu", {}).get("file", {}).get("url")
    if not pdf_url:
        raise RuntimeError("No menu PDF found in choices response")
    return pdf_url


# ─── PDF Extraction & Parsing ────────────────────────────────────────────────

def download_pdf(pdf_url: str) -> str:
    """Download the PDF and return the temp file path."""
    resp = httpx.get(pdf_url, follow_redirects=True, verify=False)
    resp.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(resp.content)
        return f.name


def strip_allergens(text: str) -> str:
    """Remove trailing allergen labels from a food description."""
    changed = True
    while changed:
        changed = False
        text = text.strip()
        for allergen in ALLERGENS:
            if text.endswith(allergen):
                text = text[:-len(allergen)].strip()
                changed = True
    return text


def is_column_layout(pdf_path: str) -> bool:
    """Detect if multiple day names appear on the same page (table/column layout)."""
    with pdfplumber.open(pdf_path) as pdf:
        first_text = pdf.pages[0].extract_text() or ""
        day_count = sum(1 for d in DAY_NAMES_DA if d.upper() in first_text.upper())
        return day_count >= 3


def _is_garbled(text: str) -> bool:
    """Detect garbled text like 'F a l a f e l' (spaced-out characters)."""
    words = text.split()
    if len(words) < 4:
        return False
    single_chars = sum(1 for w in words if len(w) == 1)
    return single_chars > len(words) * 0.4


def _truncate_at_garbled(text: str) -> str:
    """Keep text up to the first garbled segment (spaced-out single chars)."""
    # Common short Danish words that are NOT garbled
    common_short = {"i", "og", "af", "en", "et", "de", "på", "vi", "er", "med", "til"}
    words = text.split()
    clean_end = len(words)
    consecutive_single = 0
    for i, w in enumerate(words):
        if len(w) == 1 and w.lower() not in common_short:
            consecutive_single += 1
            if consecutive_single >= 3:
                clean_end = i - consecutive_single + 1
                break
        else:
            consecutive_single = 0
    return " ".join(words[:clean_end]).strip()


def parse_column_pdf(pdf_path: str) -> dict:
    """Parse a column-layout PDF using word-center assignment to columns."""
    from collections import defaultdict

    menu = {}

    # Sections we want to extract (main dishes)
    WANTED_HEADERS = [
        "Den Klassiske - Varm ret", "Den klassiske - Varm ret",
        "Varm ret - Vegetar", "Varm ret - Vegansk",
        "Torsdags kage",
    ]
    # Sections to skip (sides, sauces, salad bars, cold cuts, etc.)
    SKIP_HEADERS = [
        "Den Klassiske - Tilbehør", "Den klassiske - Tilbehør",
        "Tilbehør", "Sauce til", "Kreativ Salat", "Kold ret",
        "Den Klassiske - sauce", "Den klassiske - sauce",
        "Salat buffet", "Dressing", "Toppings",
    ]

    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        words = page.extract_words(x_tolerance=2, y_tolerance=2)

        # Find day header centers
        day_centers = {}
        for w in words:
            wl = w["text"].lower()
            if wl in DA_TO_EN:
                day_centers[wl] = (w["x0"] + w["x1"]) / 2

        if len(day_centers) < 3:
            return menu

        # Column boundaries: midpoints between adjacent day centers
        sorted_days = sorted(day_centers.items(), key=lambda x: x[1])
        boundaries = []
        for i, (day_da, center) in enumerate(sorted_days):
            left = 0 if i == 0 else (sorted_days[i - 1][1] + center) / 2
            right = page.width if i == len(sorted_days) - 1 else (center + sorted_days[i + 1][1]) / 2
            boundaries.append((DA_TO_EN[day_da], left, right))

        # Assign words to columns by center position
        col_words = defaultdict(list)
        for w in words:
            wcenter = (w["x0"] + w["x1"]) / 2
            for day_en, left, right in boundaries:
                if left <= wcenter < right:
                    col_words[day_en].append(w)
                    break

        # For each column: group words into lines, then parse sections
        for day_en, left, right in boundaries:
            day_words = sorted(col_words[day_en], key=lambda w: (w["top"], w["x0"]))

            # Group into text lines by y position
            lines = []
            current_line = []
            current_y = None
            for w in day_words:
                if current_y is None or abs(w["top"] - current_y) < 4:
                    current_line.append(w["text"])
                    current_y = w["top"] if current_y is None else current_y
                else:
                    lines.append(" ".join(current_line))
                    current_line = [w["text"]]
                    current_y = w["top"]
            if current_line:
                lines.append(" ".join(current_line))

            menu.setdefault(day_en, {"da": {}, "en": {}})
            current_section = None

            for line in lines:
                s = line.strip()
                if not s or s.lower() in DA_TO_EN:
                    continue

                # Check for wanted section headers
                matched = None
                for h in WANTED_HEADERS:
                    if s.startswith(h):
                        matched = h
                        break
                if matched:
                    current_section = matched
                    menu[day_en]["da"][current_section] = ""
                    continue

                # Check for skip headers
                if any(s.startswith(h) for h in SKIP_HEADERS):
                    current_section = None
                    continue

                # Append content to current section
                if current_section and current_section in menu[day_en]["da"]:
                    existing = menu[day_en]["da"][current_section]
                    if existing:
                        menu[day_en]["da"][current_section] = existing + " " + s
                    else:
                        menu[day_en]["da"][current_section] = s

            # For Thursday: scan raw text for cake mention if not found as section
            if day_en == "Thursday" and "Torsdags kage" not in menu[day_en]["da"]:
                full_col = "\n".join(lines)
                cake_match = re.search(r"[Tt]orsdags\s*kage\s+(.*?)(?:\n|$)", full_col)
                if cake_match:
                    menu[day_en]["da"]["Torsdags kage"] = cake_match.group(1).strip()

    # Clean up: truncate garbled text, strip allergens, fix artifacts
    for day in menu:
        for section in list(menu[day]["da"]):
            val = menu[day]["da"][section]
            val = _truncate_at_garbled(val)
            val = strip_allergens(val)
            # Remove leading quote artifacts
            val = re.sub(r'^["\'"no"\s]+(?=[A-ZÆØÅ])', '', val).strip()
            if val:
                menu[day]["da"][section] = val
            else:
                del menu[day]["da"][section]

    return menu


def parse_page_per_day_pdf(pdf_path: str) -> dict:
    """Parse a page-per-day PDF (each day gets its own page or section)."""
    with pdfplumber.open(pdf_path) as pdf:
        full_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        raw_text = "\n\n".join(full_text)

    lines = raw_text.split("\n")
    menu = {}
    current_day = None
    current_section = None
    is_english_page = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        lower = stripped.lower()

        # Day header: "Menu / mandag" or "Menu / Monday"
        if lower.startswith("menu / "):
            day_part = lower.replace("menu / ", "").strip()
            if day_part in DA_TO_EN:
                current_day = DA_TO_EN[day_part]
                is_english_page = None
                menu.setdefault(current_day, {"da": {}, "en": {}})
                current_section = None
                continue
            elif day_part in DAY_NAMES_EN:
                current_day = day_part.capitalize()
                is_english_page = True
                menu.setdefault(current_day, {"da": {}, "en": {}})
                current_section = None
                continue

        # All-caps Danish day names
        if lower in DA_TO_EN:
            current_day = DA_TO_EN[lower]
            is_english_page = False
            menu.setdefault(current_day, {"da": {}, "en": {}})
            current_section = None
            continue

        if current_day is None:
            continue

        # Auto-detect language from content markers
        if is_english_page is None:
            en_markers = ["Today's inspiration", "Hot dishes", "Heavy salad",
                          "Light salad", "For bread", "Green piece"]
            da_markers = ["Dagens inspiration", "Fyldig salat", "Let salat",
                          "Til brød", "Grønt stykke"]
            if any(m in stripped for m in en_markers):
                is_english_page = True
            elif any(m in stripped for m in da_markers):
                is_english_page = False
            else:
                is_english_page = False

        lang = "en" if is_english_page else "da"

        # Section headers (pattern: "Label: content")
        if ":" in stripped and len(stripped.split(":")[0]) < 60:
            parts = stripped.split(":", 1)
            section_name = parts[0].strip()
            section_value = parts[1].strip() if len(parts) > 1 else ""
            current_section = section_name
            if section_value:
                menu[current_day][lang][section_name] = section_value
            continue

        # Continuation line
        if current_section and current_day:
            existing = menu[current_day][lang].get(current_section, "")
            if existing:
                menu[current_day][lang][current_section] = existing + " " + stripped
            else:
                menu[current_day][lang][current_section] = stripped

    return menu


def parse_menu_pdf(pdf_path: str) -> dict:
    """Auto-detect PDF format and parse accordingly."""
    if is_column_layout(pdf_path):
        print("  PDF format: column layout (table)")
        return parse_column_pdf(pdf_path)
    else:
        print("  PDF format: page-per-day layout")
        return parse_page_per_day_pdf(pdf_path)


# ─── Slack Formatting ────────────────────────────────────────────────────────

def get_emoji(section_name: str) -> str:
    """Pick an emoji based on keywords in the section name."""
    lower = section_name.lower()
    for emoji, keywords in EMOJI_MAP:
        if any(kw in lower for kw in keywords):
            return emoji
    return ":fork_and_knife:"


def is_cake_section(section_name: str) -> bool:
    """Check if a section is about cake."""
    lower = section_name.lower()
    return "kage" in lower or "cake" in lower


# Sections to display: (emoji, label, da_keywords, en_keywords)
# We search da_data/en_data for keys containing these keywords (first match wins)
DISPLAY_SECTIONS = [
    (":cut_of_meat:", "Meat", ["full noon", "klassiske - varm ret", "klassisk - varm ret"], ["full noon", "hot dish"]),
    (":leafy_green:", "Vegetar", ["green noon", "varm ret - vegetar"], ["green noon", "hot dishes - green"]),
    (":seedling:", "Vegan", ["green noon vegansk", "varm ret - vegansk"], ["vegan green noon", "hot dishes - vegan"]),
    (":green_salad:", "Salad", ["fyldig salat", "kreativ salat"], ["heavy salad"]),
    (":plate_with_cutlery:", "Bread", ["til brød - alle", "til brød", "brød"], ["for bread - all", "for bread", "bread"]),
]


def _find_section(data: dict, keywords: list) -> str | None:
    """Find the first matching section value by keyword search."""
    for kw in keywords:
        for key in data:
            if kw in key.lower():
                val = data[key]
                if val:
                    return val
    return None


def format_day_message(
    day_en: str, date: datetime, menu_day: dict, partner_name: str
) -> str:
    """Format a single day's Slack message."""
    day_da = EN_TO_DA.get(day_en, day_en)
    date_str = date.strftime("%b %d").lstrip("0")
    da_data = menu_day.get("da", {})
    en_data = menu_day.get("en", {})

    lines = []
    lines.append(f":fork_and_knife: _TODAY'S LUNCH — {day_da} / {day_en} ({date_str})_")
    lines.append(f"_{partner_name} | Framna Denmark_")
    lines.append("")
    lines.append(DIVIDER)

    # Theme / inspiration
    da_insp = _find_section(da_data, ["inspiration"])
    en_insp = _find_section(en_data, ["inspiration"])
    if da_insp:
        lines.append("")
        if en_insp:
            lines.append(f"_Dagens inspiration: {da_insp} / {en_insp}_")
        else:
            lines.append(f"_Dagens inspiration: {da_insp}_")

    # Main menu sections
    for emoji, label, da_keywords, en_keywords in DISPLAY_SECTIONS:
        da_val = _find_section(da_data, da_keywords)
        en_val = _find_section(en_data, en_keywords)

        if not da_val and not en_val:
            continue

        lines.append("")
        if da_val:
            lines.append(f"{emoji} _{label}:_ {da_val}")
            if en_val:
                lines.append(f"_{en_val}_")
        elif en_val:
            lines.append(f"{emoji} _{label}:_ {en_val}")

    lines.append("")
    lines.append(DIVIDER)

    # Special Thursday cake section
    da_cake = _find_section(da_data, ["kage", "torsdags kage"])
    en_cake = _find_section(en_data, ["cake"])
    if day_en == "Thursday" and (da_cake or en_cake):
        lines.append("")
        lines.append(":cake: :cake: :cake:  *TORSDAGSKAGE / THURSDAY CAKE*  :cake: :cake: :cake:")
        if da_cake and en_cake:
            lines.append(f"_{da_cake}_")
            lines.append(f"_{en_cake}_")
        elif da_cake:
            lines.append(f"_{da_cake}_")
        elif en_cake:
            lines.append(f"_{en_cake}_")
        lines.append("")
        lines.append(DIVIDER)

    # Rating section
    lines.append("")
    lines.append("> _Rate today's lunch!_")
    lines.append("> :face_vomiting: = 0  :confused: = 1  :neutral_face: = 2  :slightly_smiling_face: = 3  :yum: = 4  :star-struck: = 5")

    return "\n".join(lines)


# ─── Slack Posting ───────────────────────────────────────────────────────────

def schedule_slack_message(text: str, post_at: int) -> dict:
    """Schedule a message via Slack Bot API."""
    resp = httpx.post(
        "https://slack.com/api/chat.scheduleMessage",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json={
            "channel": SLACK_CHANNEL_ID,
            "text": text,
            "post_at": post_at,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error')}")
    return data


def post_slack_message(text: str) -> dict:
    """Post a message immediately via Slack Bot API."""
    resp = httpx.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json={
            "channel": SLACK_CHANNEL_ID,
            "text": text,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error')}")
    return data


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"[{datetime.now().isoformat()}] Starting lunch menu bot...")

    if not PASSWORD:
        print("ERROR: OG_PASSWORD environment variable is required")
        sys.exit(1)
    if not SLACK_BOT_TOKEN and "--dry-run" not in sys.argv:
        print("ERROR: SLACK_BOT_TOKEN environment variable is required")
        sys.exit(1)

    # Check if already scheduled this week (avoid duplicates)
    sent_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "logs", ".last_scheduled"
    )
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())

    if os.path.exists(sent_file) and "--dry-run" not in sys.argv:
        with open(sent_file) as f:
            last_week = f.read().strip()
        if last_week == monday.isoformat():
            print(f"Already scheduled for week of {monday} — skipping")
            return

    with httpx.Client(follow_redirects=True, proxy=None, verify=False) as client:
        # 1. Login
        print("Logging in to Office Guru...")
        token = login(client)
        print("Login successful!")

        # 2. Fetch all lunch modules
        print("Fetching lunch modules...")
        lunch_modules = get_lunch_modules(client, token)
        for m in lunch_modules:
            print(f"  {m['partner_name']}: {m['_first_day']} → {m['_last_day']}")

        # 3. For each weekday, find the right module, fetch & parse its menu
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        import zoneinfo
        tz = zoneinfo.ZoneInfo("Europe/Copenhagen")

        # Cache: module_id → (partner_name, parsed_menu)
        module_menus: dict[str, tuple[str, dict]] = {}
        pdf_paths: list[str] = []

        try:
            for i, day in enumerate(day_order):
                date = monday + timedelta(days=i)
                module = get_module_for_date(lunch_modules, date)
                if not module:
                    print(f"  Skipping {day} — no module covers {date}")
                    continue

                mid = module["id"]
                if mid not in module_menus:
                    print(f"Fetching menu from {module['partner_name']} for week of {date}...")
                    pdf_url = get_menu_pdf_url(client, token, mid)
                    print(f"  PDF: {pdf_url}")
                    pdf_path = download_pdf(pdf_url)
                    pdf_paths.append(pdf_path)
                    menu = parse_menu_pdf(pdf_path)
                    module_menus[mid] = (module["partner_name"], menu)

                partner, menu = module_menus[mid]

                if day not in menu:
                    print(f"  Skipping {day} — no menu data in {partner} PDF")
                    continue

                if "--debug" in sys.argv:
                    import json as j
                    print(f"\n  {day} ({partner}):")
                    print(j.dumps(menu[day], indent=2, ensure_ascii=False))

                message = format_day_message(day, date, menu[day], partner)

                if "--dry-run" in sys.argv:
                    print(f"\n{'='*50}")
                    print(f"  {day} ({date}) [{partner}] — scheduled for {SEND_HOUR}:{SEND_MINUTE:02d}")
                    print(f"{'='*50}")
                    print(message)
                    continue

                # Calculate Unix timestamp for delivery
                deliver_at = datetime(
                    date.year, date.month, date.day,
                    SEND_HOUR, SEND_MINUTE, tzinfo=tz
                )
                post_at = int(deliver_at.timestamp())

                # Skip days that have already passed
                if post_at < int(datetime.now(tz).timestamp()) + 120:
                    print(f"  Skipping {day} — already past {SEND_HOUR}:{SEND_MINUTE:02d}")
                    continue

                print(f"  Scheduling {day} [{partner}] for {deliver_at.strftime('%Y-%m-%d %H:%M %Z')}...")
                schedule_slack_message(message, post_at)
                print(f"  ✓ Scheduled!")

            # Record this week as done
            if "--dry-run" not in sys.argv:
                os.makedirs(os.path.dirname(sent_file), exist_ok=True)
                with open(sent_file, "w") as f:
                    f.write(monday.isoformat())

        finally:
            for p in pdf_paths:
                os.unlink(p)

    print("Done!")


if __name__ == "__main__":
    main()
