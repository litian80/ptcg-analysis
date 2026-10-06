# Twinleaf battle sim (pilot)

Headless runner that lets two [Twinleaf](https://github.com/twinleafgg/twinleafgg) bots (MIT) play
full games between two decklists from `data/tournaments`, without Twinleaf's websocket server or
database. Results and the calibration against real matchup records are in `data/sim/`.

| file | what |
|---|---|
| `setup.sh` / `setup.ps1` | clone Twinleaf at a pinned commit into `sim/twinleaf/.twinleaf` (git-ignored), `npm install --ignore-scripts`, compile with `tsc` (2–3 min) |
| `pick_decks.py` | one list per archetype (best placing at Frankfurt, else Brisbane, Baltimore, Worlds) → `decks.json` |
| `run.js` | plays games, appends one JSON line per game |
| `summarize.py` | aggregates games → `data/sim/twinleaf_TEF-30C.json`, prints sim vs real per pair |

## Run

Linux / macOS / Git Bash:

```bash
bash sim/twinleaf/setup.sh
python sim/twinleaf/pick_decks.py                  # already committed; rerun after new events
node sim/twinleaf/run.js --check-decks             # card mapping report
node sim/twinleaf/run.js --bot simple --games 200 --out data/sim/games/simple.jsonl
node sim/twinleaf/run.js --bot advanced --games 30 --shard 0/4 --out data/sim/games/adv0.jsonl  # one per core
python sim/twinleaf/summarize.py
```

Windows (PowerShell, Node 18+ and Git installed):

```powershell
powershell -ExecutionPolicy Bypass -File sim\twinleaf\setup.ps1
node sim\twinleaf\run.js --check-decks
# one window per CPU core:
node sim\twinleaf\run.js --bot simple --games 200 --shard 0/4 --out data\sim\games\simple_shard0.jsonl
python sim\twinleaf\summarize.py
```

Useful options: `--pairs a:b,c:d`, `--seed N`, `--max-turns 80`, `--max-ms 120000`,
`--loop-limit N`, `--log-dir DIR` (writes the game log of every game that did not finish normally; with `--verbose`
of every game), `--confirm no` (stock Twinleaf behaviour, see below), `--twinleaf DIR`.

## How it works

* Builds a Twinleaf `Store` with a no-op handler, adds both decks with `AddPlayerAction`, then
  loops: the runner resolves shuffles and coin flips itself (seeded `Math.random`, so a game is
  reproducible from its `seed`) and answers the "go first?" prompt so seats alternate; every other
  prompt and every turn action comes from the bots' `decodeNextAction`.
* `--bot advanced` is Twinleaf's `ActionSearchAi` (beam search over legal actions within a turn,
  depth 3, scored by the simple bot's state evaluator **plus a Dragapult-specific playbook that is
  applied to whichever deck the bot plays**). `--bot simple` is `SimpleTacticsAi` (fixed priority
  list of tactics).
* Card mapping: set code + number against each Twinleaf card's `set`/`setNumber`; then the set code
  at the end of Twinleaf's `fullName` (Twinleaf stores some new cards under Japanese set codes, e.g.
  Mew ex 30C is `M6a 57`); then functional reprints from `data/cards/cards.csv`; basic energy by
  name. Names are normalised (curly apostrophes, accents, `[G]` → Grass). All 13 lists map with no
  substitutions. Growing Grass Energy exists in Twinleaf as `Growing [G] Energy` (POR 86); Chi-Yu
  TWM 39 exists in the source but is not exported by its set, so the runner registers it.
* Changes to Twinleaf behaviour, all in `run.js` and none of them game rules:
  * loop breaker (`--loop-limit 5`, default): if a bot picks the same non-prompt action more than
    5 times in one turn (it can re-activate an ability and cancel its prompt forever), the runner
    ends that turn;
  * the bots' `ConfirmPromptResolver` answers **no** to every optional "you may" prompt (Alakazam's
    Psychic Draw, etc.); by default the runner puts a resolver in front that answers yes;
  * speed: `require()` memoised, `deepClone` uses a `Map` instead of a linear array and does not
    chain prototypes, the undo backup clone in look-ahead simulators is skipped, and the UI-only
    `calculatePlayability` is disabled. Checked on 6 simple-bot games: same seed gives the same game with and without these (`SIM_NO_SPEEDUPS=1`), 5–8x faster.
* Speed on one core: simple bot about 0.6 games/s, advanced bot about one game per 25–35 s.
