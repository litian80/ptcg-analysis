# 卡组打法（archetype game plans）

当前 Standard 环境里份额最大的 12 套卡组，每套一个 `<slug>.yaml`：怎么展开、谁来打、奖赏卡按什么顺序拿、
关键对局怎么打、复盘时常见的失误。slug 和名字沿用 Limitless Labs（`standings.csv`、`matches.csv` 里的
`archetype_slug`）。

| 文件 | 内容 | 怎么来的 |
|---|---|---|
| `meta_<窗口>.json` | 每套卡组的份额、Day 2 份额、总胜率、对各卡组的胜率、核心卡表（≥25% 卡表采用的卡、常见张数、最常用的版本） | `python -m ptcg.archetypes [窗口]` 从 `data/tournaments` 计算 |
| `<slug>.yaml` | 打法 | 手写：卡牌效果来自 `data/cards`，卡表来自 meta 文件，打法是推断的 |

当前窗口是 `TEF-30C`（Frankfurt、Brisbane 区域赛，2026-09-26，共 3602 名选手）；`meta_TEF-PBL.json` 是上一个窗口
（Worlds 2026、Baltimore）供对照。

## 覆盖的卡组（TEF-30C 份额）

| slug | 名字 | 份额 |
|---|---|---|
| `dragapult-ex` | Dragapult | 15.3% |
| `n-zoroark` | N's Zoroark | 6.7% |
| `dragapult-dusknoir` | Dragapult Dusknoir | 6.1% |
| `basic-box-m` | Basic Box（Mega Kangaskhan） | 6.1% |
| `slowking-scr` | Slowking | 6.1% |
| `alakazam-dudunsparce` | Alakazam Dudunsparce | 5.8% |
| `mega-excadrill-ex` | Mega Excadrill | 5.2% |
| `dragapult-blaziken` | Dragapult Blaziken | 4.4% |
| `festival-lead` | Festival Lead | 4.0% |
| `dhelmise-pbl` | Dhelmise | 3.5% |
| `ogerpon-meganium-hydrapple` | Ogerpon Meganium Hydrapple | 3.2% |
| `crustle-dri` | Crustle | 3.2% |

合计约 76% 的选手。

## 文件格式

```yaml
slug, name, name_zh, window, basis, summary
setup:        {turn_1: [...], turn_2: [...], turn_3: [...], key_cards: [卡名]}
attackers:    [{card, printing, role, prizes, attack, cost, damage, notes}]
support:      [{card, role, prizes}]
copy_targets: [...]          # 只有 slowking-scr 有
prize_map:
  liability:  对手怎么拿你的 6 张奖赏卡
  routes:     [{name, steps: [{turn, take, target, how}]}]   # take 合计为 6
matchups:     [{vs: slug, win_rate, plan}]
mistakes:     复盘时要找的常见失误
inferred:     没有直接证据、靠推断的说法
```

- 卡名一律用英文原名，和 TCG Live 日志、卡表一致。
- `turn` 是自己的第几个回合。
- `prizes` 是这只宝可梦被击倒时对手拿几张：Mega 宝可梦 ex 3 张，其他 ex 2 张，其余 1 张。

## 检查

```bash
python -m ptcg.plans
```

检查卡名都在卡牌数据里、`printing` 与卡名对得上、`prizes` 与卡牌类型一致、每条奖赏卡路线合计 6 张、
slug 存在、对局胜率与 meta 文件相差不超过 0.05（超出只警告，说明该更新打法了）。

## 可信度

- 份额、胜率、卡表、卡牌效果：直接来自数据。
- 展开顺序、奖赏卡路线、对局打法：根据卡牌效果和卡表推断，没有对局录像或日志统计支撑。
  具体不确定的地方写在每个文件的 `inferred` 里。日志解析和视频分析做出来以后，可以用真实对局来校正。
