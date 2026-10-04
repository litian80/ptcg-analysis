# ptcg-analysis

Pokémon TCG 的环境数据、卡组选择分析，以及对局记录/视频分析。

## 目录

| 路径 | 内容 |
|---|---|
| `ptcg/` | 数据采集和读取代码（`python -m ptcg ...`） |
| `data/formats/standard_rotations.json` | Standard 各赛季：生效日期（线下赛 / TCG Live）、合法 regulation mark、禁卡、来源链接。手工维护 |
| `data/formats/<赛季>/card_pool.csv` | 该赛季全部合法卡（按"同名同效果"合并重印），含所有可用版本 |
| `data/formats/limitless_formats.csv` | 大赛实际使用的卡池窗口（如 `TEF-30C` = 从 Temporal Forces 到 30th Celebration） |
| `data/cards/sets.csv`, `cards.csv` | Sword & Shield 以来所有系列和卡牌（含 regulation mark） |
| `data/cards/standard_card_names.txt` | 当前 Standard 合法卡名清单 |
| `data/tournaments/index.csv` | 已收录的大赛（Regional、International、Special Event、Worlds） |
| `data/tournaments/<日期>_<id>_<名称>/` | 每场比赛：`meta.json`、`standings.csv`（名次、战绩、卡组）、`decklists.jsonl`（完整 60 张卡表）、`matches.csv`（每一轮每一桌的双方卡组和胜负） |
| `video/` | YouTube 对局视频分析（另一条工作线） |

## 数据来源

- 卡牌和 regulation mark：[PokemonTCG/pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data)
- 大赛名次、卡表：[Limitless TCG](https://limitlesstcg.com/tournaments)
- 逐轮对局和全部选手卡组：[Limitless Labs](https://labs.limitlesstcg.com)（数据来自 RK9）
- Rotation 公告：见 `standard_rotations.json` 中每个赛季的 `sources`

## 如何保持更新

`.github/workflows/collect.yml` 每周一自动运行（也可在 Actions 页面手动运行）：

1. 重新拉取卡牌数据，新系列自动并入，重算各赛季卡池；
2. 只抓取尚未收录的大赛，并重抓最近 14 天的比赛（Limitless 常在赛后几天补全数据）；
3. 检查 rotation 文件：出现未登记的 regulation mark，或到了次年 3 月还没有下一赛季条目时，自动开 issue 提醒。

Rotation 和禁卡每年官方公告一次，需要手工在 `standard_rotations.json` 加一条。

## 本地运行

```bash
pip install -r requirements.txt
python -m ptcg cards                 # 卡牌 + 卡池
python -m ptcg tournaments --max 5   # 最新 5 场未收录的大赛
python -m ptcg check                 # rotation 文件是否过期
```

```python
from ptcg.formats import season_for
from ptcg.cards import pool

season = season_for("2026-09-26")            # 2026-27
cards = pool(season, last_set="30C")         # TEF-30C 窗口的合法卡
```
