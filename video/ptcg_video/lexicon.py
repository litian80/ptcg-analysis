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


def normalize(text: str, lower: bool = True) -> str:
    """ASCII, lowercase, punctuation to spaces; "Boss's" -> "bosss", "that's" -> "thats"."""
    text = text.replace("’", "'")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    if lower:
        text = text.lower()
    text = re.sub(r"'[sS]\b", "s", text)
    text = re.sub(r"[^A-Za-z0-9]+", " ", text)
    return text.strip()


def _variants(norm: str) -> set[str]:
    out = {norm, norm.replace(" ", "")}
    if norm.endswith(" ex"):
        stem = norm[:-3]
        out |= {f"{stem} x", f"{stem} e x", f"{stem} eggs", stem + "ex"}
    if norm.endswith(" v"):
        out.add(norm[:-2] + " vee")
    if norm.endswith(" card") and len(norm.split()) > 2:
        out.add(norm[:-5])  # casters drop it: "Special Red" for Special Red Card
    return out


def load_card_names(path: str | Path) -> list[str]:
    path = Path(path)
    if path.suffix == ".txt":
        names = [l.strip() for l in path.read_text(encoding="utf-8-sig").splitlines()]
    elif path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as f:
            names = [row.get("name", "") for row in csv.DictReader(f)]
    elif path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
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

    def find(self, text: str, cased: bool | None = None) -> list[tuple[str, str, float]]:
        """Return (card name, matched text, score) for each mention, longest match first.

        cased: whether the caption track uses capitals at all (default: guess from text).
        """
        if cased is None:
            cased = text != text.lower()
        words = normalize(text).split()
        original = normalize(text, lower=False).split()  # same tokens, case kept
        initial = _sentence_initial(text, len(words))
        found = []
        i = 0
        while i < len(words):
            hit = None
            for n in range(min(self.max_words, len(words) - i), 0, -1):
                gram = " ".join(words[i : i + n])
                name = self.index.get(gram)
                collapsed = gram.replace(" ", "")
                # ASR splits long names ("garde voir"); don't glue short words ("be a" -> Bea).
                if not name and n > 1 and len(collapsed) >= 6:
                    name = self.index.get(collapsed)
                # "will" / "judge" are words, "Will" / "Judge" are cards. A capital
                # that only starts a sentence ("Will he find it?") doesn't count.
                word_ok = not (n == 1 and cased and (not original[i][:1].isupper() or initial[i]))
                if name and not word_ok and _word_like(name):
                    continue
                if name:
                    hit = (name, gram, 100.0, n)
                    break
                if process and n <= 3 and len(gram) >= 7 and self._fuzzy_keys:
                    best = process.extractOne(gram, self._fuzzy_keys, scorer=fuzz.ratio)
                    if best and best[1] >= self.fuzzy_threshold:
                        target = self.index[best[0]]
                        if not word_ok and _word_like(target):
                            continue
                        hit = (target, gram, float(best[1]), n)
                        break
            if hit:
                found.append(hit[:3])
                i += hit[3]
            else:
                i += 1
        return found


# One-word card names that are also everyday English words. In captions that
# use capitals, these (and any one-word name of 4 letters or fewer) only count
# when capitalized: "Judge" the Supporter, not "the judge ruled".
COMMON_WORD_NAMES = {
    "blowtorch", "caretaker", "cook", "dawn", "firebreather", "grant", "hop",
    "judge", "picnicker", "potion", "red", "repel", "ruffian", "surfer", "switch",
    "waitress",
}


def _sentence_initial(text: str, count: int) -> list[bool]:
    """For each normalized token of text: is it the first word of a sentence?"""
    flags: list[bool] = []
    for sentence in re.split(r"[.!?]+", text):
        flags += [k == 0 for k in range(len(normalize(sentence).split()))]
    return flags if len(flags) == count else [False] * count


def _word_like(name: str) -> bool:
    return " " not in name and (len(name) <= 4 or normalize(name) in COMMON_WORD_NAMES)



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
    "game_end": [r"\b(?:thats|that is) game\b", r"\bwins? (?:game|the game|the set|the match)\b", r"\bconcede[sd]?\b", r"\bscoop(?:s|ed)?\b", r"\bextends? the hand\b", r"\bdecked out\b",
                 r"\btakes? game (?:number )?(?:one|two|three|\d)\b"],
    # Ends the whole match. Also said in player intros ("your 2024 world
    # champion"), so it only closes the final game; see events._game_spans.
    "match_end": [r"\b(?:your|our|new) (?:\d{4} )?(?:\w+ ){0,5}champions?\b",
                  r"\bis the (?:\d{4} )?(?:\w+ ){0,4}champions?\b",
                  r"\bwins (?:the )?(?:whole thing|tournament|championship|world championship|worlds)\b"],
}
_COMPILED = {k: [re.compile(p) for p in v] for k, v in ACTION_PATTERNS.items()}


# Casters spend more time on what could happen than on what did ("he needs 16
# cards in hand to get the KO", "if he finds the Boss, that's game"). A
# knockout / prize / game-end line counts as something that happened unless
# it's a question, or the words *leading up to* the phrase in its sentence
# hedge it. Only the lead is checked: a conditional comes before its
# consequence, and what follows a real KO is often about the next turn
# ("knocks out the Dusknoir, now he needs one more").
_CONDITIONAL = (
    r"if|unless|could|would|should|can|cannot|might|will|ll|\w+n t|not|no|need|needs|needed|must|"
    r"has to|have to|gonna|whether|possible|possibly|potential|potentially|hoping|hope|worried|"
    r"before|until|one more|only way"
)
_HEDGE = re.compile(
    rf"\b(?:{_CONDITIONAL}|going to|want|wants|try|tries|trying|threat|threatens|threatening|"
    r"set up|setting up|looking at|look for|avoid|avoids|chance|next turn)\b"
)
# Game ends are often announced a moment early ("Andrew is going to take game
# number one"), so "going to" doesn't hedge them; conditionals do.
_GAME_HEDGE = re.compile(rf"\b(?:{_CONDITIONAL})\b")
_MATCH_HEDGE = re.compile(
    rf"\b(?:{_CONDITIONAL}|going to|be|being|become|becoming|former|last year|defending|previous|"
    r"winner of|whoever|wins this|away)\b"
)
_INFINITIVE = re.compile(r"\bto(?: \w+){0,2} ?$")  # "to KO", "to get the KO", "to take two prizes"
_LEAD_HEDGES = {"knockout": _HEDGE, "prize": _HEDGE, "game_end": _GAME_HEDGE, "match_end": _MATCH_HEDGE}
_SENTENCE = re.compile(r"[^.!?]+[.!?]*")
_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")


def is_definite(kind: str, text: str, before: str = "", year: int | None = None) -> bool:
    """False when a knockout / prize / game-end / match-end line is talk about a
    possibility, not an event.

    before: the caption text just before this line, when it is the same
    sentence running on (auto-captions break sentences across lines).
    year: the video's year; a "2024 world champion" in a 2026 video is an intro.
    """
    hedge = _LEAD_HEDGES.get(kind)
    if hedge is None:
        return True
    for idx, sentence in enumerate(_SENTENCE.findall(text) or [text]):
        norm = normalize(sentence)
        m = next((m for p in _COMPILED[kind] if (m := p.search(norm))), None)
        if m is None:
            continue
        if sentence.rstrip().endswith("?"):
            return False
        lead = norm[: m.start()]
        if idx == 0 and before:
            lead = f"{normalize(before)} {lead}"
        if hedge.search(lead):
            return False
        if kind in ("knockout", "prize") and _INFINITIVE.search(lead.strip() + " "):
            return False
        if kind == "match_end" and year and any(int(y) != year for y in _YEAR.findall(m.group(0))):
            return False
        return True
    return True


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
