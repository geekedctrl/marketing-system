"""Conservative checks for a proposed contact against public search excerpts.

Matching text is evidence for review, not proof of current employment.
"""
import re
from urllib.parse import urlsplit

from .public_fetch import FetchError, checked_url
from .research import normalize


_STALE = re.compile(r"\b(former|formerly|previously|past|retired|ex[- ]|until|left|departed)\b", re.I)
_ROLE = re.compile(r"\b(head|chief|director|manager|executive|officer|president|lead)\b", re.I)
_NAME = re.compile(r"^[A-Z][A-Z .'-]{2,149}$")
_EMAIL = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w-])", re.I)


def public_email_candidates(name, company, rows, observed_at):
    """Extract literal public addresses for review, never infer or verify them."""
    name, company = normalize(name).casefold(), normalize(company).casefold()
    if len(name) < 3 or len(company) < 3 or not observed_at:
        return []
    candidates = []
    for row in rows[:10]:
        try:
            url, raw = row["url"], row["text"]
            checked_url(url)
            if not isinstance(raw, str):
                continue
        except (KeyError, TypeError, ValueError, FetchError):
            continue
        text = normalize(raw)
        if _STALE.search(text):
            continue
        lowered = text.casefold()
        name_match = re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", lowered)
        company_match = re.search(r"(?<!\w)" + re.escape(company) + r"(?!\w)", lowered)
        if not name_match or not company_match:
            continue
        for match in _EMAIL.finditer(text):
            start = min(name_match.start(), company_match.start(), match.start())
            end = max(name_match.end(), company_match.end(), match.end())
            if end - start > 500:
                continue
            quote = text[start:end]
            candidates.append({"email": match.group(), "source_url": url,
                               "evidence_quote": quote, "observed_at": observed_at,
                               "status": "PUBLICLY_SOURCED_UNVERIFIED"})
    return candidates[:5]


def role_priority(role):
    """Prefer operational decision-makers, then senior general leadership."""
    text = (role or "").casefold()
    senior = bool(re.search(r"\b(head|chief|director|manager|president|lead)\b", text))
    operational = bool(re.search(r"\b(operations?|fleet|logistics|transport|haulage|supply chain|warehouse|distribution)\b", text))
    return 3 if senior and operational else 2 if operational else 1 if senior and "people" not in text and "human" not in text else 0


def extract_official_people(rows, website, company):
    """Extract adjacent name/role bullets from saved official page text only."""
    official = (urlsplit(website).hostname or "").lower().removeprefix("www.")
    if not official:
        return []
    found = {}
    for row in rows[:100]:
        try:
            url, text = row["url"], row["text"]
            checked_url(url)
            host = (urlsplit(url).hostname or "").lower().removeprefix("www.")
            if host != official or not isinstance(text, str) or not re.search(r"\b(leadership|management|directors|executives)\b", text, re.I):
                continue
        except (KeyError, TypeError, ValueError, FetchError):
            continue
        lines = text.splitlines()
        for first, second in zip(lines, lines[1:]):
            name_match = re.fullmatch(r"\s*\*\s*([A-Z][A-Z .'-]{2,149})\s*", first)
            role_match = re.fullmatch(r"\s*\*\s*([A-Za-z][A-Za-z &'/-]{2,199})\s*", second)
            if not name_match or not role_match:
                continue
            name, role = normalize(name_match.group(1)), normalize(role_match.group(1))
            if len(name.split()) < 2 or not _NAME.fullmatch(name) or not _ROLE.search(role) or _ROLE.search(name):
                continue
            key = name.casefold()
            evidence = support_for_person(name, role, company, [row], website=website)
            candidate = {"name": name, "role": role, "url": url, "evidence": evidence,
                         "excerpt": normalize(first + " " + second)[:500],
                         "description": "Name and role listed together on the company's public leadership page."}
            if key in found and found[key]["role"].casefold() != role.casefold():
                found[key]["evidence"] = []
                found[key]["conflicting"] = True
            elif key not in found:
                found[key] = candidate
    # A leadership page with multiple people assigned the same singular title
    # can contain stale or conflicting sections; do not silently choose one.
    title_holders = {}
    for candidate in found.values():
        role_key = candidate["role"].casefold()
        if re.match(r"^(head of |chief .+ officer$)", role_key):
            title_holders.setdefault(role_key, []).append(candidate)
    for holders in title_holders.values():
        if len(holders) > 1:
            for candidate in holders:
                candidate["evidence"] = []
                candidate["conflicting"] = True
    return list(found.values())[:30]


def support_for_person(name, role, company, rows, *, website=None, profile_url=None):
    """Return safe excerpts explicitly containing all three proposed fields."""
    fields = [normalize(value).casefold() for value in (name, role, company)]
    if any(not value or len(value) < 3 for value in fields):
        return []
    evidence = []
    for row in rows[:10]:
        try:
            url, text = row["url"], row["text"]
            checked_url(url)
            if not isinstance(text, str):
                continue
        except (KeyError, TypeError, ValueError, FetchError):
            continue
        quote = normalize(text)
        lowered = quote.casefold()
        if _STALE.search(quote):
            continue
        matches = [re.search(r"(?<!\w)" + re.escape(value) + r"(?!\w)", lowered) for value in fields]
        if not all(matches):
            continue
        # Co-occurrence in a leadership page can refer to different people.
        # Require an explicit short name/role pairing, including adjacent bullets.
        name_pattern, role_pattern = map(re.escape, fields[:2])
        separator = r"\s*(?:(?:[,;:–—-]|\*)\s*|(?:is|as|serves as|the)\s+){0,3}"
        if not (re.search(r"(?<!\w)" + name_pattern + separator + role_pattern + r"(?!\w)", lowered)
                or re.search(r"(?<!\w)" + role_pattern + separator + name_pattern + r"(?!\w)", lowered)):
            continue
        if website:
            official = (urlsplit(website).hostname or "").lower().removeprefix("www.")
            source = (urlsplit(url).hostname or "").lower().removeprefix("www.")
            if not official:
                continue
            # A third party must explicitly identify the accepted website; a
            # person's own profile by itself cannot establish employment.
            if source != official:
                if profile_url and url.rstrip('/').casefold() == profile_url.rstrip('/').casefold():
                    continue
                site_match = re.search(r"(?<![\w.-])" + re.escape(official) + r"(?![\w.-])", lowered)
                if not site_match:
                    continue
                matches.append(site_match)
        start = min(m.start() for m in matches)
        end = max(m.end() for m in matches)
        if end - start > 500:
            continue
        start = max(0, min(start, len(quote) - 500))
        evidence.append({"source_url": url, "evidence_quote": quote[start:start + 500]})
    return evidence[:5]
