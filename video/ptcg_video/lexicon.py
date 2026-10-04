"""Find card names in commentary text.

This module holds no card database of its own: card names come from the
project's card data (see the repo's data directory) or any file passed with
``--cards``. Accepted formats:

* ``.txt``  one name per line
* ``.json`` a list of names, or a list of objects with a ``name`` key
  (pokemontcg.io / TCGdex style), or ``{"cards": [...]}``
* ``.csv``  a ``name`` column

Auto-generated captions mangle names ("Charizard ex" -> "charizard x",
"Gardevoir" -> "garde voir"), so matching works on normalized tokens and,
when rapidfuzz is installed, falls back to fuzzy matching on long n-grams.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

try:
    from rapidfuzz import fuzz, process
except ImportError:  # optional
    fuzz = process = None


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("’", "'")
    text = re.sub(r"'s\b", "s", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return text.strip()


def _variants(norm: str) -> set[str]:
    out = {norm, norm.replace(" ", "")}
    if norm.endswith(" ex"):
        stem = norm[:-3]
        out |= {f"{stem} x", f"{stem} e x", f"{stem} eggs", stem + "ex"}
    if norm.endswith(" v"):
        out.add(norm[:-2] + " vee")
    return out


def load_card_names(path: str | Path) -> list[str]:
    path = Path(path)
    if path.suffix == ".txt":
        names = [l.strip() for l in path.read_text(encoding="utf-8").splitlines()]
    elif path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            names = [row.get("name", "") for row in csv.DictReader(f)]
    elif path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("cards") or data.get("data") or list(data.values())
        names = [d["name"] if isinstance(d, dict) else str(d) for d in data]
    else:
        raise ValueError(f"unsupported card list format: {path}")
    return sorted({n for n in names if n})


@dataclass
class Mention:
    t: float
    name: str
    matched: str
    score: float


class CardMatcher:
    def __init__(self, names: list[str], fuzzy_threshold: float = 90.0):
        self.index: dict[str, str] = {}
        for name in names:
            norm = normalize(name)
            if len(norm) < 3:
                continue
            for v in _variants(norm):
                # Keep the shortest canonical name per key (e.g. "Pikachu" over
                # "Pikachu (Promo)" when both normalize the same).
                if v not in self.index or len(name) < len(self.index[v]):
                    self.index[v] = name
        self.max_words = max((len(k.split()) for k in self.index), default=1)
        self.fuzzy_threshold = fuzzy_threshold
        self._fuzzy_keys = [k for k in self.index if len(k) >= 7]

    def __len__(self) -> int:
        return len(set(self.index.values()))

    def find(self, text: str) -> list[tuple[str, str, float]]:
        """Return (card name, matched text, score) for each mention, longest match first."""
        words = normalize(text).split()
        found = []
        i = 0
        while i < len(words):
            hit = None
            for n in range(min(self.max_words, len(words) - i), 0, -1):
                gram = " ".join(words[i : i + n])
                name = self.index.get(gram) or self.index.get(gram.replace(" ", ""))
                if name:
                    hit = (name, gram, 100.0, n)
                    break
                if process and n <= 3 and len(gram) >= 7 and self._fuzzy_keys:
                    best = process.extractOne(gram, self._fuzzy_keys, scorer=fuzz.ratio)
                    if best and best[1] >= self.fuzzy_threshold:
                        hit = (self.index[best[0]], gram, float(best[1]), n)
                        break
            if hit:
                found.append(hit[:3])
                i += hit[3]
            else:
                i += 1
        return found


# Game-action vocabulary for commentary. Each pattern is matched on normalized
# text. Kept here (not in the card data) because it is about how casters talk.
ACTION_PATTERNS: dict[str, list[str]] = {
    "knockout": [r"\bknock(?:s|ed)? (?:it |that |them )?out\b", r"\bko(?:s|ed)?\b", r"\bknockout\b"],
    "prize": [r"\btakes? (?:a|one|two|three|\d) prizes?\b", r"\bprizes? (?:left|remaining)\b", r"\b(?:one|two|three|four|five|six|\d) prizes? (?:left|to go)\b"],
    "attach": [r"\battach(?:es|ed|ing)?\b", r"\bmanual attachment\b"],
    "evolve": [r"\bevolv(?:e|es|ed|ing)\b", r"\brare candy\b"],
    "attack": [r"\battack(?:s|ed|ing)? (?:for|with|into)\b", r"\bswings? (?:for|in)\b", r"\bdamage\b"],
    "retreat": [r"\bretreat(?:s|ed|ing)?\b", r"\bswitch(?:es|ed)? (?:in|out|into)\b"],
    "supporter": [r"\bsupporter\b", r"\bplays? (?:a |the )?[a-z]+ (?:orders|research|request)\b"],
    "turn": [r"\bturn (?:one|two|three|four|five|\d+)\b", r"\bgoing (?:first|second)\b", r"\bpasses? (?:the )?turn\b"],
    "game_start": [r"\bgame (?:one|two|three|1|2|3)\b", r"\bshuffle up\b", r"\bopening hand\b", r"\bmulligan\b"],
    "game_end": [r"\b(?:that s|that is) game\b", r"\bwins? (?:game|the game|the set|the match)\b", r"\bconcede[sd]?\b", r"\bscoop(?:s|ed)?\b", r"\bextends? the hand\b", r"\bdecks? out\b"],
}
_COMPILED = {k: [re.compile(p) for p in v] for k, v in ACTION_PATTERNS.items()}


def find_actions(text: str) -> list[tuple[str, str]]:
    norm = normalize(text)
    hits = []
    for kind, patterns in _COMPILED.items():
        for p in patterns:
            m = p.search(norm)
            if m:
                hits.append((kind, m.group(0)))
                break
    return hits
