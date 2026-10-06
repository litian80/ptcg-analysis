#!/usr/bin/env node
/*
 * Headless Twinleaf battle runner: two bots play full games between two decklists.
 * No websocket server, no database: it drives Twinleaf's Store directly.
 *
 * Usage (from the repo root, after sim/twinleaf/setup.sh):
 *   node sim/twinleaf/run.js --pairs dragapult-ex:crustle-dri --games 20
 *   node sim/twinleaf/run.js --shard 0/4 --games 200 --out data/sim/games/shard0.jsonl
 *   node sim/twinleaf/run.js --check-decks
 *
 * Options:
 *   --twinleaf DIR    Twinleaf checkout (default sim/twinleaf/.twinleaf or $TWINLEAF_DIR)
 *   --decks FILE      deck file from pick_decks.py (default sim/twinleaf/decks.json)
 *   --pairs a:b,...   explicit pairs (default: every recommended deck x every opponent)
 *   --shard i/n       run only pairs with index % n == i
 *   --games N         games per pair (alternating who goes first), default 20
 *   --bot advanced|simple   Twinleaf bot for both seats (default advanced)
 *   --confirm yes|no  how the bot answers optional "you may ..." ConfirmPrompts.
 *                     Twinleaf's stock resolver always says no; default here is yes.
 *   --seed N          base seed (each game is seeded from base seed, pair and game index)
 *   --max-turns N     declare a draw/timeout after N turns (default 80)
 *   --max-ms N        per-game wall clock limit (default 120000)
 *   --out FILE        append one JSON line per game (default data/sim/games/twinleaf_games.jsonl)
 *   --loop-limit N    end a turn once the same action repeats more than N times in it (default 5, 0 = off)
 *   --log-dir DIR     write the text log of games that end in error/timeout/stall here
 */
'use strict';
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..');

function parseArgs(argv) {
  const a = {
    twinleaf: process.env.TWINLEAF_DIR || path.join(__dirname, '.twinleaf'),
    decks: path.join(__dirname, 'decks.json'),
    games: 20, bot: 'advanced', confirm: 'yes', seed: 1, maxTurns: 80, maxMs: 120000,
    out: path.join(REPO, 'data/sim/games/twinleaf_games.jsonl'),
    logDir: null, loopLimit: 5, pairs: null, shard: null, checkDecks: false, verbose: false,
  };
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    const v = () => argv[++i];
    switch (k) {
      case '--twinleaf': a.twinleaf = v(); break;
      case '--decks': a.decks = v(); break;
      case '--pairs': a.pairs = v().split(',').map(s => s.split(':')); break;
      case '--shard': { const [x, n] = v().split('/').map(Number); a.shard = { i: x, n }; break; }
      case '--games': a.games = Number(v()); break;
      case '--bot': a.bot = v(); break;
      case '--confirm': a.confirm = v(); break;
      case '--seed': a.seed = Number(v()); break;
      case '--max-turns': a.maxTurns = Number(v()); break;
      case '--max-ms': a.maxMs = Number(v()); break;
      case '--out': a.out = v(); break;
      case '--log-dir': a.logDir = v(); break;
      case '--loop-limit': a.loopLimit = Number(v()); break;
      case '--check-decks': a.checkDecks = true; break;
      case '--verbose': a.verbose = true; break;
      default: throw new Error('unknown option ' + k);
    }
  }
  return a;
}

const args = parseArgs(process.argv);

// ---------- seeded randomness: Twinleaf uses Math.random for shuffles, coin flips, bots ----------
let rngState = 1;
function mulberry32() {
  rngState |= 0; rngState = (rngState + 0x6D2B79F5) | 0;
  let t = Math.imul(rngState ^ (rngState >>> 15), 1 | rngState);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
}
Math.random = mulberry32;
function seedFor(...parts) {
  let h = 2166136261;
  for (const ch of parts.join('|')) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

// ---------- load Twinleaf ----------
const OUT = path.join(path.resolve(args.twinleaf), 'ptcg-server', 'output');
if (!fs.existsSync(path.join(OUT, 'game', 'index.js'))) {
  console.error(`Twinleaf build not found at ${OUT}. Run sim/twinleaf/setup.sh first (or pass --twinleaf).`);
  process.exit(2);
}
// Twinleaf calls require() inside hot paths (Store.callReduceEffect); Node re-resolves the path each
// time, which was ~50% of CPU. Memoise require per (calling module, request).
const SPEEDUPS = !process.env.SIM_NO_SPEEDUPS; // set SIM_NO_SPEEDUPS=1 to verify they change nothing
if (SPEEDUPS) {
  const Module = require('module');
  const orig = Module.prototype.require;
  Module.prototype.require = function (id) {
    let memo = this.__reqMemo;
    if (memo === undefined) { memo = new Map(); Object.defineProperty(this, '__reqMemo', { value: memo }); }
    let m = memo.get(id);
    if (m === undefined) {
      if (global.__reqMiss) global.__reqMiss[this.filename + ' ' + id] = (global.__reqMiss[this.filename + ' ' + id] || 0) + 1;
      m = orig.call(this, id); memo.set(id, m);
    }
    return m;
  };
}
const quiet = console.log; // Twinleaf logs a lot; silence it while loading/playing
console.log = () => {};
const T = require(path.join(OUT, 'game'));
const sets = require(path.join(OUT, 'sets'));
const { CardManager } = require(path.join(OUT, 'game/cards/card-manager'));
const { Store } = require(path.join(OUT, 'game/store/store'));
const { ActionSearchAi } = require(path.join(OUT, 'advanced-bot/action-search-ai'));
const { defaultAdvancedBotOptions } = require(path.join(OUT, 'advanced-bot/advanced-bot-definitions'));
const { SimpleTacticsAi } = require(path.join(OUT, 'simple-bot/simple-tactics-ai'));
const simpleDefs = require(path.join(OUT, 'simple-bot/simple-bot-definitions'));
const { PromptResolver } = require(path.join(OUT, 'simple-bot/prompt-resolver/prompt-resolver'));
console.log = quiet;

// Twinleaf's deepClone (used by the bots' look-ahead Simulator on every candidate move) tracks
// already-cloned objects in an array searched linearly, i.e. O(n^2) in state size. Same algorithm,
// identity Map instead of the array. Compiled TS calls utils_1.deepClone at call time, so
// replacing the export is enough.
if (SPEEDUPS) {
  const U = require(path.join(OUT, 'utils/utils'));
  function deepCloneFast(source, ignores = [], refMap = new Map()) {
    if (source === null) return null;
    if (typeof source === 'function') return source;
    if (source instanceof Array) return source.map(item => deepCloneFast(item, ignores, refMap));
    if (source instanceof Object) {
      for (let i = 0; i < ignores.length; i++) if (source instanceof ignores[i]) return source;
      const ref = refMap.get(source);
      if (ref !== undefined) return ref;
      const dest = Object.create(Object.getPrototypeOf(source));
      refMap.set(source, dest);
      const keys = Object.keys(source); // own enumerable keys, same set as for-in + hasOwnProperty
      for (let i = 0; i < keys.length; i++) {
        const v = source[keys[i]];
        dest[keys[i]] = (v === null || typeof v !== 'object') ? v : deepCloneFast(v, ignores, refMap);
      }
      return dest;
    }
    return source;
  }
  // Store.reduce() deep-clones the whole state as an undo backup before every action. Inside the
  // bots' look-ahead Simulator an illegal action just discards the simulator, so skip that backup.
  const { Simulator } = require(path.join(OUT, 'game/bots/simulator'));
  let skipCloneOf = null;
  const origDispatch = Store.prototype.dispatch;
  Store.prototype.dispatch = function (action, roleId) {
    if (this.handler instanceof Simulator) skipCloneOf = this.state;
    try { return origDispatch.call(this, action, roleId); } finally { skipCloneOf = null; }
  };
  U.deepClone = (source, ignores = [], refMap) => (source === skipCloneOf && source !== null) ? (skipCloneOf = null, source) : (
    deepCloneFast(source, ignores, Array.isArray(refMap) ? new Map(refMap.map(r => [r.s, r.d])) : (refMap || new Map())));
}

// Store.calculatePlayability fills player.playableCardIds (UI hints only; no rule reads them) by
// test-playing every hand card after every effect. Headless, it only costs time.
if (SPEEDUPS) Store.prototype.calculatePlayability = function (state) { return state; };

// Overlay: cards that exist in the Twinleaf source tree but are not exported by their set index.
const OVERLAY = [
  ['game/../sets/10-scarlet-and-violet/set-twilight-masquerade/chi-yu', 'ChiYu'], // Chi-Yu TWM 39
];

const cm = CardManager.getInstance();
const allCards = [];
for (const k of Object.keys(sets)) {
  if (!k.startsWith('set') || !Array.isArray(sets[k])) continue;
  try { cm.defineSet(sets[k]); } catch (e) { /* duplicate across sets: ignore */ }
  allCards.push(...sets[k]);
}
for (const [mod, cls] of OVERLAY) {
  try {
    const C = require(path.join(OUT, mod))[cls];
    const card = new C();
    if (!cm.isCardDefined(card.fullName)) { cm.defineSet([card]); allCards.push(card); }
  } catch (e) { console.error('overlay failed', mod, e.message); }
}

// ---------- decklist -> Twinleaf fullName ----------
function norm(s) {
  return s.replace(/[‘’]/g, "'").normalize('NFKD').replace(/[̀-ͯ]/g, '')
    .replace(/\[G\]/g, 'Grass').replace(/\[R\]/g, 'Fire').replace(/\[W\]/g, 'Water')
    .replace(/\[L\]/g, 'Lightning').replace(/\[P\]/g, 'Psychic').replace(/\[F\]/g, 'Fighting')
    .replace(/\[D\]/g, 'Darkness').replace(/\[M\]/g, 'Metal').toLowerCase().trim();
}
const byName = new Map();
for (const c of allCards) {
  const n = norm(c.name);
  if (!byName.has(n)) byName.set(n, []);
  byName.get(n).push(c);
}
// functional reprint groups from the repo's card table (same functional_id = same card text)
const reprints = new Map(); // "SET NUM" -> [["SET","NUM"],...]
try {
  const lines = fs.readFileSync(path.join(REPO, 'data/cards/cards.csv'), 'utf8').split(/\r?\n/);
  const hdr = lines[0].split(',');
  const iCode = hdr.indexOf('code'), iNum = hdr.indexOf('number'), iFid = hdr.indexOf('functional_id');
  const groups = new Map(); const fidOf = new Map();
  for (const line of lines.slice(1)) {
    if (!line) continue;
    const f = line.split(','); // fid is the last column; names with commas don't matter here
    const code = f[iCode], num = f[iNum], fid = f[f.length - 1];
    if (!groups.has(fid)) groups.set(fid, []);
    groups.get(fid).push([code, num]); fidOf.set(code + ' ' + num, fid);
  }
  for (const [k, fid] of fidOf) reprints.set(k, groups.get(fid));
} catch (e) { /* optional */ }

const REG_ORDER = 'JIHGFEDCBA';
function mapCard(name, set, num) {
  const cands = byName.get(norm(name)) || [];
  const how = (c, h) => ({ fullName: c.fullName, how: h, twinleaf: `${c.name} ${c.set} ${c.setNumber}` });
  let c = cands.find(x => x.set === set && String(x.setNumber) === num);
  if (c) return how(c, 'exact');
  c = cands.find(x => x.fullName.split(' ').pop() === set);
  if (c) return how(c, 'set-code-in-fullName');
  for (const [s2, n2] of (reprints.get(set + ' ' + num) || [])) {
    c = cands.find(x => x.set === s2 && String(x.setNumber) === n2);
    if (c) return how(c, `reprint ${s2} ${n2}`);
  }
  if (/ Energy$/.test(name) && cands.length) {
    c = cands.find(x => x.set === 'SVE') || cands[0];
    return how(c, 'basic energy');
  }
  if (cands.length) {
    const sorted = cands.slice().sort((a, b) =>
      REG_ORDER.indexOf(a.regulationMark || 'A') - REG_ORDER.indexOf(b.regulationMark || 'A'));
    return how(sorted[0], 'NAME ONLY (check text)');
  }
  return null;
}

function buildDeck(lines) {
  const deck = []; const report = [];
  for (const line of lines) {
    const m = /^(\d+) (.+) (\S+) (\S+)$/.exec(line);
    if (!m) throw new Error('bad card line ' + line);
    const [, n, name, set, num] = m;
    const r = mapCard(name, set, num);
    if (!r) { report.push({ line, missing: true }); continue; }
    if (r.how !== 'exact') report.push({ line, ...r });
    for (let i = 0; i < Number(n); i++) deck.push(r.fullName);
  }
  return { deck, report };
}

const deckFile = JSON.parse(fs.readFileSync(args.decks, 'utf8'));
const DECKS = {};
let deckProblems = false;
for (const [slug, d] of Object.entries(deckFile.decks)) {
  const { deck, report } = buildDeck(d.cards);
  DECKS[slug] = deck;
  const valid = new (require(path.join(OUT, 'game/cards/deck-analyser')).DeckAnalyser)(deck).isValid(T.Format.STANDARD);
  if (args.checkDecks || report.some(r => r.missing) || deck.length !== 60 || !valid) {
    console.error(`${slug}: ${deck.length} cards, valid=${valid}`);
    for (const r of report) console.error('   ', JSON.stringify(r));
    if (report.some(r => r.missing) || deck.length !== 60 || !valid) deckProblems = true;
  }
}
if (args.checkDecks) process.exit(deckProblems ? 1 : 0);

// ---------- bots ----------
class ConfirmYesResolver extends PromptResolver {
  resolvePrompt(state, player, prompt) {
    if (prompt instanceof T.ConfirmPrompt) return new T.ResolvePromptAction(prompt.id, true);
    return undefined;
  }
}
function makeAi(clientId, deck) {
  const client = { id: clientId, name: 'bot' + clientId };
  if (args.bot === 'simple') {
    const opts = {
      tactics: simpleDefs.allSimpleTactics, scores: simpleDefs.defaultStateScores,
      promptResolvers: simpleDefs.allPromptResolvers, arbiter: simpleDefs.defaultArbiterOptions,
    };
    if (args.confirm === 'yes') opts.promptResolvers = [ConfirmYesResolver, ...opts.promptResolvers];
    return new SimpleTacticsAi(client, opts, deck);
  }
  const opts = Object.assign({}, defaultAdvancedBotOptions);
  if (args.confirm === 'yes') opts.promptResolvers = [ConfirmYesResolver, ...opts.promptResolvers];
  return new ActionSearchAi(client, opts, deck);
}

// ---------- arbiter (shuffles, coin flips, who-goes-first) ----------
function shuffleOrder(len) {
  const order = [...Array(len).keys()];
  for (let i = len - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [order[i], order[j]] = [order[j], order[i]];
  }
  return order;
}
function arbiterAction(state, prompt, firstId) {
  if (prompt instanceof T.ShuffleDeckPrompt) {
    const owner = state.players.find(p => p.id === prompt.getPerspectivePlayerId());
    return new T.ResolvePromptAction(prompt.id, shuffleOrder(owner.deck.cards.length));
  }
  if (prompt instanceof T.CoinFlipPrompt) {
    return new T.ResolvePromptAction(prompt.id, Math.random() < 0.5);
  }
  if (prompt instanceof T.ConfirmPrompt && prompt.message === T.GameMessage.GO_FIRST) {
    return new T.ResolvePromptAction(prompt.id, prompt.playerId === firstId);
  }
  return undefined;
}

function logText(logs) {
  return logs.map(l => {
    let msg = String(l.message);
    for (const [k, v] of Object.entries(l.params || {})) msg += ` ${k}=${v}`;
    return `[${l.client}] ${msg}`;
  }).join('\n');
}

// ---------- one game ----------
function playGame(slugA, slugB, firstSeat, seed) {
  rngState = seed;
  const settings = new T.GameSettings();
  const handler = { onStateChange() {}, gameSettings: settings };
  const store = new Store(handler);
  store.state.rules = settings.rules;
  store.state.gameSettings = settings;
  const ids = [1, 2];
  const ais = [makeAi(1, DECKS[slugA]), makeAi(2, DECKS[slugB])];
  const firstId = ids[firstSeat];
  const t0 = Date.now();
  const res = { a: slugA, b: slugB, first: firstSeat === 0 ? 'a' : 'b', seed, winner: null, turns: 0,
    steps: 0, invalid: 0, error: null, end: null, prizesLeft: null, deckLeft: null, ms: 0 };
  let invalidRun = 0;
  const archived = [];
  let loopTurn = -1; const loopCounts = new Map();
  try {
    store.dispatch(new T.AddPlayerAction(1, 'A', DECKS[slugA]));
    store.dispatch(new T.AddPlayerAction(2, 'B', DECKS[slugB]));
    while (store.state.phase !== T.GamePhase.FINISHED) {
      const state = store.state;
      if (state.turn > args.maxTurns) { res.end = 'turn-limit'; break; }
      if (Date.now() - t0 > args.maxMs) { res.end = 'time-limit'; break; }
      res.steps++;
      if (res.firstActual === undefined && state.turn >= 1 && state.phase === T.GamePhase.PLAYER_TURN) {
        res.firstActual = state.players[state.activePlayer].id === 1 ? 'a' : 'b';
      }
      let action;
      const open = state.prompts.filter(p => p.result === undefined);
      for (const p of open) { action = arbiterAction(state, p, firstId); if (action) break; }
      if (!action) {
        for (const ai of ais) { action = ai.decodeNextAction(state); if (action) break; }
      }
      if (!action) {
        // nobody can act: stuck prompt nobody resolves
        if (open.length) {
          res.error = 'unresolved prompt ' + open.map(p => p.constructor.name).join(',');
        } else {
          res.error = 'no action';
        }
        res.end = 'stuck';
        break;
      }
      // Loop breaker: Twinleaf bots can re-activate an ability whose prompt they then cancel
      // (Mew ex Memory Helix, Munkidori Adrena-Brain, ...) forever within one turn. After the same
      // non-prompt action is chosen more than LOOP_LIMIT times in a turn, end that player's turn.
      if (args.loopLimit > 0 && !(action instanceof T.ResolvePromptAction)) {
        if (loopTurn !== state.turn) { loopTurn = state.turn; loopCounts.clear(); }
        const key = action.constructor.name + JSON.stringify(action);
        const c = (loopCounts.get(key) || 0) + 1;
        loopCounts.set(key, c);
        if (c > args.loopLimit && !open.length) {
          res.loopBreaks = (res.loopBreaks || 0) + 1;
          action = new T.PassTurnAction(state.players[state.activePlayer].id);
        }
      }
      try {
        store.dispatch(action);
        invalidRun = 0;
        // keep the live log short: the bots clone the whole state per candidate move
        if (store.state.logs.length > 60) archived.push(...store.state.logs.splice(0, store.state.logs.length - 20));
      } catch (e) {
        res.invalid++; invalidRun++;
        if (invalidRun > 20) {
          // bot keeps proposing an illegal move: pass the turn (or cancel the prompt)
          const active = state.players[state.activePlayer];
          try {
            if (open.length) store.dispatch(new T.ResolvePromptAction(open[0].id, null));
            else store.dispatch(new T.PassTurnAction(active.id));
          } catch (e2) {
            res.error = 'illegal-loop: ' + (e.message || e); res.end = 'stuck'; break;
          }
          invalidRun = 0;
        }
      }
    }
  } catch (e) {
    res.error = String(e && e.stack ? e.stack.split('\n').slice(0, 3).join(' | ') : e);
    res.end = 'exception';
  }
  const st = store.state;
  res.turns = st.turn;
  res.ms = Date.now() - t0;
  if (st.phase === T.GamePhase.FINISHED) {
    res.end = res.end || 'finished';
    res.winner = st.winner === T.GameWinner.PLAYER_1 ? 'a' : st.winner === T.GameWinner.PLAYER_2 ? 'b'
      : st.winner === T.GameWinner.DRAW ? 'draw' : 'none';
    // map Twinleaf player index -> our seat (players[0] is client 1 = deck A)
    if (st.players[0] && st.players[0].id !== 1 && (res.winner === 'a' || res.winner === 'b')) {
      res.winner = res.winner === 'a' ? 'b' : 'a';
    }
  }
  res.prizesLeft = st.players.map(p => p.prizes.reduce((s, l) => s + l.cards.length, 0));
  res.deckLeft = st.players.map(p => p.deck.cards.length);
  res.winReason = winReason(st);
  if (args.logDir && (res.end !== 'finished' || args.verbose)) {
    fs.mkdirSync(args.logDir, { recursive: true });
    fs.writeFileSync(path.join(args.logDir, `${slugA}__${slugB}__${seed}.log`), JSON.stringify(res) + '\n' + logText(archived.concat(st.logs)));
  }
  return res;
}

function winReason(st) {
  if (st.phase !== T.GamePhase.FINISHED) return null;
  const last = st.logs.slice(-6).map(l => String(l.message)).join(' ');
  const m = /LOG_GAME_FINISHED_[A-Z_]+|LOG_PLAYER_NO_|LOG_[A-Z_]*(PRIZE|DECK|CONCEDE|ACTIVE|BENCH)[A-Z_]*/.exec(last);
  return m ? m[0] : last.slice(-80);
}

// ---------- main ----------
if (deckProblems) { console.error('deck problems above; fix before running'); process.exit(1); }
let pairs = args.pairs;
if (!pairs) {
  pairs = [];
  for (const r of deckFile.recommended) for (const o of deckFile.opponents) pairs.push([r, o]);
}
if (args.shard) pairs = pairs.filter((_, i) => i % args.shard.n === args.shard.i);
fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
const outFd = fs.openSync(args.out, 'a');
const tStart = Date.now();
let n = 0;
for (let g = 0; g < args.games; g++) {      // interleave pairs so partial runs cover every pair
  for (const [a, b] of pairs) {
    const seed = seedFor(args.seed, args.bot, a, b, g);
    console.log = () => {};
    const r = playGame(a, b, g % 2, seed);
    console.log = quiet;
    r.bot = args.bot; r.confirm = args.confirm; r.loopLimit = args.loopLimit; r.game = g;
    fs.writeSync(outFd, JSON.stringify(r) + '\n');
    n++;
    if (args.verbose || n % 20 === 0) {
      process.stderr.write(`${n} games, ${(n / ((Date.now() - tStart) / 1000)).toFixed(2)} g/s; last ${a} vs ${b}: ${r.winner} ${r.end} t${r.turns} ${r.ms}ms\n`);
    }
  }
}
fs.closeSync(outFd);
process.stderr.write(`done: ${n} games in ${((Date.now() - tStart) / 1000).toFixed(1)}s\n`);
